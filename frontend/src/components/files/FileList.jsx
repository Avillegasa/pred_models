/**
 * FileList Component
 * Display list of uploaded files with actions
 */
import React from 'react';
import { Table, Button, Badge, Spinner } from 'react-bootstrap';
import { FaEye, FaTrash, FaPlayCircle, FaFileAlt } from 'react-icons/fa';

function FileList({ files, loading, onPreview, onDelete, onGenerateReport }) {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getModelBadge = (modelType) => {
    const badges = {
      phishing: <Badge bg="info">Phishing</Badge>,
      ato: <Badge bg="warning" text="dark">ATO</Badge>,
      brute_force: <Badge bg="danger">Brute Force</Badge>
    };
    return badges[modelType] || <Badge bg="secondary">No detectado</Badge>;
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2 text-muted">Cargando archivos...</p>
      </div>
    );
  }

  if (!files || files.length === 0) {
    return (
      <div className="text-center py-5 text-muted">
        <FaFileAlt size={48} className="mb-3 opacity-50" />
        <p>No hay archivos subidos</p>
      </div>
    );
  }

  return (
    <Table responsive hover className="align-middle">
      <thead className="bg-light">
        <tr>
          <th>Archivo</th>
          <th>Modelo Detectado</th>
          <th>Registros</th>
          <th>Fecha</th>
          <th className="text-end">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {files.map((file) => (
          <tr key={file.id}>
            <td>
              <div className="fw-semibold">{file.original_filename}</div>
              <small className="text-muted">{file.columns?.length || 0} columnas</small>
            </td>
            <td>{getModelBadge(file.detected_model)}</td>
            <td>{file.row_count?.toLocaleString()}</td>
            <td>
              <small>{formatDate(file.uploaded_at)}</small>
            </td>
            <td className="text-end">
              <Button
                variant="outline-primary"
                size="sm"
                className="me-1"
                onClick={() => onPreview(file.id)}
                title="Vista previa"
              >
                <FaEye />
              </Button>
              <Button
                variant="outline-success"
                size="sm"
                className="me-1"
                onClick={() => onGenerateReport(file)}
                disabled={!file.detected_model}
                title="Generar reporte"
              >
                <FaPlayCircle />
              </Button>
              <Button
                variant="outline-danger"
                size="sm"
                onClick={() => onDelete(file.id)}
                title="Eliminar"
              >
                <FaTrash />
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

export default FileList;
