import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SentimentAnalysisService } from '../../core/services/sentiment-analysis.service';
import { 
  SentimentAnalysisResponse 
} from '../../core/models/sentiment.models';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss']
})
export class AnalysisComponent implements OnInit, OnDestroy {
  
  // Estado del componente
  selectedComment: string = '';
  analysisResult: SentimentAnalysisResponse | null = null;
  analysisHistory: SentimentAnalysisResponse[] = [];
  
  // Estados de UI
  isLoading: boolean = false;
  error: string | null = null;
  
  // Subscripciones
  private subscriptions: Subscription[] = [];
  
  constructor(
    private sentimentService: SentimentAnalysisService
  ) {}

  ngOnInit(): void {
    this.loadHistory();
    
    // Suscribirse al estado de carga del servicio
    const loadingSub = this.sentimentService.loading$.subscribe(loading => {
      this.isLoading = loading;
    });
    this.subscriptions.push(loadingSub);
    
    // Test de conexión al iniciar
    this.testConnection();
  }
  
  ngOnDestroy(): void {
    // Limpiar subscripciones
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }
  
  /**
   * Test de conexión con el backend
   */
  private testConnection(): void {
    this.sentimentService.checkHealth().subscribe({
      next: (response) => {
        if (response.status === 'healthy') {
          console.log('✅ Conectado al backend');
        }
      },
      error: (error) => {
        console.warn('⚠️ Backend no disponible:', error);
        this.error = 'No se puede conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:8000';
      }
    });
  }

  /**
   * Analizar comentario usando el backend
   */
  analyzeSingleComment(): void {
    if (!this.selectedComment.trim()) {
      this.error = 'Por favor ingresa un comentario';
      return;
    }
    
    // Limpiar error previo
    this.error = null;
    this.isLoading = true;
    
    console.log('🔍 Analizando comentario:', this.selectedComment);
    
    // Llamar al servicio
    const analysisSub = this.sentimentService.analyzeSingle(this.selectedComment, true).subscribe({
      next: (result) => {
        console.log('✅ Resultado recibido:', result);
        this.analysisResult = result;
        this.isLoading = false;
        
        // Mensaje de éxito
        console.log(`📊 Sentimiento: ${result.sentiment} (${(result.confidence * 100).toFixed(1)}%)`);
      },
      error: (error) => {
        console.error('❌ Error en análisis:', error);
        this.error = error.message || 'Error analizando el comentario';
        this.isLoading = false;
        
        // Mostrar resultado con error - CORREGIDO
        this.analysisResult = {
          success: false,
          comment: this.selectedComment,
          sentiment: 'Error',
          confidence: 0,
          confidence_level: 'Baja',
          probabilities: {
            negativo: 0,
            neutral: 0,
            positivo: 0
          },
          error: this.error || undefined,  // ✅ CAMBIADO: this.error a undefined si es null
          timestamp: new Date().toISOString()
        };
      }
    });
    this.subscriptions.push(analysisSub);
  }

  /**
   * Obtener clase CSS según el sentimiento
   */
  getSentimentClass(sentiment: string): string {
    return this.sentimentService.getSentimentClass(sentiment);
  }

  /**
   * Obtener emoji según el sentimiento
   */
  getSentimentIcon(sentiment: string): string {
    return this.sentimentService.getSentimentEmoji(sentiment);
  }

  /**
   * Contar palabras
   */
  countWords(text: string): number {
    return text.trim().split(/\s+/).length;
  }

  /**
   * Limpiar análisis
   */
  clearAnalysis(): void {
    this.selectedComment = '';
    this.analysisResult = null;
    this.error = null;
  }

  /**
   * Guardar análisis en historial
   */
  saveAnalysis(): void {
    if (this.analysisResult && this.analysisResult.success) {
      this.analysisHistory.unshift(this.analysisResult);
      this.saveHistory();
      alert('✅ Análisis guardado correctamente en el historial');
    }
  }

  /**
   * Eliminar del historial
   */
  deleteFromHistory(index: number): void {
    if (confirm('¿Está seguro de eliminar este análisis del historial?')) {
      this.analysisHistory.splice(index, 1);
      this.saveHistory();
    }
  }

  /**
   * Guardar historial en localStorage
   */
  private saveHistory(): void {
    try {
      localStorage.setItem('analysisHistory', JSON.stringify(this.analysisHistory));
    } catch (e) {
      console.error('Error guardando historial:', e);
    }
  }

  /**
   * Cargar historial desde localStorage
   */
  private loadHistory(): void {
    try {
      const saved = localStorage.getItem('analysisHistory');
      if (saved) {
        this.analysisHistory = JSON.parse(saved);
        console.log('📜 Historial cargado:', this.analysisHistory.length, 'items');
      }
    } catch (e) {
      console.error('Error cargando historial:', e);
      this.analysisHistory = [];
    }
  }
  
  /**
   * Limpiar todo el historial
   */
  clearAllHistory(): void {
    if (confirm('¿Está seguro de eliminar todo el historial?')) {
      this.analysisHistory = [];
      this.saveHistory();
      console.log('🧹 Historial limpiado');
    }
  }
}