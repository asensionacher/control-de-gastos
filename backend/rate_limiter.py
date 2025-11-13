"""
Rate limiter para prevenir abuso de endpoints
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import HTTPException, status, Request
import threading

class RateLimiter:
    """
    Rate limiter simple basado en IP
    """
    def __init__(self):
        # Estructura: {ip: [(timestamp, endpoint), ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()
    
    def _clean_old_requests(self, ip: str, window_minutes: int):
        """Eliminar requests antiguos fuera de la ventana de tiempo"""
        cutoff = datetime.now() - timedelta(minutes=window_minutes)
        with self.lock:
            self.requests[ip] = [
                (ts, endpoint) for ts, endpoint in self.requests[ip]
                if ts > cutoff
            ]
    
    def check_rate_limit(
        self,
        request: Request,
        endpoint: str,
        max_requests: int,
        window_minutes: int
    ) -> bool:
        """
        Verificar si se ha excedido el límite de requests
        
        Args:
            request: Request de FastAPI para obtener la IP
            endpoint: Nombre del endpoint (ej: "register")
            max_requests: Número máximo de requests permitidos
            window_minutes: Ventana de tiempo en minutos
        
        Returns:
            True si está permitido, False si se excedió el límite
        
        Raises:
            HTTPException: Si se excede el límite
        """
        # Obtener IP del cliente
        client_ip = request.client.host if request.client else "unknown"
        
        # Limpiar requests antiguos
        self._clean_old_requests(client_ip, window_minutes)
        
        # Contar requests en la ventana de tiempo
        with self.lock:
            endpoint_requests = [
                ts for ts, ep in self.requests[client_ip]
                if ep == endpoint
            ]
            
            if len(endpoint_requests) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Demasiados intentos. Por favor, espera {window_minutes} minutos."
                )
            
            # Registrar este request
            self.requests[client_ip].append((datetime.now(), endpoint))
        
        return True
    
    def get_remaining_attempts(
        self,
        request: Request,
        endpoint: str,
        max_requests: int,
        window_minutes: int
    ) -> Tuple[int, datetime]:
        """
        Obtener intentos restantes y tiempo de reseteo
        
        Returns:
            (intentos_restantes, tiempo_de_reseteo)
        """
        client_ip = request.client.host if request.client else "unknown"
        self._clean_old_requests(client_ip, window_minutes)
        
        with self.lock:
            endpoint_requests = [
                ts for ts, ep in self.requests[client_ip]
                if ep == endpoint
            ]
            
            remaining = max(0, max_requests - len(endpoint_requests))
            
            if endpoint_requests:
                oldest_request = min(endpoint_requests)
                reset_time = oldest_request + timedelta(minutes=window_minutes)
            else:
                reset_time = datetime.now()
            
            return remaining, reset_time

# Instancia global
rate_limiter = RateLimiter()
