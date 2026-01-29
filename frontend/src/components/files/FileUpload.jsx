/**
 * FileUpload Component
 * File upload with drag and drop support
 */
import React, { useState, useRef } from 'react';
import { Card, Button, Alert, ProgressBar, Badge } from 'react-bootstrap';
import { FaCloudUploadAlt, FaFileExcel, FaFileCsv, FaTimes } from 'react-icons/fa';
import fileService from '../../services/fileService';

function FileUpload({ onUploadSuccess }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const inputRef = useRef(null);

  const allowedTypes = [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ];

  const allowedExtensions = ['.csv', '.xls', '.xlsx'];

  const validateFile = (file) => {
    const extension = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedExtensions.includes(extension)) {
      return 'Tipo de archivo no permitido. Use CSV o Excel.';
    }
    if (file.size > 50 * 1024 * 1024) {
      return 'El archivo excede el limite de 50MB.';
    }
    return null;
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setError('');

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const validationError = validateFile(file);
      if (validationError) {
        setError(validationError);
      } else {
        setSelectedFile(file);
      }
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    setError('');

    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const validationError = validateFile(file);
      if (validationError) {
        setError(validationError);
      } else {
        setSelectedFile(file);
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploadProgress(0);
    setError('');
    setSuccess('');

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const result = await fileService.uploadFile(selectedFile);

      clearInterval(progressInterval);
      setUploadProgress(100);

      setSuccess(`Archivo "${result.original_filename}" subido exitosamente. Modelo detectado: ${result.detected_model || 'No detectado'}`);
      setSelectedFile(null);

      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al subir el archivo');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setError('');
    setSuccess('');
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  const getFileIcon = () => {
    if (!selectedFile) return <FaCloudUploadAlt size={48} className="text-primary" />;
    const ext = selectedFile.name.split('.').pop().toLowerCase();
    if (ext === 'csv') return <FaFileCsv size={48} className="text-success" />;
    return <FaFileExcel size={48} className="text-success" />;
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <Card className="shadow-sm">
      <Card.Body>
        <h5 className="mb-3">Subir Archivo</h5>

        {error && (
          <Alert variant="danger" dismissible onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert variant="success" dismissible onClose={() => setSuccess('')}>
            {success}
          </Alert>
        )}

        <div
          className={`border rounded p-5 text-center ${
            dragActive ? 'border-primary bg-light' : 'border-dashed'
          }`}
          style={{
            borderStyle: 'dashed',
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".csv,.xls,.xlsx"
            onChange={handleChange}
            style={{ display: 'none' }}
          />

          {getFileIcon()}

          {selectedFile ? (
            <div className="mt-3">
              <p className="fw-semibold mb-1">{selectedFile.name}</p>
              <small className="text-muted">{formatFileSize(selectedFile.size)}</small>
              <Button
                variant="link"
                size="sm"
                className="text-danger p-0 ms-2"
                onClick={(e) => {
                  e.stopPropagation();
                  handleClear();
                }}
              >
                <FaTimes />
              </Button>
            </div>
          ) : (
            <div className="mt-3">
              <p className="mb-1">
                <strong>Arrastre un archivo aqui</strong> o haga clic para seleccionar
              </p>
              <small className="text-muted">
                Formatos permitidos: CSV, Excel (.xls, .xlsx) - Max 50MB
              </small>
            </div>
          )}
        </div>

        {uploading && (
          <ProgressBar
            animated
            now={uploadProgress}
            className="mt-3"
            label={`${uploadProgress}%`}
          />
        )}

        <div className="mt-3 d-flex gap-2">
          <Button
            variant="primary"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading ? 'Subiendo...' : 'Subir Archivo'}
          </Button>

          {selectedFile && (
            <Button variant="outline-secondary" onClick={handleClear} disabled={uploading}>
              Cancelar
            </Button>
          )}
        </div>

        <div className="mt-3">
          <small className="text-muted">
            <strong>Columnas requeridas por modelo:</strong>
            <br />
            <Badge bg="info" className="me-1">Phishing</Badge> sender, subject, body
            <br />
            <Badge bg="warning" className="me-1">ATO</Badge> user_id, ip_address, country
            <br />
            <Badge bg="danger" className="me-1">Brute Force</Badge> dst_port, protocol, flow_duration
          </small>
        </div>
      </Card.Body>
    </Card>
  );
}

export default FileUpload;
