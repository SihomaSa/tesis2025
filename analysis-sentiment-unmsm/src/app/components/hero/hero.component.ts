/**
 * HERO COMPONENT - CORREGIDO PARA GRÁFICOS DE DISTRIBUCIÓN Y TENDENCIAS
 */

import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';

import { SentimentAnalysisService } from '../../core/services/sentiment-analysis.service';
import { StatisticsService } from '../../core/services/statistics.service';
import { ReportsService } from '../../core/services/reports.service';

interface SentimentData {
  name: string;
  value: number;
  color: string;
  percentage?: number;
}

interface TopicData {
  tema: string;
  positivo: number;
  neutral: number;
  negativo: number;
}

interface CommonWord {
  word: string;
  count: number;
  percentage: number;
}

interface RadarData {
  categoria: string;
  valor: number;
  fullMark: number;
}

interface Comment {
  id?: number;
  text: string;
  sentiment: string;
  confidence: number;
  date?: string;
  engagement?: number;
}

interface KPI {
  title: string;
  value: string;
  change: string;
  icon: string;
  color: string;
  trend: string;
}

interface AnalysisResult {
  comment: string;
  sentiment: string;
  confidence: number;
  probabilities: {
    positivo: number;
    neutral: number;
    negativo: number;
  };
  timestamp: string;
}

// ✅ NUEVO: Interface para datos de tendencias temporales
interface TrendPoint {
  month: string;
  positivo: number;
  neutral: number;
  negativo: number;
}

@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.scss']
})
export class HeroComponent implements OnInit, OnDestroy {
  @Input() activeView: string = 'dashboard';
  
  private destroy$ = new Subject<void>();
  
  isLoading = false;
  hasError = false;
  errorMessage = '';
  backendConnected = false;
  
  selectedComment: string = '';
  analysisResult: AnalysisResult | null = null;
  
  // Datos del dashboard
  sentimentData: SentimentData[] = [];
  topicsData: TopicData[] = [];
  commonWords: CommonWord[] = [];
  radarData: RadarData[] = [];
  recentComments: Comment[] = [];
  kpis: KPI[] = [];
  
  // ✅ NUEVO: Datos para tendencias temporales
  trendData: TrendPoint[] = [];
  
  constructor(
    private sentimentService: SentimentAnalysisService,
    private statisticsService: StatisticsService,
    private reportsService: ReportsService
  ) {
    console.log('🎯 HeroComponent inicializado');
  }

  ngOnInit(): void {
    console.log('🚀 Iniciando carga de datos del backend...');
    this.loadAllData();
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  /**
   * ✅ CORREGIDO: Carga todos los datos del backend
   */
  loadAllData(): void {
    this.isLoading = true;
    this.hasError = false;
    
    console.log('📡 Cargando datos completos del dashboard...');
    
    this.statisticsService.getDashboardData()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (dashboardData) => {
          console.log('✅ Dashboard data recibido:', dashboardData);
          this.processDashboardData(dashboardData);
          this.backendConnected = true;
          this.isLoading = false;
        },
        error: (error) => {
          console.error('❌ Error cargando dashboard:', error);
          this.hasError = true;
          this.errorMessage = error.message;
          this.loadMockDataAsBackup();
          this.isLoading = false;
        }
      });
  }
  
  /**
   * ✅ CORREGIDO: Procesa datos del dashboard con distribución correcta
   */
  private processDashboardData(data: any): void {
    console.log('🔄 Procesando datos del dashboard...');
    
    const metrics = data.metrics;
    const distribution = metrics.sentiment_distribution;
    const percentages = metrics.sentiment_percentages || {};
    const total = metrics.total_comments;
    
    // 1. ✅ DISTRIBUCIÓN DE SENTIMIENTOS - CORREGIDA
    this.sentimentData = [
      { 
        name: 'Positivo', 
        value: distribution.Positivo || 0,
        percentage: percentages.Positivo || 0,
        color: '#10b981' 
      },
      { 
        name: 'Neutral', 
        value: distribution.Neutral || 0,
        percentage: percentages.Neutral || 0,
        color: '#f59e0b' 
      },
      { 
        name: 'Negativo', 
        value: distribution.Negativo || 0,
        percentage: percentages.Negativo || 0,
        color: '#ef4444' 
      }
    ];
    
    console.log('📊 Distribución de sentimientos:', this.sentimentData);
    
    // 2. ✅ TENDENCIAS TEMPORALES - GENERADAS
    this.trendData = this.generateTrendData(distribution, total);
    console.log('📈 Tendencias temporales:', this.trendData);
    
    // 3. KPIs
    const positiveCount = distribution.Positivo || 0;
    const positivePercentage = total > 0 ? (positiveCount / total) * 100 : 0;
    
    this.kpis = [
      { 
        title: 'Total Comentarios', 
        value: total.toString(), 
        change: '+12%', 
        icon: 'message-square', 
        color: 'bg-blue-500',
        trend: 'up'
      },
      { 
        title: 'Sentimiento Positivo', 
        value: `${positivePercentage.toFixed(1)}%`, 
        change: '+5%', 
        icon: 'thumbs-up', 
        color: 'bg-green-500',
        trend: 'up'
      },
      { 
        title: 'Engagement Rate', 
        value: '8.4%', 
        change: '+2.1%', 
        icon: 'activity', 
        color: 'bg-purple-500',
        trend: 'up'
      },
      { 
        title: 'Confianza Promedio', 
        value: data.model_info?.accuracy 
          ? `${(data.model_info.accuracy * 100).toFixed(1)}%` 
          : '86%', 
        change: '+1.8%', 
        icon: 'trending-up', 
        color: 'bg-orange-500',
        trend: 'up'
      }
    ];
    
    console.log('📈 KPIs:', this.kpis);
    
    // 4. TEMAS
    if (data.topics_analysis && data.topics_analysis.length > 0) {
      this.topicsData = data.topics_analysis.map((topic: any) => ({
        tema: topic.name,
        positivo: topic.positive,
        neutral: topic.neutral,
        negativo: topic.negative
      }));
      console.log('📚 Temas:', this.topicsData);
    } else {
      this.topicsData = [];
    }
    
    // 5. PALABRAS MÁS COMUNES
    if (metrics.most_common_words && metrics.most_common_words.length > 0) {
      this.commonWords = metrics.most_common_words
        .slice(0, 10)
        .map((wordData: [string, number]) => ({
          word: this.formatWord(wordData[0]),
          count: wordData[1],
          percentage: total > 0 ? (wordData[1] / total) * 100 : 0
        }));
      console.log('📝 Palabras comunes:', this.commonWords);
    } else {
      this.commonWords = [];
    }
    
    // 6. COMENTARIOS RECIENTES
    if (data.recent_comments && data.recent_comments.length > 0) {
      this.recentComments = data.recent_comments.map((comment: any, index: number) => ({
        id: index + 1,
        text: comment.comment,
        sentiment: comment.sentiment,
        confidence: comment.confidence,
        date: new Date().toISOString().split('T')[0],
        engagement: Math.floor(Math.random() * 50) + 20
      }));
      console.log('💬 Comentarios recientes:', this.recentComments);
    } else {
      this.recentComments = [];
    }
    
    // 7. RADAR
    this.generateRadarData();
    
    console.log('✅ Procesamiento de dashboard completado');
  }

  /**
   * Genera datos para el gráfico radar
   */
  private generateRadarData(): void {
    const total = this.getTotalComments();
    const positivePercent = this.getSentimentPercentage('Positivo');
    
    const baseValue = positivePercent;
    
    this.radarData = [
      { categoria: 'Enseñanza', valor: Math.min(100, baseValue + 5), fullMark: 100 },
      { categoria: 'Infraestructura', valor: Math.min(100, baseValue - 10), fullMark: 100 },
      { categoria: 'Servicios', valor: Math.min(100, baseValue - 5), fullMark: 100 },
      { categoria: 'Tecnología', valor: Math.min(100, baseValue - 15), fullMark: 100 },
      { categoria: 'Comunicación', valor: Math.min(100, baseValue), fullMark: 100 },
      { categoria: 'Gestión', valor: Math.min(100, baseValue - 8), fullMark: 100 }
    ];
    
    console.log('🎯 Radar data:', this.radarData);
  }
  
  /**
   * Formatear palabras especiales
   */
  private formatWord(word: string): string {
    const specialWords: { [key: string]: string } = {
      'EMOJI_5': '😊',
      'EMOJI_4': '😍',
      'EMOJI_3': '👏',
      'EMOJI_2': '❤️',
      'EMOJI_1': '😂',
      'EMOJI': '😀',
      'MENCION': '@Mención'
    };
    
    return specialWords[word] || word;
  }
  
  /**
   * Cargar datos mock como respaldo
   */
  private loadMockDataAsBackup(): void {
    console.warn('⚠️ Usando datos mock de respaldo');
    this.backendConnected = false;
    
    this.sentimentData = [
      { name: 'Positivo', value: 456, percentage: 52.5, color: '#10b981' },
      { name: 'Neutral', value: 234, percentage: 27.0, color: '#f59e0b' },
      { name: 'Negativo', value: 178, percentage: 20.5, color: '#ef4444' }
    ];
    
    // Generar tendencias mock
    this.trendData = this.generateTrendData(
      { Positivo: 456, Neutral: 234, Negativo: 178 },
      868
    );
    
    const total = this.getTotalComments();
    const positivePercentage = this.getSentimentPercentage('Positivo');
    
    this.kpis = [
      { title: 'Total Comentarios', value: total.toString(), change: '+12%', icon: 'message-square', color: 'bg-blue-500', trend: 'up' },
      { title: 'Sentimiento Positivo', value: `${positivePercentage.toFixed(1)}%`, change: '+5%', icon: 'thumbs-up', color: 'bg-green-500', trend: 'up' },
      { title: 'Engagement Rate', value: '8.4%', change: '+2%', icon: 'activity', color: 'bg-purple-500', trend: 'up' },
      { title: 'Confianza Promedio', value: '86%', change: '+2%', icon: 'trending-up', color: 'bg-orange-500', trend: 'up' }
    ];
    
    this.topicsData = [
      { tema: 'Infraestructura', positivo: 65, neutral: 20, negativo: 15 },
      { tema: 'Docentes', positivo: 80, neutral: 15, negativo: 5 },
      { tema: 'Servicios', positivo: 45, neutral: 30, negativo: 25 }
    ];
    
    this.commonWords = [
      { word: 'universidad', count: 245, percentage: 28.2 },
      { word: 'excelente', count: 198, percentage: 22.8 },
      { word: 'profesor', count: 176, percentage: 20.3 }
    ];
    
    this.generateRadarData();
    
    this.recentComments = [
      { id: 1, text: 'Excelente universidad', sentiment: 'Positivo', confidence: 0.92, date: '2025-11-23', engagement: 45 }
    ];
  }

  /**
   * Analizar comentario individual
   */
  analyzeSingleComment(): void {
    if (!this.selectedComment.trim()) return;
    
    console.log('🔍 Analizando comentario:', this.selectedComment);
    this.isLoading = true;
    
    this.sentimentService.analyzeSingle(this.selectedComment, true)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          console.log('✅ Análisis recibido:', response);
          
          this.analysisResult = {
            comment: this.selectedComment,
            sentiment: response.sentiment,
            confidence: response.confidence,
            probabilities: response.probabilities || {
              positivo: 0,
              neutral: 0,
              negativo: 0
            },
            timestamp: new Date().toLocaleString('es-PE')
          };
          
          this.isLoading = false;
        },
        error: (error) => {
          console.error('❌ Error:', error);
          this.hasError = true;
          this.errorMessage = error.message;
          this.isLoading = false;
        }
      });
  }

  /**
   * Exportar reporte
   */
  exportReport(): void {
    console.log('📥 Exportando reporte...');
    this.isLoading = true;
    
    this.reportsService.exportReport('pdf')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (blob) => {
          const filename = `reporte_unmsm_${new Date().toISOString().split('T')[0]}.pdf`;
          this.reportsService.downloadBlob(blob, filename);
          console.log('✅ Reporte descargado');
          this.isLoading = false;
        },
        error: (error) => {
          console.error('❌ Error:', error);
          alert('Error al exportar el reporte');
          this.isLoading = false;
        }
      });
  }
  
  /**
   * Recargar datos
   */
  refreshData(): void {
    console.log('🔄 Recargando datos...');
    this.statisticsService.clearCache();
    this.loadAllData();
  }

  // ========== UTILIDADES ==========
  
  getSentimentClass(sentiment: string): string {
    return this.sentimentService.getSentimentClass(sentiment);
  }

  getSentimentIcon(sentiment: string): string {
    return this.sentimentService.getSentimentEmoji(sentiment);
  }

  getTotalComments(): number {
    return this.sentimentData.reduce((sum, item) => sum + item.value, 0);
  }

  getSentimentPercentage(sentiment: string): number {
    const total = this.getTotalComments();
    if (total === 0) return 0;
    
    const item = this.sentimentData.find(s => s.name === sentiment);
    return item ? (item.value / total) * 100 : 0;
  }

  getBarWidth(value: number, maxValue: number): string {
    return `${(value / maxValue) * 100}%`;
  }
  
  getWordBarWidth(count: number): string {
    if (this.commonWords.length === 0) return '0%';
    const maxCount = Math.max(...this.commonWords.map(w => w.count));
    return `${(count / maxCount) * 100}%`;
  }

  // ✅ MÉTODOS PARA GRÁFICO DE PASTEL
  
  /**
   * Calcula el dasharray para el círculo del gráfico de pastel
   */
  /**
 * ✅ MÉTODO CORREGIDO: Calcula el dasharray para círculos SVG
 */
getCircleDashArray(value: number): string {
  const total = this.getTotalComments();
  if (total === 0) return '0 502.4'; // Circunferencia completa
  
  const circumference = 2 * Math.PI * 80; // 502.4
  const percentage = value / total;
  const filled = circumference * percentage;
  const empty = circumference - filled;
  
  return `${filled.toFixed(2)} ${empty.toFixed(2)}`;
}

/**
 * ✅ MÉTODO CORREGIDO: Offset acumulativo
 */
getCircleDashOffset(index: number): number {
  if (index === 0) return 0;
  
  const total = this.getTotalComments();
  if (total === 0) return 0;
  
  const circumference = 2 * Math.PI * 80;
  let accumulatedPercentage = 0;
  
  for (let i = 0; i < index; i++) {
    accumulatedPercentage += this.sentimentData[i].value / total;
  }
  
  return -(accumulatedPercentage * circumference);
}

/**
 * ✅ MÉTODO CORREGIDO: Líneas de tendencias
 */
getTrendLinePoints(sentiment: 'positivo' | 'neutral' | 'negativo'): string {
  if (this.trendData.length === 0) return '';
  
  const padding = 40;
  const graphWidth = 340;
  const graphHeight = 160;
  const maxValue = 100;
  
  const points = this.trendData.map((point, index) => {
    const x = padding + (index * graphWidth / Math.max(1, this.trendData.length - 1));
    const value = point[sentiment];
    const y = padding + graphHeight - ((value / maxValue) * graphHeight);
    return `${x.toFixed(2)},${y.toFixed(2)}`;
  });
  
  return points.join(' ');
}

/**
 * ✅ MÉTODO MEJORADO: Genera tendencias más realistas
 */
private generateTrendData(distribution: any, total: number): TrendPoint[] {
  const months = ['Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const trends: TrendPoint[] = [];
  
  // Porcentajes finales (mes actual)
  const finalPositive = ((distribution.Positivo || 0) / total) * 100;
  const finalNeutral = ((distribution.Neutral || 0) / total) * 100;
  const finalNegative = ((distribution.Negativo || 0) / total) * 100;
  
  // Generar evolución mes a mes
  for (let i = 0; i < 6; i++) {
    const progress = i / 5; // 0 a 1
    
    // Tendencia: positivos crecen, negativos decrecen
    const variation = (Math.random() - 0.5) * 5; // ±2.5%
    
    trends.push({
      month: months[i],
      positivo: Math.max(15, Math.min(85, 
        finalPositive - (5 - i) * 2 + variation
      )),
      neutral: Math.max(10, Math.min(50,
        finalNeutral + (Math.random() - 0.5) * 3
      )),
      negativo: Math.max(5, Math.min(35,
        finalNegative + (5 - i) * 1.5 - variation
      ))
    });
  }
  
  return trends;
}

  

  // Métodos para gráfico radar
  getPolygonPoints(): string {
    const centerX = 150;
    const centerY = 150;
    const maxRadius = 100;
    
    if (!this.radarData || this.radarData.length === 0) {
      return "150,65 210,110 210,185 150,218 95,185 95,115";
    }
    
    const points = this.radarData.map((item, index) => {
      const angle = (index * 60 * Math.PI) / 180;
      const normalizedValue = ((item.valor - 60) / 25) * 60 + 40;
      const radius = (normalizedValue / 100) * maxRadius;
      
      const x = centerX + radius * Math.sin(angle);
      const y = centerY - radius * Math.cos(angle);
      
      return `${x},${y}`;
    });
    
    return points.join(' ');
  }

  getDataPoints(): { x: number, y: number }[] {
    const centerX = 150;
    const centerY = 150;
    const maxRadius = 100;
    
    if (!this.radarData || this.radarData.length === 0) {
      return [
        { x: 150, y: 65 },
        { x: 210, y: 110 },
        { x: 210, y: 185 },
        { x: 150, y: 218 },
        { x: 95, y: 185 },
        { x: 95, y: 115 }
      ];
    }
    
    return this.radarData.map((item, index) => {
      const angle = (index * 60 * Math.PI) / 180;
      const normalizedValue = ((item.valor - 60) / 25) * 60 + 40;
      const radius = (normalizedValue / 100) * maxRadius;
      
      const x = centerX + radius * Math.sin(angle);
      const y = centerY - radius * Math.cos(angle);
      
      return { x, y };
    });
  }
}