import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, timeout, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { DatasetInfo, ModelTrainingResponse } from '../models/sentiment.models';

@Injectable({
  providedIn: 'root'
})
export class DatasetService {
  
  private readonly baseUrl: string;
  private readonly timeout = environment.defaultTimeout || 10000;
  
  constructor(private http: HttpClient) {
    this.baseUrl = environment.backendUrl;
    console.log('📊 DatasetService inicializado');
  }
  
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });
  }
  
  getDatasetInfo(): Observable<DatasetInfo> {
    console.log('📊 Obteniendo info del dataset...');
    
    return this.http.get<DatasetInfo>(
      `${this.baseUrl}/dataset/info`,
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout),
      tap(response => console.log('✅ Dataset info:', response)),
      catchError(error => {
        console.error('❌ Error:', error);
        return throwError(() => error);
      })
    );
  }
  
  uploadDataset(file: File): Observable<any> {
    console.log('📤 Subiendo dataset:', file.name);
    
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post(
      `${this.baseUrl}/dataset/upload`,
      formData
    ).pipe(
      timeout(this.timeout * 3),
      tap(response => console.log('✅ Dataset cargado:', response)),
      catchError(error => {
        console.error('❌ Error:', error);
        return throwError(() => error);
      })
    );
  }
  
  trainModel(): Observable<ModelTrainingResponse> {
    console.log('🤖 Iniciando entrenamiento...');
    
    return this.http.post<ModelTrainingResponse>(
      `${this.baseUrl}/dataset/train-model`,
      {},
      { headers: this.getHeaders() }
    ).pipe(
      timeout(this.timeout * 6),
      tap(response => console.log('✅ Modelo entrenado:', response)),
      catchError(error => {
        console.error('❌ Error:', error);
        return throwError(() => error);
      })
    );
  }
}