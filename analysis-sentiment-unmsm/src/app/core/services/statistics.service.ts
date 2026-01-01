/**
 * SERVICIO DE ESTADÍSTICAS - VERSIÓN LIMPIA
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, of, forkJoin } from 'rxjs';
import { catchError, map, retry, tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

// ========== INTERFACES ==========

export interface SentimentDistribution {
  Positivo: number;
  Neutral: number;
  Negativo: number;
  [key: string]: number;
}

export interface ModelInfo {
  accuracy: number;
  f1_weighted: number;
  train_size: number;
  test_size: number;
  features: number;
  training_date: string;
  version: string;
}

export interface StatisticsResponse {
  total_comments: number;
  distribution: SentimentDistribution;
  percentages?: SentimentDistribution;
  avg_comment_length: number;
  most_common_words: Array<[string, number]>;
  model_info?: ModelInfo;
  dataset_sample_size?: number;
  timestamp: string;
}

export interface TopicAnalysis {
  name: string;
  positive: number;
  neutral: number;
  negative: number;
  total: number;
  percentage?: number;
}

export interface RecentComment {
  comment: string;
  sentiment: string;
  confidence: number;
}

export interface DashboardData {
  metrics: {
    total_comments: number;
    sentiment_distribution: SentimentDistribution;
    sentiment_percentages: SentimentDistribution;
    changes: any;
    avg_comment_length: number;
    most_common_words: Array<[string, number]>;
  };
  topics_analysis: TopicAnalysis[];
  recent_comments: RecentComment[];
  model_info?: ModelInfo;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class StatisticsService {
  private readonly API_URL = `${environment.backendUrl}/statistics`;
  private readonly CACHE_TIME = 5 * 60 * 1000; // 5 minutos
  
  // Cache
  private cache = new Map<string, { data: any; timestamp: number }>();
  
  constructor(private http: HttpClient) {
    console.log('📊 StatisticsService inicializado');
    console.log('🔗 API URL:', this.API_URL);
  }

  // ========== MÉTODOS PRINCIPALES ==========

  getStatistics(): Observable<StatisticsResponse> {
    console.log('📡 GET /statistics/');
    
    return this.http.get<StatisticsResponse>(`${this.API_URL}/`).pipe(
      retry(2),
      tap(data => {
        console.log('✅ Estadísticas recibidas:', data);
        this.setCache('statistics', data);
      }),
      catchError(this.handleError<StatisticsResponse>('getStatistics'))
    );
  }

  getTopicAnalysis(): Observable<TopicAnalysis[]> {
    console.log('📡 GET /statistics/topics');
    
    return this.http.get<TopicAnalysis[]>(`${this.API_URL}/topics`).pipe(
      retry(2),
      tap(data => {
        console.log('✅ Temas recibidos:', data);
        this.setCache('topics', data);
      }),
      catchError(this.handleError<TopicAnalysis[]>('getTopicAnalysis', []))
    );
  }

  getRecentComments(limit: number = 10): Observable<any> {
    console.log(`📡 GET /statistics/recent-comments?limit=${limit}`);
    
    return this.http.get<any>(`${this.API_URL}/recent-comments`, {
      params: { limit: limit.toString() }
    }).pipe(
      retry(2),
      tap(data => console.log('✅ Comentarios recientes:', data)),
      catchError(this.handleError<any>('getRecentComments', { comments: [] }))
    );
  }

  getDashboardData(): Observable<DashboardData> {
    console.log('📡 GET /statistics/dashboard-data');
    
    return this.http.get<DashboardData>(`${this.API_URL}/dashboard-data`).pipe(
      retry(2),
      tap(data => {
        console.log('✅ Dashboard data recibido:', data);
        this.setCache('dashboard', data);
      }),
      catchError(() => {
        console.warn('⚠️ Error en dashboard-data, usando fallback');
        return this.getDashboardDataFallback();
      })
    );
  }

  checkBackendHealth(): Observable<boolean> {
    console.log('🏥 Verificando salud del backend...');
    
    return this.http.get<any>(`${environment.backendUrl}/health`, {
      headers: { 'X-Health-Check': 'true' }
    }).pipe(
      map(response => {
        console.log('✅ Backend health:', response);
        return response.status === 'healthy';
      }),
      catchError(() => {
        console.error('❌ Backend no disponible');
        return of(false);
      })
    );
  }

  // ========== PRIVADOS ==========

  private getDashboardDataFallback(): Observable<DashboardData> {
    console.log('🔄 Usando fallback para dashboard data');
    
    return forkJoin({
      stats: this.getStatistics(),
      topics: this.getTopicAnalysis(),
      comments: this.getRecentComments(5)
    }).pipe(
      map(({ stats, topics, comments }) => {
        const distribution = stats.distribution;
        const total = stats.total_comments;
        
        const percentages = stats.percentages || {
          Positivo: (distribution.Positivo / total) * 100,
          Neutral: (distribution.Neutral / total) * 100,
          Negativo: (distribution.Negativo / total) * 100
        };

        return {
          metrics: {
            total_comments: total,
            sentiment_distribution: distribution,
            sentiment_percentages: percentages,
            changes: this.generateMockChanges(),
            avg_comment_length: stats.avg_comment_length,
            most_common_words: stats.most_common_words
          },
          topics_analysis: topics,
          recent_comments: comments.comments || [],
          model_info: stats.model_info,
          timestamp: new Date().toISOString()
        };
      })
    );
  }

  private setCache(key: string, data: any): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  private getCache<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (!cached) return null;
    
    const isExpired = Date.now() - cached.timestamp > this.CACHE_TIME;
    if (isExpired) {
      this.cache.delete(key);
      return null;
    }
    
    console.log(`✨ Usando cache para: ${key}`);
    return cached.data as T;
  }

  clearCache(): void {
    console.log('🗑️ Limpiando cache');
    this.cache.clear();
  }

  private generateMockChanges(): any {
    return {
      total_comments: { change: '+12%', trend: 'up' },
      positive_sentiment: { change: '+5%', trend: 'up' },
      negative_sentiment: { change: '-3%', trend: 'down' },
      neutral_sentiment: { change: '+2%', trend: 'stable' }
    };
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: HttpErrorResponse): Observable<T> => {
      console.error(`❌ Error en ${operation}:`, error);
      
      let errorMessage = 'Error desconocido';
      
      if (error.error instanceof ErrorEvent) {
        errorMessage = `Error de red: ${error.error.message}`;
      } else {
        errorMessage = `Error ${error.status}: ${error.message}`;
        
        if (error.status === 0) {
          errorMessage = 'No se puede conectar con el backend';
        } else if (error.status === 404) {
          errorMessage = 'Endpoint no encontrado';
        } else if (error.status === 500) {
          errorMessage = 'Error interno del servidor';
        }
      }
      
      console.error('📝 Mensaje de error:', errorMessage);
      
      if (result !== undefined) {
        return of(result as T);
      }
      
      return throwError(() => new Error(errorMessage));
    };
  }
}