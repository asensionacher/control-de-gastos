# Exportación e Importación de Transacciones CSV

## Descripción

El sistema permite exportar e importar todas las transacciones de un usuario en formato CSV. Esta funcionalidad es útil para:

- **Backup de datos**: Exportar todas las transacciones para tener una copia de seguridad
- **Migración**: Mover transacciones entre diferentes instalaciones
- **Análisis externo**: Exportar datos para análisis en Excel, Google Sheets u otras herramientas
- **Restauración**: Importar transacciones previamente exportadas

## Características

### ✅ Exportación
- Exporta todas las transacciones del usuario actual
- Incluye todos los campos: fecha, descripción, importe, tipo, banco, categoría, subcategoría
- Formato CSV estándar compatible con Excel y Google Sheets
- Nombre de archivo con timestamp: `transacciones_YYYYMMDD_HHMMSS.csv`

### ✅ Importación
- Importa transacciones desde archivo CSV
- **Detección automática de duplicados** usando `transaction_hash`
- Asignación automática de categorías y subcategorías si existen
- Validación de campos y formato
- Reporte detallado del resultado: importadas, duplicadas, errores

## Uso

### Exportar Transacciones

1. Ve a la página de **Transacciones**
2. Haz clic en el botón **📥 Exportar CSV**
3. El archivo se descargará automáticamente

### Importar Transacciones

1. Ve a la página de **Transacciones**
2. Haz clic en el botón **📤 Importar CSV**
3. Selecciona el archivo CSV a importar
4. Espera a que se procese el archivo
5. Verás un resumen con:
   - ✓ Transacciones importadas
   - ⊘ Duplicados omitidos
   - ✗ Errores encontrados

## Formato del CSV

### Campos del archivo

```csv
id,date,description,amount,bank_type,balance,reference,extra_info,category,subcategory,transaction_hash,created_at
1,2024-01-15T10:30:00,COMPRA MERCADONA,-45.50,imaginbank,1500.00,REF001,,Alimentación,Supermercado,abc123...,2024-01-15T10:30:00
```

### Campos requeridos para importación

Los siguientes campos son **obligatorios** para importar:
- `date`: Fecha en formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)
- `description`: Descripción de la transacción
- `amount`: Importe (negativo para gastos, positivo para ingresos)
- `bank_type`: Tipo de banco (imaginbank, kutxabank_account, kutxabank_card, openbank, etc.)

### Campos opcionales

- `balance`: Saldo después de la transacción
- `reference`: Referencia de la transacción
- `extra_info`: Información adicional
- `category`: Nombre de la categoría (debe existir previamente)
- `subcategory`: Nombre de la subcategoría (debe existir previamente)
- `transaction_hash`: Hash único para detección de duplicados (se genera automáticamente si no se proporciona)
- `id`: Se ignora en la importación
- `created_at`: Se ignora en la importación

## Detección de Duplicados

El sistema utiliza el campo `transaction_hash` para detectar duplicados:

```python
# El hash se genera a partir de:
hash_string = f"{date.date()}_{description}_{amount}_{bank_type}"
transaction_hash = md5(hash_string).hexdigest()
```

**Comportamiento:**
- Si el `transaction_hash` ya existe para el usuario → Se omite (duplicado)
- Si no existe → Se importa como nueva transacción
- Si no se proporciona el hash → Se genera automáticamente

## Ejemplos

### Ejemplo 1: Exportación completa

```bash
# Hacer clic en "Exportar CSV"
# Se descarga: transacciones_20240115_143022.csv
```

### Ejemplo 2: Importación exitosa

```
Importación completada:
✓ 150 transacciones importadas
⊘ 25 duplicados omitidos
✗ 0 errores
```

### Ejemplo 3: Importación con errores

```
Importación completada:
✓ 100 transacciones importadas
⊘ 30 duplicados omitidos
✗ 5 errores

Primeros errores:
Fila 15: Formato de fecha inválido
Fila 23: Importe inválido
Fila 45: Faltan campos requeridos
```

## Aislamiento Multi-usuario

🔒 **Importante**: Todas las operaciones están aisladas por usuario:
- Solo puedes exportar tus propias transacciones
- Las transacciones importadas se asignan automáticamente a tu usuario
- No es posible ver ni importar transacciones de otros usuarios

## API Endpoints

### GET /api/transactions/export

Exporta todas las transacciones del usuario actual.

**Respuesta:**
- Tipo: `text/csv`
- Descarga directa del archivo

**Ejemplo:**
```javascript
const response = await fetch('/api/transactions/export', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const blob = await response.blob();
// Descargar archivo...
```

### POST /api/transactions/import

Importa transacciones desde un archivo CSV.

**Request:**
- Content-Type: `multipart/form-data`
- Body: archivo CSV

**Response:**
```json
{
  "message": "Importación completada",
  "imported": 150,
  "duplicates": 25,
  "errors": 5,
  "error_details": [
    "Fila 15: Formato de fecha inválido",
    "Fila 23: Importe inválido"
  ]
}
```

## Limitaciones

1. **Tamaño de archivo**: No hay límite explícito, pero archivos muy grandes pueden tardar
2. **Categorías**: Las categorías y subcategorías deben existir previamente en el sistema
3. **Encoding**: El archivo debe estar en UTF-8
4. **Formato**: Debe ser CSV válido con encabezados en la primera fila

## Recomendaciones

✅ **Buenas prácticas:**
- Exporta regularmente como backup
- Verifica el CSV antes de importar en producción
- Revisa el reporte de importación para detectar errores
- Mantén las categorías sincronizadas entre sistemas

⚠️ **Precauciones:**
- No modifiques el `transaction_hash` si quieres evitar duplicados
- Asegúrate de que las fechas estén en formato ISO
- Verifica que las categorías existan antes de importar
- No importes el mismo archivo múltiples veces (generará duplicados si cambias los hashes)

## Casos de Uso

### Backup Mensual
```bash
1. Exportar todas las transacciones el último día del mes
2. Guardar el archivo en un lugar seguro
3. Nombre sugerido: backup_YYYY_MM.csv
```

### Migración de Sistema
```bash
1. Sistema antiguo: Exportar todas las transacciones
2. Sistema nuevo: Crear las categorías necesarias
3. Sistema nuevo: Importar el CSV exportado
4. Verificar el reporte de importación
```

### Corrección Masiva
```bash
1. Exportar transacciones
2. Modificar en Excel/Google Sheets
3. Guardar como CSV UTF-8
4. Importar de nuevo (duplicados se omitirán)
```

## Solución de Problemas

### Error: "El archivo debe ser un CSV"
- Asegúrate de que el archivo tenga extensión `.csv`

### Error: "Formato de fecha inválido"
- Las fechas deben estar en formato ISO: `2024-01-15` o `2024-01-15T10:30:00`

### Error: "Importe inválido"
- El importe debe ser un número, usa punto (.) como separador decimal

### Error: "Faltan campos requeridos"
- Verifica que el CSV tenga los campos: fecha, descripcion, importe, tipo, banco

### Muchos duplicados al importar
- Esto es normal si ya importaste esas transacciones antes
- El sistema protege contra duplicados usando el hash

## Implementación Técnica

### Backend (FastAPI)

**Exportación:**
```python
@router.get("/export")
def export_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Obtener transacciones del usuario
    # Generar CSV con writer
    # Retornar StreamingResponse
```

**Importación:**
```python
@router.post("/import")
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Leer CSV
    # Validar campos
    # Detectar duplicados por hash
    # Asignar categorías si existen
    # Crear transacciones
    # Retornar estadísticas
```

### Frontend (React)

**Exportación:**
```javascript
const handleExport = async () => {
  const response = await api.get('/api/transactions/export', {
    responseType: 'blob'
  });
  // Crear blob URL y disparar descarga
};
```

**Importación:**
```javascript
const handleImport = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const result = await api.post('/api/transactions/import', formData);
  // Mostrar resultado
};
```

## Versión

- Implementado en: v0.0.3
- Última actualización: 2024-01-15
