/**
 * PDFGenerator Component
 * Generates PDF report with logo, metrics, and charts
 */
import React, { useState } from 'react';
import { Button, Spinner } from 'react-bootstrap';
import { FaFilePdf, FaDownload } from 'react-icons/fa';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import dayjs from 'dayjs';

function PDFGenerator({ report, chartsRef }) {
  const [generating, setGenerating] = useState(false);

  const generatePDF = async () => {
    setGenerating(true);

    try {
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 15;
      let yPos = margin;

      // Load and add logo
      try {
        const logoImg = new Image();
        logoImg.crossOrigin = 'anonymous';
        await new Promise((resolve, reject) => {
          logoImg.onload = resolve;
          logoImg.onerror = reject;
          logoImg.src = '/logo-bcp.png';
        });
        pdf.addImage(logoImg, 'PNG', margin, yPos, 40, 15);
      } catch (e) {
        console.warn('Could not load logo:', e);
      }

      // Header
      pdf.setFontSize(18);
      pdf.setFont('helvetica', 'bold');
      pdf.text('Reporte Mensual de Ciberseguridad', pageWidth / 2, yPos + 8, { align: 'center' });

      yPos += 20;

      // Period info
      pdf.setFontSize(11);
      pdf.setFont('helvetica', 'normal');
      pdf.setTextColor(100, 100, 100);
      pdf.text(
        `${report.month_name} ${report.year} - La Paz, Bolivia (UTC-4)`,
        pageWidth / 2,
        yPos,
        { align: 'center' }
      );
      pdf.text(
        `Generado: ${dayjs().format('DD/MM/YYYY HH:mm')}`,
        pageWidth / 2,
        yPos + 5,
        { align: 'center' }
      );

      yPos += 15;

      // Horizontal line
      pdf.setDrawColor(0, 75, 142);
      pdf.setLineWidth(0.5);
      pdf.line(margin, yPos, pageWidth - margin, yPos);

      yPos += 10;

      // Executive Summary Section
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(0, 75, 142);
      pdf.text('Resumen Ejecutivo', margin, yPos);
      yPos += 8;

      // Summary metrics in a table-like format
      pdf.setFontSize(10);
      pdf.setFont('helvetica', 'normal');
      pdf.setTextColor(50, 50, 50);

      const summaryData = [
        ['Total Predicciones:', report.summary.total_predictions.toLocaleString()],
        ['Amenazas Detectadas:', `${report.summary.threats_detected.toLocaleString()} (${report.summary.threat_rate_percent.toFixed(1)}%)`],
        ['Trafico Legitimo:', `${report.summary.benign_count.toLocaleString()} (${(100 - report.summary.threat_rate_percent).toFixed(1)}%)`],
        ['Confianza Promedio:', `${report.summary.avg_confidence.toFixed(1)}%`],
      ];

      summaryData.forEach((row, idx) => {
        pdf.setFont('helvetica', 'bold');
        pdf.text(row[0], margin, yPos + idx * 6);
        pdf.setFont('helvetica', 'normal');
        pdf.text(row[1], margin + 45, yPos + idx * 6);
      });

      yPos += 30;

      // Model Breakdown Section
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(0, 75, 142);
      pdf.text('Desglose por Modelo', margin, yPos);
      yPos += 8;

      pdf.setFontSize(10);
      pdf.setTextColor(50, 50, 50);

      const modelLabels = {
        phishing: 'Phishing',
        ato: 'Account Takeover',
        brute_force: 'Fuerza Bruta',
      };

      Object.entries(report.by_model).forEach(([model, data], idx) => {
        pdf.setFont('helvetica', 'bold');
        pdf.text(`${modelLabels[model] || model}:`, margin, yPos + idx * 6);
        pdf.setFont('helvetica', 'normal');
        pdf.text(
          `${data.total} total | ${data.threats} amenazas | ${data.benign} legitimos | ${data.avg_confidence.toFixed(1)}% confianza`,
          margin + 40,
          yPos + idx * 6
        );
      });

      yPos += 25;

      // Alerts Section
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(0, 75, 142);
      pdf.text('Alertas del Mes', margin, yPos);
      yPos += 8;

      pdf.setFontSize(10);
      pdf.setTextColor(50, 50, 50);
      pdf.setFont('helvetica', 'normal');
      pdf.text(`Total: ${report.alerts.total}`, margin, yPos);
      pdf.text(
        `Criticas: ${report.alerts.by_severity.critical} | Altas: ${report.alerts.by_severity.high} | Medias: ${report.alerts.by_severity.medium}`,
        margin + 30,
        yPos
      );
      yPos += 6;
      pdf.text(
        `Sin leer: ${report.alerts.by_status.unread} | Leidas: ${report.alerts.by_status.read} | Resueltas: ${report.alerts.by_status.acknowledged}`,
        margin,
        yPos
      );

      yPos += 15;

      // Capture charts if available
      if (chartsRef?.current) {
        try {
          const canvas = await html2canvas(chartsRef.current, {
            scale: 2,
            useCORS: true,
            logging: false,
            backgroundColor: '#ffffff',
          });

          const imgData = canvas.toDataURL('image/png');
          const imgWidth = pageWidth - margin * 2;
          const imgHeight = (canvas.height * imgWidth) / canvas.width;

          // Check if we need a new page
          if (yPos + imgHeight > pageHeight - margin) {
            pdf.addPage();
            yPos = margin;
          }

          pdf.setFontSize(14);
          pdf.setFont('helvetica', 'bold');
          pdf.setTextColor(0, 75, 142);
          pdf.text('Graficos y Tendencias', margin, yPos);
          yPos += 8;

          pdf.addImage(imgData, 'PNG', margin, yPos, imgWidth, imgHeight);
          yPos += imgHeight + 10;
        } catch (e) {
          console.warn('Could not capture charts:', e);
        }
      }

      // Top Threats Section (new page if needed)
      if (report.top_threats && report.top_threats.length > 0) {
        if (yPos > pageHeight - 80) {
          pdf.addPage();
          yPos = margin;
        }

        pdf.setFontSize(14);
        pdf.setFont('helvetica', 'bold');
        pdf.setTextColor(0, 75, 142);
        pdf.text('Top 10 Amenazas Detectadas', margin, yPos);
        yPos += 8;

        pdf.setFontSize(9);
        pdf.setTextColor(50, 50, 50);

        report.top_threats.slice(0, 10).forEach((threat, idx) => {
          if (yPos > pageHeight - 20) {
            pdf.addPage();
            yPos = margin;
          }

          pdf.setFont('helvetica', 'bold');
          pdf.text(`${idx + 1}.`, margin, yPos);
          pdf.setFont('helvetica', 'normal');
          pdf.text(
            `${modelLabels[threat.model_type] || threat.model_type} - ${threat.prediction_label} - ${threat.confidence.toFixed(1)}%`,
            margin + 8,
            yPos
          );
          yPos += 5;
        });
      }

      // Footer on last page
      pdf.setFontSize(8);
      pdf.setTextColor(150, 150, 150);
      pdf.text(
        'Sistema de Deteccion de Incidentes de Ciberseguridad - BCP Bolivia',
        pageWidth / 2,
        pageHeight - 10,
        { align: 'center' }
      );

      // Save PDF
      const fileName = `reporte_mensual_${report.year}_${String(report.month).padStart(2, '0')}.pdf`;
      pdf.save(fileName);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error al generar el PDF. Por favor intente nuevamente.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <Button
      variant="primary"
      onClick={generatePDF}
      disabled={generating || !report}
      className="d-flex align-items-center gap-2"
    >
      {generating ? (
        <>
          <Spinner animation="border" size="sm" />
          <span>Generando...</span>
        </>
      ) : (
        <>
          <FaFilePdf />
          <span>Descargar PDF</span>
          <FaDownload size={12} />
        </>
      )}
    </Button>
  );
}

export default PDFGenerator;
