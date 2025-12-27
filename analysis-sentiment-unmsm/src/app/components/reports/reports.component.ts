import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Category {
  name: string;
  score: number;
  description: string;
}

interface WordTag {
  text: string;
  size: number;
}

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent implements OnInit {
  selectedPeriod: string = 'current';
  
  // Summary Stats
  totalComments: number = 868;
  positiveComments: number = 456;
  neutralComments: number = 234;
  negativeComments: number = 178;
  engagementRate: number = 8.4;
  avgConfidence: number = 86.3;
  
  // Calculated percentages
  positivePercentage: number = 0;
  neutralPercentage: number = 0;
  negativePercentage: number = 0;
  
  // Specific metrics
  infrastructurePositive: number = 65;
  bestDay: string = 'Miércoles';
  bestDayEngagement: number = 127;
  bestTime: string = '10:00 AM - 12:00 PM';
  bestTimeRange: string = '10:00 AM y 12:00 PM';
  
  categories: Category[] = [
    {
      name: 'Enseñanza',
      score: 85,
      description: 'Calidad docente y metodologías de enseñanza'
    },
    {
      name: 'Infraestructura',
      score: 65,
      description: 'Instalaciones, aulas y espacios académicos'
    },
    {
      name: 'Servicios',
      score: 70,
      description: 'Biblioteca, cafetería y servicios estudiantiles'
    },
    {
      name: 'Tecnología',
      score: 60,
      description: 'Plataformas digitales y recursos tecnológicos'
    },
    {
      name: 'Comunicación',
      score: 75,
      description: 'Canales de información y atención al estudiante'
    },
    {
      name: 'Gestión',
      score: 68,
      description: 'Procesos administrativos y trámites'
    }
  ];
  
  topWords: WordTag[] = [
    { text: 'Universidad', size: 24 },
    { text: 'Excelente', size: 20 },
    { text: 'Profesores', size: 22 },
    { text: 'Calidad', size: 18 },
    { text: 'Educación', size: 21 },
    { text: 'San Marcos', size: 23 },
    { text: 'Investigación', size: 19 },
    { text: 'Infraestructura', size: 17 },
    { text: 'Estudiantes', size: 20 },
    { text: 'Biblioteca', size: 16 },
    { text: 'Decana', size: 22 },
    { text: 'Perú', size: 18 }
  ];

  ngOnInit(): void {
    this.calculatePercentages();
  }

  calculatePercentages(): void {
    this.positivePercentage = Math.round((this.positiveComments / this.totalComments) * 100 * 10) / 10;
    this.neutralPercentage = Math.round((this.neutralComments / this.totalComments) * 100 * 10) / 10;
    this.negativePercentage = Math.round((this.negativeComments / this.totalComments) * 100 * 10) / 10;
  }

  onPeriodChange(): void {
    console.log('Period changed to:', this.selectedPeriod);
    // Aquí podrías cargar datos diferentes según el período
    // Por ahora solo muestra en consola
  }

  getPeriodText(): string {
    const now = new Date();
    const monthNames = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
    
    switch(this.selectedPeriod) {
      case 'current':
        return `${monthNames[now.getMonth()]} ${now.getFullYear()}`;
      case 'last':
        const lastMonth = now.getMonth() === 0 ? 11 : now.getMonth() - 1;
        const lastYear = now.getMonth() === 0 ? now.getFullYear() - 1 : now.getFullYear();
        return `${monthNames[lastMonth]} ${lastYear}`;
      case 'quarter':
        const quarterMonth = Math.floor(now.getMonth() / 3) * 3;
        return `${monthNames[quarterMonth]} - ${monthNames[now.getMonth()]} ${now.getFullYear()}`;
      case 'year':
        return `Enero - ${monthNames[now.getMonth()]} ${now.getFullYear()}`;
      default:
        return `${monthNames[now.getMonth()]} ${now.getFullYear()}`;
    }
  }

  getCurrentDate(): string {
    return new Date().toLocaleDateString('es-PE', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getScoreClass(score: number): string {
    if (score >= 80) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 60) return 'score-average';
    return 'score-poor';
  }

  exportReport(): void {
    console.log('Exportando reporte...');
    // Simular exportación
    const reportData = {
      period: this.getPeriodText(),
      date: this.getCurrentDate(),
      stats: {
        total: this.totalComments,
        positive: this.positiveComments,
        neutral: this.neutralComments,
        negative: this.negativeComments
      },
      categories: this.categories
    };
    
    console.log('Datos del reporte:', reportData);
    
    // Aquí iría la lógica real de exportación a PDF
    alert(`📄 Reporte generado exitosamente
    
Período: ${this.getPeriodText()}
Total de comentarios: ${this.totalComments}
Sentimiento positivo: ${this.positivePercentage}%

El reporte está listo para descargar.`);
  }
}