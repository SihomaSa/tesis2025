import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { 
  ReportRequest, 
  ReportResponse, 
  PeriodOption
} from '../models/report.models';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  
  private readonly API_URL = `${environment.backendUrl}/reports`; // ✅ CORREGIR SI ES NECESARIO
  
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  
  private currentReportSubject = new BehaviorSubject<ReportResponse | null>(null);
  public currentReport$ = this.currentReportSubject.asObservable();

  constructor(private http: HttpClient) {
    console.log('📊 ReportService inicializado');
    console.log('🔗 API URL:', this.API_URL);
  }

  /**
   * ✅ Generar un nuevo reporte
   */
  generateReport(request: ReportRequest): Observable<ReportResponse> {
    this.loadingSubject.next(true);
    
    console.log('📤 Generando reporte:', request);
    
    return this.http.post<ReportResponse>(`${this.API_URL}/generate`, request).pipe(
      tap(response => {
        console.log('✅ Reporte recibido:', response);
        
        // ✅ VERIFICAR DATOS
        console.log('📊 Verificación:');
        console.log('   Total:', response.summary.total_comments);
        console.log('   Positivos:', response.summary.positive_count, `(${response.summary.positive_percentage}%)`);
        console.log('   Neutrales:', response.summary.neutral_count, `(${response.summary.neutral_percentage}%)`);
        console.log('   Negativos:', response.summary.negative_count, `(${response.summary.negative_percentage}%)`);
        console.log('   Confianza:', response.summary.model_confidence + '%');
        
        this.currentReportSubject.next(response);
        this.loadingSubject.next(false);
      }),
      catchError(this.handleError.bind(this))
    );
  }

  /**
   * Obtener el último reporte
   */
  getLatestReport(): Observable<ReportResponse> {
    this.loadingSubject.next(true);
    
    return this.http.get<ReportResponse>(`${this.API_URL}/latest`).pipe(
      tap(response => {
        console.log('✅ Último reporte:', response);
        this.currentReportSubject.next(response);
        this.loadingSubject.next(false);
      }),
      catchError(this.handleError.bind(this))
    );
  }

  /**
   * Obtener períodos disponibles
   */
  getAvailablePeriods(): Observable<{ periods: PeriodOption[] }> {
    return this.http.get<{ periods: PeriodOption[] }>(`${this.API_URL}/periods`).pipe(
      tap(response => console.log('✅ Períodos:', response)),
      catchError(this.handleError.bind(this))
    );
  }

  /**
   * Limpiar reporte actual
   */
  clearCurrentReport(): void {
    this.currentReportSubject.next(null);
  }

  /**
   * Manejo de errores
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    this.loadingSubject.next(false);
    
    let errorMessage = 'Error desconocido';
    
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      if (error.status === 0) {
        errorMessage = 'No se puede conectar con el servidor. Verifica que el backend esté corriendo.';
      } else if (error.status === 404) {
        errorMessage = 'Endpoint no encontrado.';
      } else if (error.status === 500) {
        errorMessage = 'Error interno del servidor.';
      } else if (error.error?.detail) {
        errorMessage = error.error.detail;
      }
    }
    
    console.error('❌ Error en ReportService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }

  // ========== UTILIDADES ==========

  formatPercentage(value: number, decimals: number = 1): string {
    return `${value.toFixed(decimals)}%`;
  }

  formatDate(dateString: string): string {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('es-PE', {
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

  getPeriodDescription(period: string): string {
    const descriptions: { [key: string]: string } = {
      'current': 'Mes Actual',
      'last': 'Mes Anterior',
      'quarter': 'Último Trimestre',
      'year': 'Año Actual',
      'custom': 'Período Personalizado'
    };
    return descriptions[period] || 'Período Desconocido';
  }

  getScoreColor(score: number): string {
    if (score >= 80) return '#10b981';
    if (score >= 70) return '#3b82f6';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  }

  getSentimentColor(sentiment: string): string {
    const colors: { [key: string]: string } = {
      'positiva': '#10b981',
      'neutral': '#f59e0b',
      'negativa': '#ef4444'
    };
    return colors[sentiment.toLowerCase()] || '#6b7280';
  }
}