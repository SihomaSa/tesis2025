// src/app/core/services/reports.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, timeout, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { ReportResponse } from '../models/sentiment.models';

@Injectable({
  providedIn: 'root'
})
export class ReportsService {
  
  private readonly baseUrl: string;
  private readonly timeout = environment.defaultTimeout || 10000;
  
  constructor(private http: HttpClient) {
    this.baseUrl = environment.backendUrl;
    console.log('📄 ReportsService inicializado');
  }
  
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });
  }
  
  /**
   * Generar reporte
   */
  generateReport(period: string = 'current', format: string = 'json'): Observable<ReportResponse> {
    console.log(`📄 Generando reporte: ${period} (${format})`); // ✅ CORREGIDO
    
    const request = {
      period,
      format
    };
    
    return this.http.post<ReportResponse>(
      `${this.baseUrl}/reports/generate`,
      request,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout * 2),
      tap(response => console.log('✅ Reporte generado:', response.title)),
      catchError(this.handleError)
    );
  }
  
  /**
   * Obtener último reporte
   */
  getLatestReport(): Observable<ReportResponse> {
    console.log('📄 Obteniendo último reporte...');
    
    return this.http.get<ReportResponse>(
      `${this.baseUrl}/reports/latest`,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout),
      catchError(this.handleError)
    );
  }
  
  /**
   * Exportar reporte (descarga archivo)
   */
  exportReport(format: 'pdf' | 'xlsx' | 'csv' = 'pdf'): Observable<Blob> {
    console.log(`📥 Exportando reporte en formato ${format}...`); // ✅ CORREGIDO
    
    return this.http.post(
      `${this.baseUrl}/reports/export`,
      { format },
      { 
        headers: this.getHeaders(),
        responseType: 'blob'
      }
    ).pipe(
      timeout(this.timeout * 3),
      tap(() => console.log('✅ Reporte exportado')),
      catchError(this.handleError)
    );
  }
  
  /**
   * Descargar archivo blob
   */
  downloadBlob(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    console.log('💾 Archivo descargado:', filename);
  }
  
  private handleError(error: any): Observable<never> {
    console.error('❌ Error en ReportsService:', error);
    return throwError(() => error); // ✅ CORREGIDO
  }
}