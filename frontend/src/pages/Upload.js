import React, { useState, useEffect } from 'react';
import { uploadCSV, getBankTypes, detectBank } from '../services/api';

function Upload() {
  const [bankTypes, setBankTypes] = useState([]);
  const [selectedBank, setSelectedBank] = useState('');
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [detecting, setDetecting] = useState(false);
  const [detectedBanks, setDetectedBanks] = useState({});
  const [result, setResult] = useState(null);
  const [useAutoDetect, setUseAutoDetect] = useState(true);

  useEffect(() => {
    loadBankTypes();
  }, []);

  const loadBankTypes = async () => {
    try {
      const response = await getBankTypes();
      setBankTypes(response.data.bank_types);
    } catch (error) {
      console.error('Error cargando tipos de banco:', error);
    }
  };

  const handleFileChange = async (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
      setFiles(selectedFiles);
      setResult(null);
      setDetectedBanks({});

      // Intentar detectar automáticamente el banco de cada archivo
      if (useAutoDetect) {
        setDetecting(true);
        const detections = {};

        for (const file of selectedFiles) {
          try {
            const response = await detectBank(file);
            detections[file.name] = response.data;
          } catch (error) {
            console.error(`Error detectando banco para ${file.name}:`, error);
            detections[file.name] = { success: false };
          }
        }

        setDetectedBanks(detections);
        setDetecting(false);
      }
    } else {
      e.target.value = '';
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (files.length === 0) {
      alert('Por favor selecciona al menos un archivo');
      return;
    }

    // Si no hay banco seleccionado y no está en modo auto-detección, pedir selección manual
    if (!selectedBank && !useAutoDetect) {
      alert('Por favor selecciona un banco');
      return;
    }

    setUploading(true);
    setResult(null);

    try {
      // Si está en modo manual, enviar el banco seleccionado
      const bankToUse = useAutoDetect ? null : selectedBank;
      const response = await uploadCSV(files, bankToUse);
      setResult(response.data);
      setFiles([]);
      setDetectedBanks({});
      setSelectedBank('');

      // Reset file input
      document.getElementById('file-input').value = '';
    } catch (error) {
      console.error('Error subiendo archivos:', error);
      setResult({
        success: false,
        message: error.response?.data?.detail || 'Error al subir los archivos'
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Subir Extracto Bancario</h1>
        <p className="page-subtitle">Importa extractos bancarios en CSV o XLS</p>
      </div>

      <div className="card">
        <form onSubmit={handleUpload}>
          {/* Toggle de detección automática */}
          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={useAutoDetect}
                onChange={(e) => {
                  setUseAutoDetect(e.target.checked);
                  setDetectedBanks({});
                  if (!e.target.checked) {
                    setSelectedBank('');
                  }
                }}
                style={{ marginRight: '0.5rem' }}
              />
              <span>Detectar banco automáticamente</span>
            </label>
            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#a8a8a8' }}>
              {useAutoDetect
                ? 'El sistema intentará identificar el banco al subir el archivo'
                : 'Selecciona manualmente el banco antes de subir'}
            </p>
          </div>

          {/* Selector manual de banco */}
          {!useAutoDetect && (
            <div className="form-group">
              <label className="form-label">Banco *</label>
              <select
                className="form-control"
                value={selectedBank}
                onChange={(e) => setSelectedBank(e.target.value)}
                required={!useAutoDetect}
              >
                <option value="">Selecciona un banco</option>
                {bankTypes.map(bank => (
                  <option key={bank.id} value={bank.id}>
                    {bank.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Selector de archivos múltiples */}
          <div className="form-group">
            <label className="form-label">Archivos (CSV, XLS) *</label>
            <input
              id="file-input"
              type="file"
              className="form-control"
              accept=".csv,.xls,.xlsx"
              onChange={handleFileChange}
              multiple
              required
            />

            {/* Indicador de detección */}
            {detecting && (
              <p style={{ marginTop: '0.5rem', color: '#00d9a3' }}>
                🔍 Detectando bancos...
              </p>
            )}

            {/* Lista de archivos seleccionados con detección */}
            {files.length > 0 && !detecting && (
              <div style={{ marginTop: '1rem' }}>
                <p style={{ color: '#e8e8e8', marginBottom: '0.5rem' }}>
                  <strong>Archivos seleccionados ({files.length}):</strong>
                </p>
                <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                  {files.map((file, index) => {
                    const detection = detectedBanks[file.name];
                    return (
                      <li
                        key={index}
                        style={{
                          marginBottom: '0.5rem',
                          padding: '0.5rem',
                          background: '#1a1a1a',
                          borderRadius: '4px',
                          border: '1px solid #333'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span style={{ color: '#a8a8a8' }}>📄 {file.name}</span>
                          {detection && (
                            <span style={{
                              color: detection.success ? '#00d9a3' : '#ff9f1c',
                              fontSize: '0.9rem'
                            }}>
                              {detection.success
                                ? `✓ ${detection.bank_name}`
                                : '⚠️ No detectado'}
                            </span>
                          )}
                        </div>
                      </li>
                    );
                  })}
                </ul>

                {/* Advertencia si algún archivo no se detectó */}
                {useAutoDetect && Object.values(detectedBanks).some(d => !d.success) && (
                  <p style={{ color: '#ff9f1c', marginTop: '0.5rem' }}>
                    ⚠️ Algunos archivos no se pudieron detectar.
                    <br />
                    <span
                      style={{ cursor: 'pointer', textDecoration: 'underline', marginTop: '0.25rem', display: 'inline-block' }}
                      onClick={() => {
                        setUseAutoDetect(false);
                        setDetectedBanks({});
                      }}
                    >
                      Haz clic aquí para seleccionar el banco manualmente
                    </span>
                  </p>
                )}
              </div>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={uploading || files.length === 0 || detecting || (!useAutoDetect && !selectedBank)}
          >
            {uploading ? 'Subiendo...' : `Subir ${files.length > 0 ? files.length : ''} Archivo${files.length !== 1 ? 's' : ''}`}
          </button>
        </form>
      </div>

      {/* Resultado */}
      {result && (
        <div className={`alert ${result.success ? 'alert-success' : 'alert-error'}`}>
          <h3 style={{ marginBottom: '1rem' }}>
            {result.success ? '✓ Importación Completada' : '✗ Error en la Importación'}
          </h3>
          <pre style={{
            whiteSpace: 'pre-wrap',
            fontFamily: 'inherit',
            margin: 0,
            lineHeight: '1.6'
          }}>
            {result.message}
          </pre>

          {result.success && (
            <div style={{
              marginTop: '1rem',
              paddingTop: '1rem',
              borderTop: '1px solid rgba(255,255,255,0.1)'
            }}>
              <p><strong>Total de filas:</strong> {result.total_rows}</p>
              <p><strong>Importadas:</strong> {result.imported}</p>
              <p><strong>Duplicadas:</strong> {result.duplicates}</p>
              {result.errors > 0 && (
                <p style={{ color: '#ff9f1c' }}>
                  <strong>Errores:</strong> {result.errors}
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Información */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">ℹ️ Información</h2>
        </div>
        <div style={{ color: '#a8a8a8' }}>
          <h3 style={{ color: '#e8e8e8', marginBottom: '1rem' }}>
            Cómo funciona
          </h3>
          <p style={{ marginBottom: '1rem' }}>
            Descarga el extracto bancario desde tu entidad y súbelo aquí.
            El sistema puede detectar automáticamente el formato o puedes seleccionarlo manualmente.
          </p>

          <h4 style={{ color: '#e8e8e8', marginTop: '1.5rem', marginBottom: '0.5rem' }}>
            Bancos soportados:
          </h4>
          <ul style={{ paddingLeft: '1.5rem' }}>
            <li><strong>Kutxabank</strong> - Cuenta Corriente (XLS)</li>
            <li><strong>Kutxabank</strong> - Tarjeta de Crédito (XLS)</li>
            <li><strong>Openbank</strong> - Exportación HTML/XLS</li>
            <li><strong>Imaginbank</strong> - CSV</li>
            <li><strong>BBVA</strong> - Exportación XLSX</li>
            <li><strong>ING Direct</strong> - Exportación XLS</li>
          </ul>

          <h4 style={{ color: '#e8e8e8', marginTop: '1.5rem', marginBottom: '0.5rem' }}>
            Características:
          </h4>
          <ul style={{ paddingLeft: '1.5rem' }}>
            <li>✓ Carga múltiple de archivos</li>
            <li>✓ Detección automática del banco y formato</li>
            <li>✓ Soporte para CSV, XLS, XLSX y HTML</li>
            <li>✓ Detección automática de duplicados</li>
            <li>✓ Auto-categorización basada en historial</li>
            <li>✓ Validación de datos</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Upload;
