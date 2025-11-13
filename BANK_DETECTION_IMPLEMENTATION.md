# Detección de Banco y Mejora de Carga de Archivos

## Resumen

He implementado con éxito la detección automática de banco y mejorado el soporte de formatos de archivo para la aplicación de control de gastos. El sistema ahora puede:

1. **Auto-detectar** el tipo de banco de los archivos subidos (CSV, XLS, HTML)
2. Permitir **selección manual** si la auto-detección falla
3. Soportar **múltiples formatos de archivo**: CSV, XLS (Excel binario), y HTML

## Cambios Realizados

### Cambios en Backend

#### 1. **Dependencias Actualizadas** (`backend/requirements.txt`)
Añadido soporte para parseo de Excel y HTML:
- `xlrd==2.0.1` - Para leer archivos XLS antiguos de Excel
- `openpyxl==3.1.2` - Para leer archivos Excel modernos
- `lxml==4.9.3` - Para parsear archivos HTML

#### 2. **Nuevo Módulo Detector de Bancos** (`backend/bank_detector.py`)
Creado un sistema completo de detección de bancos:
- Analiza el contenido del archivo para identificar el banco automáticamente
- Detecta el formato del archivo (CSV, HTML, XLS binario)
- Identifica patrones específicos para cada banco:
  - **Imaginbank**: CSV con sufijo "EUR" en las cantidades
  - **Openbank**: Archivo HTML disfrazado de XLS
  - **Kutxabank**: Archivos XLS binarios (diferencia entre cuenta y tarjeta)
- Proporciona un respaldo basado en detección por nombre de archivo

#### 3. **Parsers Actualizados** (`backend/parsers.py`)
Mejorados todos los parsers para manejar formatos de archivo reales:

- **ImaginbankParser**: 
  - Maneja formato CSV con sufijo EUR (ej: "-217,98EUR")
  - Orden de columnas: Concepto, Fecha, Importe, Saldo

- **OpenbankParser**:
  - Parsea tablas HTML (Openbank exporta HTML con extensión .xls)
  - Respaldo a parseo CSV si es necesario
  - Extrae: Fecha Operación, Fecha Valor, Concepto, Importe, Saldo

- **KutxabankAccountParser** & **KutxabankCardParser**:
  - Lee archivos XLS binarios con motor xlrd
  - Encuentra dinámicamente la fila de encabezado en el archivo
  - Omite filas de metadatos
  - Maneja datos numéricos correctamente (no necesita conversión a string)

#### 4. **Actualizaciones del Endpoint de Carga** (`backend/routes/upload.py`)
- Hecho `bank_type` opcional en el endpoint de carga
- Auto-detecta el banco si no se proporciona
- Añadido nuevo endpoint `/detect-bank` para detección previa a la carga
- Actualizado endpoint `/bank-types` para usar BankDetector
- Mejorados los mensajes de error con el nombre del banco detectado

### Cambios en Frontend

#### 1. **UI de Carga Mejorada** (`frontend/src/pages/Upload.js`)
Añadida interfaz de carga inteligente:
- **Toggle para auto-detección**: Los usuarios pueden elegir entre modo automático y manual
- **Detección de banco en tiempo real**: Muestra el banco detectado inmediatamente después de seleccionar el archivo
- **Anulación manual**: Si la detección falla, los usuarios pueden seleccionar el banco manualmente
- **Mejor aceptación de archivos**: Acepta archivos .csv, .xls, .xlsx
- **Retroalimentación visual**: 
  - Muestra progreso de detección
  - Muestra el nombre del banco detectado
  - Proporciona mensajes de error útiles
- **Sección de información actualizada**: Explica las nuevas funcionalidades

#### 2. **Actualizaciones del Servicio API** (`frontend/src/services/api.js`)
- Hecho parámetro `bank_type` opcional en `uploadCSV`
- Añadida nueva función `detectBank` para detección previa a la carga

## Bancos y Formatos Soportados

| Banco | Formato | Tipo de Archivo | Características |
|------|--------|-----------|----------|
| **Imaginbank** | CSV | `.csv` | Sufijo EUR en cantidades, separador punto y coma |
| **Kutxabank - Cuenta** | XLS Binario | `.xls` | Formato Excel antiguo, detección de encabezado |
| **Kutxabank - Tarjeta** | XLS Binario | `.xls` | Formato Excel antiguo, detección de encabezado |
| **Openbank** | HTML | `.xls` | Tabla HTML disfrazada de XLS |

## Pruebas

Todos los archivos de ejemplo han sido probados y parsean correctamente:
- ✅ `imaginbank_ejemplo.csv` - 6 transacciones
- ✅ `kutxabank_cuenta_ejemplo.xls` - 26 transacciones  
- ✅ `kutxabank_tarjeta_ejemplo.xls` - 26 transacciones
- ✅ `openbank_ejemplo.xls` - 11 transacciones

## Flujo de Experiencia de Usuario

### Modo Automático (Por defecto)
1. El usuario selecciona un archivo
2. El sistema detecta el banco automáticamente
3. Muestra el nombre del banco detectado
4. El usuario hace clic en "Subir Archivo"
5. Las transacciones se importan

### Modo Manual
1. El usuario desmarca "Detectar banco automáticamente"
2. El usuario selecciona el banco del desplegable
3. El usuario selecciona el archivo
4. El usuario hace clic en "Subir Archivo"
5. Las transacciones se importan

### Flujo de Respaldo
1. El usuario sube un archivo en modo automático
2. La detección falla
3. El sistema sugiere selección manual
4. El usuario hace clic en el enlace de sugerencia
5. Cambia a modo manual automáticamente
6. El usuario selecciona el banco y completa la carga

## Detalles Técnicos

### Lógica de Detección de Banco
1. **Detección de Formato de Archivo**: Verificación de firma binaria (HTML, XLS)
2. **Análisis de Contenido**: Búsqueda de patrones específicos del banco
3. **Análisis de Encabezado**: Nombres de columnas y estructura
4. **Respaldo por Nombre de Archivo**: Nombre del banco en el nombre del archivo

### Arquitectura de Parsers
- Clase base con funcionalidad común (detección de codificación, generación de hash)
- Parsers especializados para cada banco
- Manejo robusto de errores
- Detección flexible de columnas (maneja variaciones de formato)

## Mejoras Futuras
- Añadir más bancos según sea necesario
- Machine learning para mejor detección
- Soporte para extractos en PDF
- Carga masiva de archivos
- Mostrar puntuación de confianza de la detección

