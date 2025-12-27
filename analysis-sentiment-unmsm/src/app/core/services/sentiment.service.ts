import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

export interface SentimentResult {
  comment: string;
  sentiment: 'Positivo' | 'Neutral' | 'Negativo';
  confidence: number;
  probabilities: {
    positivo: number;
    neutral: number;
    negativo: number;
  };
  features?: any;
  timestamp: string;
}

export interface Statistics {
  total_comments: number;
  distribution: {
    Positivo: number;
    Neutral: number;
    Negativo: number;
  };
  percentages: {
    Positivo: number;
    Neutral: number;
    Negativo: number;
  };
  avg_comment_length: number;
  most_common_words: [string, number][];
  model_info?: any;
  timestamp: string;
}

export interface TopicAnalysis {
  name: string;
  positive: number;
  neutral: number;
  negative: number;
  total: number;
  percentage: number;
}

export interface RecentComment {
  comment: string;
  sentiment: string;
  confidence: number;
  timestamp?: string;
}

export interface DashboardData {
  metrics: {
    total_comments: number;
    sentiment_distribution: any;
    sentiment_percentages: any;
    changes: any;
    avg_comment_length: number;
    most_common_words: [string, number][];
  };
  topics_analysis: TopicAnalysis[];
  recent_comments: RecentComment[];
  model_info?: any;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class SentimentService {
  private apiUrl = 'http://localhost:8000'; // Cambia a tu puerto del backend

  constructor(private http: HttpClient) {}

  /**
   * Analizar un comentario individual
   */
  analyzeSingle(comment: string): Observable<SentimentResult> {
    return this.http.post<SentimentResult>(`${this.apiUrl}/api/analysis/single`, { text: comment });
  }

  /**
   * Analizar múltiples comentarios
   */
  analyzeBatch(comments: string[]): Observable<SentimentResult[]> {
    return this.http.post<{ results: SentimentResult[] }>(`${this.apiUrl}/api/analysis/batch`, { comments })
      .pipe(map(response => response.results));
  }

  /**
   * Obtener estadísticas COMPLETAS del dataset
   */
  getStatistics(): Observable<Statistics> {
    return this.http.get<Statistics>(`${this.apiUrl}/api/statistics/`);
  }

  /**
   * Obtener análisis por temas
   */
  getTopicAnalysis(): Observable<TopicAnalysis[]> {
    return this.http.get<TopicAnalysis[]>(`${this.apiUrl}/api/statistics/topics`);
  }

  /**
   * Obtener comentarios recientes
   */
  getRecentComments(limit: number = 10): Observable<RecentComment[]> {
    return this.http.get<any>(`${this.apiUrl}/api/statistics/recent-comments?limit=${limit}`)
      .pipe(map(response => response.comments));
  }

  /**
   * Obtener TODOS los datos para el dashboard
   */
  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.apiUrl}/api/statistics/dashboard-data`);
  }

  /**
   * Obtener información del dataset
   */
  getDatasetInfo(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/dataset/info`);
  }

  /**
   * Verificar salud del sistema
   */
  getHealthCheck(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/health`);
  }

  /**
   * Obtener todos los datos de una vez (para inicialización rápida)
   */
  getAllData(): Observable<{
    statistics: Statistics;
    topics: TopicAnalysis[];
    recentComments: RecentComment[];
  }> {
    return forkJoin({
      statistics: this.getStatistics(),
      topics: this.getTopicAnalysis(),
      recentComments: this.getRecentComments(5)
    });
  }

  /**
   * Calcular indicadores de satisfacción por categoría
   */
  getSatisfactionIndicators(): Observable<any> {
    return this.getTopicAnalysis().pipe(
      map(topics => {
        return topics.map(topic => ({
          category: topic.name,
          satisfaction: ((topic.positive + (topic.neutral * 0.3)) / topic.total) * 100
        }));
      })
    );
  }
}