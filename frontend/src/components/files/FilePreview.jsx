/**
 * FilePreview Component
 * Modal to preview file contents
 */
import React from 'react';
import { Modal, Table, Badge, Spinner } from 'react-bootstrap';

function FilePreview({ show, onHide, preview, loading }) {
  const getModelBadge = (modelType) => {
    const badges = {
      phishing: <Badge bg="info">Phishing</Badge>,
      ato: <Badge bg="warning" text="dark">Account Takeover</Badge>,
      brute_force: <Badge bg="danger">Brute Force</Badge>
    };
    return badges[modelType] || <Badge bg="secondary">No detectado</Badge>;
  };

  return (
    <Modal show={show} onHide={onHide} size="xl" centered>
      <Modal.Header closeButton>
        <Modal.Title>
          Vista Previa: {preview?.filename || 'Cargando...'}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {loading ? (
          <div className="text-center py-5">
            <Spinner animation="border" variant="primary" />
            <p className="mt-2 text-muted">Cargando vista previa...</p>
          </div>
        ) : preview ? (
          <>
            <div className="mb-3 d-flex gap-3 align-items-center">
              <div>
                <strong>Registros:</strong> {preview.row_count?.toLocaleString()}
              </div>
              <div>
                <strong>Columnas:</strong> {preview.columns?.length}
              </div>
              <div>
                <strong>Modelo:</strong> {getModelBadge(preview.detected_model)}
              </div>
            </div>

            <div className="mb-3">
              <strong>Columnas detectadas:</strong>
              <div className="mt-1">
                {preview.columns?.map((col, idx) => (
                  <Badge key={idx} bg="light" text="dark" className="me-1 mb-1">
                    {col}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="table-responsive" style={{ maxHeight: '400px', overflow: 'auto' }}>
              <Table striped bordered hover size="sm">
                <thead className="sticky-top bg-light">
                  <tr>
                    <th>#</th>
                    {preview.columns?.map((col, idx) => (
                      <th key={idx} style={{ whiteSpace: 'nowrap' }}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {preview.preview_rows?.map((row, rowIdx) => (
                    <tr key={rowIdx}>
                      <td>{rowIdx + 1}</td>
                      {preview.columns?.map((col, colIdx) => (
                        <td
                          key={colIdx}
                          style={{
                            maxWidth: '200px',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap'
                          }}
                          title={String(row[col] ?? '')}
                        >
                          {String(row[col] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>

            <small className="text-muted">
              Mostrando las primeras {preview.preview_rows?.length} filas de {preview.row_count?.toLocaleString()} totales
            </small>
          </>
        ) : (
          <p className="text-muted">No hay datos disponibles</p>
        )}
      </Modal.Body>
    </Modal>
  );
}

export default FilePreview;
