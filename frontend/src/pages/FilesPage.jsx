/**
 * FilesPage Component
 * File management page (Admin only)
 */
import React, { useState, useEffect, useCallback } from 'react';
import { Row, Col, Card, Modal, Form, Button, Alert } from 'react-bootstrap';
import MainLayout from '../components/layout/MainLayout';
import FileUpload from '../components/files/FileUpload';
import FileList from '../components/files/FileList';
import FilePreview from '../components/files/FilePreview';
import fileService from '../services/fileService';
import reportService from '../services/reportService';

function FilesPage() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [previewFile, setPreviewFile] = useState(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  // Report generation modal
  const [showReportModal, setShowReportModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [reportTitle, setReportTitle] = useState('');
  const [generating, setGenerating] = useState(false);
  const [reportError, setReportError] = useState('');
  const [reportSuccess, setReportSuccess] = useState('');

  const loadFiles = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fileService.listFiles();
      setFiles(data);
    } catch (err) {
      console.error('Error loading files:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const handleUploadSuccess = (file) => {
    loadFiles();
  };

  const handlePreview = async (fileId) => {
    setPreviewLoading(true);
    setShowPreview(true);
    try {
      const preview = await fileService.getFilePreview(fileId);
      setPreviewFile(preview);
    } catch (err) {
      console.error('Error loading preview:', err);
    } finally {
      setPreviewLoading(false);
    }
  };

  const handleDelete = async (fileId) => {
    if (window.confirm('¿Eliminar este archivo? Esta accion no se puede deshacer.')) {
      try {
        await fileService.deleteFile(fileId);
        loadFiles();
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al eliminar archivo');
      }
    }
  };

  const handleGenerateReport = (file) => {
    setSelectedFile(file);
    setReportTitle(`Reporte ${file.detected_model} - ${new Date().toLocaleDateString()}`);
    setReportError('');
    setReportSuccess('');
    setShowReportModal(true);
  };

  const submitGenerateReport = async (e) => {
    e.preventDefault();
    if (!selectedFile || !reportTitle) return;

    setGenerating(true);
    setReportError('');

    try {
      await reportService.generateReport(reportTitle, selectedFile.id);
      setReportSuccess('Reporte generado exitosamente. Puede verlo en la seccion de Reportes.');
      setShowReportModal(false);
      setTimeout(() => setReportSuccess(''), 5000);
    } catch (err) {
      setReportError(err.response?.data?.detail || 'Error al generar reporte');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <MainLayout title="Gestion de Archivos">
      {reportSuccess && (
        <Alert variant="success" dismissible onClose={() => setReportSuccess('')}>
          {reportSuccess}
        </Alert>
      )}

      <Row className="g-3">
        <Col lg={4} className="order-lg-1 order-2">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </Col>
        <Col lg={8} className="order-lg-2 order-1">
          <Card className="shadow-sm">
            <Card.Body className="p-2 p-md-3">
              <h5 className="mb-3">Archivos Subidos</h5>
              <FileList
                files={files}
                loading={loading}
                onPreview={handlePreview}
                onDelete={handleDelete}
                onGenerateReport={handleGenerateReport}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* File Preview Modal */}
      <FilePreview
        show={showPreview}
        onHide={() => setShowPreview(false)}
        preview={previewFile}
        loading={previewLoading}
      />

      {/* Generate Report Modal */}
      <Modal show={showReportModal} onHide={() => setShowReportModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Generar Reporte</Modal.Title>
        </Modal.Header>
        <Form onSubmit={submitGenerateReport}>
          <Modal.Body>
            {reportError && <Alert variant="danger">{reportError}</Alert>}

            <p className="text-muted">
              Se ejecutaran predicciones sobre el archivo{' '}
              <strong>{selectedFile?.original_filename}</strong> usando el modelo{' '}
              <strong>{selectedFile?.detected_model}</strong>.
            </p>

            <Form.Group className="mb-3">
              <Form.Label>Titulo del Reporte</Form.Label>
              <Form.Control
                type="text"
                value={reportTitle}
                onChange={(e) => setReportTitle(e.target.value)}
                placeholder="Ingrese un titulo descriptivo"
                required
              />
            </Form.Group>

            <Alert variant="info">
              <small>
                <strong>Nota:</strong> Este proceso puede tomar varios minutos
                dependiendo del tamaño del archivo ({selectedFile?.row_count?.toLocaleString()} registros).
              </small>
            </Alert>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowReportModal(false)}>
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={generating}
            >
              {generating ? 'Generando...' : 'Generar Reporte'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </MainLayout>
  );
}

export default FilesPage;
