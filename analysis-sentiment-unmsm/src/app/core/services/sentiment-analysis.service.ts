/**
 * SERVICIO DE ANÁLISIS DE SENTIMIENTOS
 * Conecta con el backend FastAPI
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError, of, BehaviorSubject } from 'rxjs';
import { catchError, map, retry, timeout, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import {
  CommentAnalysisRequest,
  BatchAnalysisRequest,
  SentimentAnalysisResponse,
  BatchAnalysisResponse,
  ErrorResponse
} from '../models/sentiment.models';

@Injectable({
  providedIn: 'root'
})
export class SentimentAnalysisService {
  
  private readonly baseUrl: string;
  private readonly timeout = environment.apiTimeout || 30000;
  
  // Estado de carga global
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  
  // Caché simple en memoria
  private cache = new Map<string, any>();
  private cacheTimeout = 5 * 60 * 1000; // 5 minutos
  
  constructor(private http: HttpClient) {
    this.baseUrl = environment.useLocalBackend 
      ? environment.backendUrl 
      : environment.mlApiUrl;
    
    console.log('🔧 SentimentAnalysisService inicializado');
    console.log(`📡 Backend URL: ${this.baseUrl}`);
  }
  
  /**
   * Headers HTTP estándar
   */
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });
  }
  
  /**
   * Analizar un comentario individual
   */
  analyzeSingle(text: string, includeDetails: boolean = true): Observable<SentimentAnalysisResponse> {
    console.log('📝 Analizando comentario:', text.substring(0, 50) + '...');
    
    this.loadingSubject.next(true);
    
    const request: CommentAnalysisRequest = {
      text,
      include_details: includeDetails,
      include_suggestions: true
    };
    
    // Verificar caché
    const cacheKey = `single_${text}`;
    const cached = this.getFromCache(cacheKey);
    if (cached) {
      console.log('⚡ Resultado obtenido de caché');
      this.loadingSubject.next(false);
      return of(cached);
    }
    
    return this.http.post<SentimentAnalysisResponse>(
      `${this.baseUrl}/analysis/single`,
      request,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout),
      retry(1),
      tap(response => {
        console.log('✅ Análisis completado:', response.sentiment);
        this.saveToCache(cacheKey, response);
        this.loadingSubject.next(false);
      }),
      catchError(error => {
        console.error('❌ Error en análisis:', error);
        this.loadingSubject.next(false);
        return this.handleError(error);
      })
    );
  }
  
  /**
   * Analizar múltiples comentarios (batch)
   */
  analyzeBatch(
    texts: string[], 
    batchSize: number = 100,
    includeDetails: boolean = true
  ): Observable<BatchAnalysisResponse> {
    console.log(`📦 Analizando lote de ${texts.length} comentarios...`);
    
    this.loadingSubject.next(true);
    
    const request: BatchAnalysisRequest = {
      texts,
      batch_size: batchSize,
      include_details: includeDetails
    };
    
    return this.http.post<BatchAnalysisResponse>(
      `${this.baseUrl}/analysis/batch`,
      request,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout * 2), // Timeout mayor para batches
      retry(1),
      tap(response => {
        console.log('✅ Batch completado:', response.total_analyzed, 'comentarios');
        this.loadingSubject.next(false);
      }),
      catchError(error => {
        console.error('❌ Error en batch:', error);
        this.loadingSubject.next(false);
        return this.handleError(error);
      })
    );
  }
  
  /**
   * Endpoint de prueba
   */
  testAnalysis(): Observable<any> {
    console.log('🧪 Ejecutando test de análisis...');
    
    return this.http.get<any>(
      `${this.baseUrl}/analysis/test`,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout),
      tap(response => console.log('✅ Test completado:', response)),
      catchError(this.handleError)
    );
  }
  
  /**
   * Predicción rápida (alias de analyzeSingle)
   */
  predict(text: string): Observable<SentimentAnalysisResponse> {
    return this.http.post<SentimentAnalysisResponse>(
      `${this.baseUrl}/analysis/predict`,
      { text },
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout),
      catchError(this.handleError)
    );
  }
  
  /**
   * Verificar salud del backend
   */
  checkHealth(): Observable<any> {
    return this.http.get<any>(
      `${this.baseUrl.replace('/api', '')}/health`,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(5000),
      catchError(error => {
        console.warn('⚠️ Backend no disponible');
        return of({ status: 'offline', error: error.message });
      })
    );
  }
  
  // ========== CACHÉ ==========
  
  private getFromCache(key: string): any {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }
    return null;
  }
  
  private saveToCache(key: string, data: any): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
  
  public clearCache(): void {
    this.cache.clear();
    console.log('🧹 Caché limpiado');
  }
  
  // ========== ERROR HANDLING ==========
  
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'Error desconocido';
    let errorDetail = '';
    
    if (error.error instanceof ErrorEvent) {
      // Error del cliente
      errorMessage = `Error de red: ${error.error.message}`;
      console.error('Error del cliente:', error.error.message);
    } else {
      // Error del servidor
      errorMessage = `Error del servidor: ${error.status}`;
      errorDetail = error.error?.message || error.message;
      
      console.error('Error del servidor:', {
        status: error.status,
        message: error.message,
        detail: error.error
      });
      
      // Mensajes amigables según el código de estado
      switch (error.status) {
        case 0:
          errorMessage = 'No se puede conectar con el servidor. Verifica que el backend esté corriendo.';
          break;
        case 400:
          errorMessage = 'Solicitud inválida';
          break;
        case 404:
          errorMessage = 'Endpoint no encontrado';
          break;
        case 500:
          errorMessage = 'Error interno del servidor';
          break;
        case 503:
          errorMessage = 'Servicio no disponible';
          break;
        case 504:
          errorMessage = 'Tiempo de espera agotado';
          break;
      }
    }
    
    const errorResponse: ErrorResponse = {
      error: error.name || 'Error',
      message: errorMessage,
      detail: errorDetail,
      timestamp: new Date().toISOString()
    };
    
    return throwError(() => errorResponse);
  }
  
  // ========== UTILIDADES ==========
  
  /**
   * Obtener clase CSS según el sentimiento
   */
  getSentimentClass(sentiment: string): string {
    switch (sentiment) {
      case 'Positivo':
        return 'sentiment-positive';
      case 'Negativo':
        return 'sentiment-negative';
      case 'Neutral':
        return 'sentiment-neutral';
      default:
        return '';
    }
  }
  
  /**
   * Obtener emoji según el sentimiento
   */
  getSentimentEmoji(sentiment: string): string {
    switch (sentiment) {
      case 'Positivo':
        return '👍';
      case 'Negativo':
        return '👎';
      case 'Neutral':
        return '➖';
      default:
        return '❓';
    }
  }
  
  /**
   * Obtener color según el sentimiento
   */
  getSentimentColor(sentiment: string): string {
    switch (sentiment) {
      case 'Positivo':
        return '#10b981';
      case 'Negativo':
        return '#ef4444';
      case 'Neutral':
        return '#f59e0b';
      default:
        return '#6b7280';
    }
  }
  
  /**
   * Formatear porcentaje
   */
  formatPercentage(value: number): string {
    return `${(value * 100).toFixed(1)}%`;
  }
  
  /**
   * Formatear fecha
   */
  formatDate(dateString: string): string {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('es-PE', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  }
}