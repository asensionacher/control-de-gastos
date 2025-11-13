# Ejemplos de Archivos para Testing

Este directorio contiene ejemplos de archivos bancarios que puedes usar para probar la aplicación.

⚠️ **Nota**: Todos los datos en estos archivos son **ficticios** y han sido anonimizados para proteger la privacidad.

## 📄 Archivos de Ejemplo

### 1. Kutxabank - Cuenta Corriente
**Archivo**: `kutxabank_cuenta_ejemplo.xls`
- Formato: XLS/XLSX
- Transacciones de ejemplo: nóminas, transferencias, pagos de recibos
- Detección automática: ✓

### 2. Kutxabank - Tarjeta de Crédito
**Archivo**: `kutxabank_tarjeta_ejemplo.xls`
- Formato: XLS/XLSX
- Transacciones de ejemplo: compras en comercios
- Detección automática: ✓

### 3. Openbank
**Archivo**: `openbank_ejemplo.xls`
- Formato: HTML (con extensión .xls)
- Transacciones de ejemplo: transferencias, compras, pagos
- Detección automática: ✓

### 4. Imaginbank
**Archivo**: `imaginbank_ejemplo.csv`
- Formato: CSV
- Transacciones de ejemplo: transferencias, compras
- Detección automática: ✓

### 5. BBVA
**Archivo**: `bbva_ejemplo.xlsx`
- Formato: XLSX
- Transacciones de ejemplo: traspasos, programa tu cuenta
- Detección automática: ✓

### 6. ING Direct
**Archivo**: `ing_ejemplo.xls`
- Formato: XLS
- Transacciones de ejemplo: transferencias, ingresos, ventajas ING
- Detección automática: ✓

## 🔧 Cómo usar estos archivos

1. Ve a la sección "Subir Extracto Bancario" en la aplicación
2. Selecciona cualquiera de estos archivos de ejemplo
3. La aplicación detectará automáticamente el banco (o puedes seleccionarlo manualmente)
4. Haz clic en "Subir Archivo" para importar las transacciones

## 📊 Datos de Ejemplo

Todos los archivos contienen **datos ficticios** incluyendo:
- Descripciones genéricas (sin nombres reales de comercios específicos)
- Cantidades aleatorias
- Fechas recientes para pruebas
- Sin información personal identificable

## ⚠️ Nota Importante

Estos son solo ejemplos con **datos completamente ficticios**. Los formatos reales de tu banco pueden variar ligeramente. La aplicación está diseñada para ser flexible y adaptarse a pequeñas variaciones en el formato.

Si encuentras problemas al importar tus archivos reales, verifica:
- El separador de campos (`;` es el más común en España)
- El formato de decimales (`,` para decimal en formato español)
- El formato de fecha (DD/MM/YYYY)
- La codificación del archivo (UTF-8 o ISO-8859-1)
