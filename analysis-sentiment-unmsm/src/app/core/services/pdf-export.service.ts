/**
 * Servicio mejorado para exportar reportes a PDF
 * Usa captura de pantalla para PDF idéntico a lo que se ve
 * Ubicación: src/app/core/services/pdf-export.service.ts
 */

import { Injectable } from '@angular/core';

declare var html2pdf: any;

@Injectable({
  providedIn: 'root'
})
export class PdfExportService {

  constructor() {}

  /**
   * Exportar como captura de pantalla a PDF (RECOMENDADO)
   * Captura exactamente lo que ves en pantalla - FULL SIZE
   */
  async exportWithValidation(
    element: HTMLElement,
    filename: string = 'reporte-unmsm.pdf',
    options?: {
      addHeader?: boolean;
      headerText?: string;
      logoUrl?: string;
      addFooter?: boolean;
      optimizeImages?: boolean;
      reportType?: 'sentimientos' | 'satisfaccion' | 'mensual' | 'anual';
    }
  ): Promise<void> {
    
    if (typeof html2pdf === 'undefined') {
      console.error('❌ html2pdf no está cargado');
      throw new Error('La librería html2pdf no está disponible');
    }

    try {
      console.log('📸 Capturando reporte completo como imagen...');

      // Clonar elemento
      const clone = element.cloneNode(true) as HTMLElement;
      
      // Limpiar botones y elementos interactivos
      this.cleanElement(clone);

      // Preparar elemento para captura FULL SIZE
      this.prepareForFullScreenshot(clone);

      // Obtener dimensiones reales del elemento
      const elementWidth = element.scrollWidth;
      const elementHeight = element.scrollHeight;

      console.log(`📐 Dimensiones del elemento: ${elementWidth}x${elementHeight}px`);

      // Configuración optimizada para captura COMPLETA
      const pdfOptions = {
        margin: 0,  // Sin márgenes para capturar todo
        filename: filename,
        image: { 
          type: 'jpeg', 
          quality: 0.98 
        },
        html2canvas: { 
          scale: 2,                    // Escala para calidad
          useCORS: true,
          logging: true,               // Activar logs para debug
          backgroundColor: '#F8F9FA',
          letterRendering: true,
          allowTaint: false,
          scrollY: 0,                  // Sin offset de scroll
          scrollX: 0,
          x: 0,
          y: 0,
          width: elementWidth,         // Ancho completo
          height: elementHeight,       // Alto completo
          windowWidth: elementWidth,   // Ventana del ancho del elemento
          windowHeight: elementHeight, // Ventana del alto del elemento
          onclone: (clonedDoc: Document) => {
            const clonedElement = clonedDoc.body.querySelector('.report-content') || 
                                 clonedDoc.body.querySelector('.reports-container');
            if (clonedElement) {
              // Forzar dimensiones en el clon
              (clonedElement as HTMLElement).style.width = `${elementWidth}px`;
              (clonedElement as HTMLElement).style.height = 'auto';
              (clonedElement as HTMLElement).style.overflow = 'visible';
              this.applyScreenshotStyles(clonedElement as HTMLElement);
            }
          }
        },
        jsPDF: { 
          unit: 'px',                  // Usar píxeles para precisión
          format: [elementWidth, elementHeight], // Formato personalizado
          orientation: elementHeight > elementWidth ? 'portrait' : 'landscape',
          compress: true,
          hotfixes: ['px_scaling']
        },
        pagebreak: { 
          mode: 'avoid-all'  // Evitar saltos de página
        }
      };

      // Generar PDF
      await html2pdf().set(pdfOptions).from(clone).save();
      
      console.log('✅ PDF completo generado exitosamente');
      
    } catch (error) {
      console.error('❌ Error generando PDF:', error);
      throw error;
    }
  }

  /**
   * Preparar elemento para screenshot COMPLETO
   */
  private prepareForFullScreenshot(element: HTMLElement): void {
    // Forzar que el elemento muestre todo su contenido
    element.style.width = 'auto';
    element.style.maxWidth = 'none';
    element.style.height = 'auto';
    element.style.maxHeight = 'none';
    element.style.overflow = 'visible';
    element.style.margin = '0';
    element.style.padding = '20px';
    element.style.backgroundColor = '#F8F9FA';
    element.style.display = 'block';
    
    // Forzar que todos los hijos sean visibles
    const allElements = element.querySelectorAll('*');
    allElements.forEach(el => {
      const htmlEl = el as HTMLElement;
      
      // Asegurar visibilidad
      htmlEl.style.overflow = 'visible';
      htmlEl.style.maxHeight = 'none';
      
      // Asegurar que los colores de fondo se rendericen
      const computedStyle = window.getComputedStyle(htmlEl);
      if (computedStyle.backgroundColor && computedStyle.backgroundColor !== 'rgba(0, 0, 0, 0)') {
        htmlEl.style.backgroundColor = computedStyle.backgroundColor;
      }
      
      // Asegurar que los colores de texto se rendericen
      if (computedStyle.color) {
        htmlEl.style.color = computedStyle.color;
      }
      
      // Forzar bordes
      if (computedStyle.border && computedStyle.border !== '0px none rgb(0, 0, 0)') {
        htmlEl.style.border = computedStyle.border;
      }
    });
  }

  /**
   * Método para screenshot regular (compatible con exportLightweight)
   */
  private prepareForScreenshot(element: HTMLElement): void {
    // Estilos para screenshot normal (no full size)
    element.style.width = '100%';
    element.style.height = 'auto';
    element.style.overflow = 'visible';
    element.style.margin = '0';
    element.style.padding = '10px';
    element.style.backgroundColor = '#F8F9FA';
    element.style.display = 'block';
    
    // Estilos específicos para elementos internos
    const allElements = element.querySelectorAll('*');
    allElements.forEach(el => {
      const htmlEl = el as HTMLElement;
      htmlEl.style.overflow = 'visible';
      htmlEl.style.maxHeight = 'none';
      
      // Asegurar visibilidad de bordes y colores
      const computedStyle = window.getComputedStyle(htmlEl);
      if (computedStyle.backgroundColor && computedStyle.backgroundColor !== 'rgba(0, 0, 0, 0)') {
        htmlEl.style.backgroundColor = computedStyle.backgroundColor;
      }
    });
  }

  /**
   * Aplicar estilos específicos para screenshot
   */
  private applyScreenshotStyles(element: HTMLElement): void {
    // Banner
    const banner = element.querySelector('.report-banner');
    if (banner) {
      (banner as HTMLElement).style.background = 'linear-gradient(135deg, #1A73E8 0%, #00D9C0 100%)';
      (banner as HTMLElement).style.color = 'white';
    }

    // Section numbers
    const sectionNumbers = element.querySelectorAll('.section-number');
    sectionNumbers.forEach(num => {
      (num as HTMLElement).style.background = 'linear-gradient(135deg, #1A73E8 0%, #00D9C0 100%)';
      (num as HTMLElement).style.color = 'white';
    });

    // Stat cards
    const statCards = element.querySelectorAll('.stat-card');
    statCards.forEach(card => {
      if (card.classList.contains('positive')) {
        (card as HTMLElement).style.borderTopColor = '#00D9C0';
      } else if (card.classList.contains('neutral')) {
        (card as HTMLElement).style.borderTopColor = '#FDB82B';
      } else if (card.classList.contains('negative')) {
        (card as HTMLElement).style.borderTopColor = '#EA4335';
      }
    });

    // SVG elements
    const svgs = element.querySelectorAll('svg');
    svgs.forEach(svg => {
      const svgElement = svg as SVGSVGElement;
      svgElement.style.display = 'block';
      svgElement.style.margin = '0 auto';
      
      // Forzar dimensiones explícitas
      const bbox = svgElement.getBBox();
      if (!svgElement.getAttribute('width')) {
        svgElement.setAttribute('width', `${bbox.width || 600}`);
      }
      if (!svgElement.getAttribute('height')) {
        svgElement.setAttribute('height', `${bbox.height || 400}`);
      }
      
      // Agregar xmlns para compatibilidad
      svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      svgElement.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
      
      // Forzar que sea visible
      svgElement.style.visibility = 'visible';
      svgElement.style.opacity = '1';
    });
    // Abstract and findings boxes
    const boxes = element.querySelectorAll('.abstract-box, .findings-box');
    boxes.forEach(box => {
      (box as HTMLElement).style.background = 'linear-gradient(135deg, rgba(26, 115, 232, 0.05) 0%, rgba(0, 217, 192, 0.05) 100%)';
      (box as HTMLElement).style.borderLeft = '4px solid #1A73E8';
    });

    // Category fills
    const fills = element.querySelectorAll('.category-fill');
    fills.forEach(fill => {
      const parent = (fill as HTMLElement).closest('.category-card');
      if (parent) {
        const score = parseFloat(parent.querySelector('.category-score')?.textContent || '0');
        let color = '#64748b';
        if (score >= 70) color = '#00D9C0';
        else if (score >= 50) color = '#FDB82B';
        else color = '#EA4335';
        (fill as HTMLElement).style.background = color;
      }
    });

    // Recommendation cards borders
    const recommendations = element.querySelectorAll('.recommendation-card');
    recommendations.forEach(rec => {
      if (rec.classList.contains('potenciar')) {
        (rec as HTMLElement).style.borderLeftColor = '#00D9C0';
      } else if (rec.classList.contains('mejorar')) {
        (rec as HTMLElement).style.borderLeftColor = '#FDB82B';
      } else if (rec.classList.contains('monitorear')) {
        (rec as HTMLElement).style.borderLeftColor = '#1A73E8';
      }
    });

    // Word tags
    const wordTags = element.querySelectorAll('.word-tag');
    wordTags.forEach(tag => {
      (tag as HTMLElement).style.border = '2px solid #1A73E8';
      (tag as HTMLElement).style.color = '#1A73E8';
      (tag as HTMLElement).style.backgroundColor = 'white';
    });
  }

  /**
   * Limpiar elementos no deseados
   */
  private cleanElement(element: HTMLElement): void {
    const selectors = [
      'button',
      'select',
      'input',
      '.reports-header',
      '.btn-export',
      '.btn-refresh',
      '.period-select',
      '.action-button',
      '.header-actions',
      '[role="button"]'
    ];

    selectors.forEach(selector => {
      const elements = element.querySelectorAll(selector);
      elements.forEach(el => el.remove());
    });
  }

  /**
   * Generar nombre de archivo con timestamp
   */
  generateFilename(prefix: string = 'reporte', tipo?: string): string {
    const now = new Date();
    const fecha = now.toISOString().split('T')[0];
    const tipoStr = tipo ? `_${tipo}` : '';
    return `${prefix}_unmsm${tipoStr}_${fecha}.pdf`;
  }

  /**
   * Verificar disponibilidad de html2pdf
   */
  isAvailable(): boolean {
    return typeof html2pdf !== 'undefined';
  }

  /**
   * Exportar a PDF de alta calidad (wrapper)
   */
  async exportToPdf(
    element: HTMLElement,
    filename: string = 'reporte-unmsm.pdf'
  ): Promise<void> {
    await this.exportWithValidation(element, filename, {
      optimizeImages: true
    });
  }

  /**
   * Exportar con opciones personalizadas
   */
  async exportCustomReport(
    element: HTMLElement,
    reportType: 'sentimientos' | 'satisfaccion' | 'mensual' | 'anual' = 'sentimientos'
  ): Promise<void> {
    const filename = this.generateFilename('reporte', reportType);
    await this.exportWithValidation(element, filename, {
      reportType: reportType,
      optimizeImages: true
    });
  }

  /**
   * Exportar con calidad máxima - FULL SIZE
   */
  async exportHighQuality(
    element: HTMLElement,
    filename: string = 'reporte-unmsm-hq.pdf'
  ): Promise<void> {
    
    if (typeof html2pdf === 'undefined') {
      throw new Error('La librería html2pdf no está disponible');
    }

    try {
      console.log('📸 Generando PDF de alta calidad COMPLETO...');

      const clone = element.cloneNode(true) as HTMLElement;
      this.cleanElement(clone);
      this.prepareForFullScreenshot(clone);

      const elementWidth = element.scrollWidth;
      const elementHeight = element.scrollHeight;

      const options = {
        margin: 0,
        filename: filename,
        image: { 
          type: 'jpeg', 
          quality: 1.0  // Calidad máxima
        },
        html2canvas: { 
          scale: 3,     // Escala máxima
          useCORS: true,
          logging: true,
          backgroundColor: '#F8F9FA',
          letterRendering: true,
          allowTaint: false,
          scrollY: 0,
          scrollX: 0,
          x: 0,
          y: 0,
          width: elementWidth,
          height: elementHeight,
          windowWidth: elementWidth,
          windowHeight: elementHeight,
          onclone: (clonedDoc: Document) => {
            const clonedElement = clonedDoc.body.querySelector('.report-content') || 
                                 clonedDoc.body.querySelector('.reports-container');
            if (clonedElement) {
              (clonedElement as HTMLElement).style.width = `${elementWidth}px`;
              (clonedElement as HTMLElement).style.height = 'auto';
              (clonedElement as HTMLElement).style.overflow = 'visible';
              this.applyScreenshotStyles(clonedElement as HTMLElement);
            }
          }
        },
        jsPDF: { 
          unit: 'px',
          format: [elementWidth, elementHeight],
          orientation: elementHeight > elementWidth ? 'portrait' : 'landscape',
          compress: false,  // Sin comprimir para máxima calidad
          hotfixes: ['px_scaling']
        },
        pagebreak: { 
          mode: 'avoid-all'
        }
      };

      await html2pdf().set(options).from(clone).save();
      
      console.log('✅ PDF de alta calidad completo generado');
      
    } catch (error) {
      console.error('❌ Error:', error);
      throw error;
    }
  }

  /**
   * Exportar ligero (menor tamaño de archivo)
   */
  async exportLightweight(
    element: HTMLElement,
    filename: string = 'reporte-unmsm-light.pdf'
  ): Promise<void> {
    
    if (typeof html2pdf === 'undefined') {
      throw new Error('La librería html2pdf no está disponible');
    }

    try {
      const clone = element.cloneNode(true) as HTMLElement;
      this.cleanElement(clone);
      this.prepareForScreenshot(clone);

      const options = {
        margin: [5, 5, 5, 5],
        filename: filename,
        image: { 
          type: 'jpeg', 
          quality: 0.8  // Calidad reducida
        },
        html2canvas: { 
          scale: 1.5,   // Escala reducida
          useCORS: true,
          logging: false,
          backgroundColor: '#F8F9FA',
          scrollY: -window.scrollY,
          scrollX: -window.scrollX,
          onclone: (clonedDoc: Document) => {
            const clonedElement = clonedDoc.body.querySelector('.report-content');
            if (clonedElement) {
              this.applyScreenshotStyles(clonedElement as HTMLElement);
            }
          }
        },
        jsPDF: { 
          unit: 'mm', 
          format: 'a4', 
          orientation: 'portrait',
          compress: true  // Comprimir
        },
        pagebreak: { 
          mode: ['avoid-all'],
          avoid: '.no-break'
        }
      };

      await html2pdf().set(options).from(clone).save();
      
      console.log('✅ PDF ligero generado');
      
    } catch (error) {
      console.error('❌ Error:', error);
      throw error;
    }
  }
}