// /**
//  * MODELOS DE DATOS - FRONTEND ANGULAR
//  * Interfaces que corresponden a los schemas del backend FastAPI
//  */

// // ========== ENUMS ==========

// export enum SentimentType {
//   POSITIVO = 'Positivo',
//   NEUTRAL = 'Neutral',
//   NEGATIVO = 'Negativo'
// }

// export enum ConfidenceLevel {
//   HIGH = 'Alta',
//   MEDIUM = 'Media',
//   LOW = 'Baja'
// }

// // ========== REQUEST INTERFACES ==========

// export interface CommentAnalysisRequest {
//   text: string;
//   include_details?: boolean;
//   include_suggestions?: boolean;
// }

// export interface BatchAnalysisRequest {
//   texts: string[];
//   batch_size?: number;
//   include_details?: boolean;
// }

// // ========== RESPONSE INTERFACES ==========

// export interface SentimentProbabilities {
//   negativo: number;
//   neutral: number;
//   positivo: number;
// }

// export interface CommentFeatures {
//   emoji_score: number;
//   pos_word_score: number;
//   neg_word_score: number;
//   word_count: number;
//   char_count?: number;
//   avg_word_length?: number;
//   sentiment_diff?: number;
// }

// export interface SentimentAnalysisResponse {
//   success: boolean;
//   comment: string;
//   sentiment: string;
//   confidence: number;
//   confidence_level: string;
//   probabilities: SentimentProbabilities;
//   features?: CommentFeatures;
//   timestamp?: string;
//   error?: string | null;
// }

// export interface BatchAnalysisResponse {
//   results: SentimentAnalysisResponse[];
//   summary: {
//     sentiment_distribution: {
//       [key: string]: number;
//     };
//     avg_confidence: number;
//     positive_percentage?: number;
//     negative_percentage?: number;
//     neutral_percentage?: number;
//   };
//   total_analyzed: number;
//   timestamp: string;
// }

// // ========== ESTADÍSTICAS MEJORADAS ==========

// export interface SentimentDistribution {
//   positive: number;
//   neutral: number;
//   negative: number;
// }

// export interface TopicSentiment {
//   name: string;
//   positive: number;
//   neutral: number;
//   negative: number;
//   total: number;
// }

// export interface RecentComment {
//   text: string;
//   sentiment: string;
//   confidence: number;
//   date: string;
//   engagement?: number;
//   features?: CommentFeatures;
// }

// export interface TrendData {
//   date: string;
//   positive: number;
//   neutral: number;
//   negative: number;
// }

// export interface CategoryScore {
//   category: string;
//   score: number;
//   max_score: number;
// }

// // Interfaz principal de estadísticas (MEJORADA)
// export interface StatisticsResponse {
//   // Estadísticas básicas
//   total_comments: number;
//   distribution: {
//     [key: string]: number;
//   };
  
//   // Distribución de sentimientos (formato específico)
//   sentiment_distribution: SentimentDistribution;
  
//   // Métricas calculadas
//   avg_comment_length: number;
//   avg_confidence?: number;
//   engagement_rate?: string;
//   growth_rate?: string;
  
//   // Palabras más comunes
//   most_common_words: [string, number][];
  
//   // Temas y categorías
//   topics?: TopicSentiment[];
//   categories?: CategoryScore[];
  
//   // Comentarios recientes
//   recent_comments?: RecentComment[];
  
//   // Tendencias temporales
//   trends?: TrendData[];
  
//   // Información del modelo
//   model_info?: {
//     accuracy: number;
//     f1_weighted: number;
//     version: string;
//     last_trained?: string;
//   };
  
//   timestamp: string;
// }

// // ========== DATASET ==========

// export interface DatasetInfo {
//   total_records: number;
//   columns: string[];
//   sentiment_distribution: {
//     [key: string]: number;
//   };
//   date_loaded?: string;
//   file_name?: string;
//   file_size?: number;
// }

// export interface ModelTrainingResponse {
//   status: string;
//   accuracy: number;
//   f1_weighted: number;
//   train_size: number;
//   test_size: number;
//   features: number;
//   training_date: string;
//   model_path?: string;
// }

// // ========== REPORTES ==========

// export interface ReportSummary {
//   total_comments: number;
//   positive_percentage: number;
//   negative_percentage?: number;
//   neutral_percentage?: number;
//   general_perception: string;
//   engagement_rate?: number;
//   model_confidence?: number;
// }

// export interface ReportStatistics {
//   sentiment_distribution: {
//     [key: string]: number;
//   };
//   avg_comment_length: number;
//   most_common_words: [string, number][];
//   topics?: TopicSentiment[];
// }

// export interface ReportResponse {
//   title: string;
//   period: string;
//   summary: ReportSummary;
//   statistics: ReportStatistics;
//   insights: string[];
//   recommendations: string[];
//   generated_at: string;
//   format?: string;
// }

// // ========== HEALTH CHECK ==========

// export interface HealthCheckResponse {
//   status: string;
//   timestamp: string;
//   components: {
//     api: string;
//     analyzer: string;
//     dataset: string;
//     model: string;
//   };
//   dataset_size?: number;
//   model_accuracy?: string;
//   uptime?: string;
// }

// // ========== ERROR HANDLING ==========

// export interface ErrorResponse {
//   error: string;
//   message: string;
//   detail?: string;
//   timestamp: string;
//   status_code?: number;
// }

// // ========== HELPER TYPES ==========

// export interface ApiResponse<T> {
//   data?: T;
//   error?: ErrorResponse;
//   loading: boolean;
// }

// export interface PaginatedResponse<T> {
//   items: T[];
//   total: number;
//   page: number;
//   page_size: number;
//   pages: number;
// }

// // ========== DASHBOARD ESPECÍFICO ==========

// export interface DashboardKPI {
//   title: string;
//   value: string | number;
//   change: string;
//   trend: 'up' | 'down' | 'neutral';
//   icon: string;
//   color: string;
// }

// export interface DashboardData {
//   kpis: DashboardKPI[];
//   sentiment_distribution: SentimentDistribution;
//   topics: TopicSentiment[];
//   recent_comments: RecentComment[];
//   trends: TrendData[];
//   categories: CategoryScore[];
//   timestamp: string;
// }

// // ========== ANÁLISIS ESPECÍFICO ==========

// export interface AnalysisResult {
//   comment: string;
//   sentiment: string;
//   confidence: number;
//   probabilities: SentimentProbabilities;
//   features?: CommentFeatures;
//   timestamp: string;
//   suggestions?: string[];
// }
/**
 * MODELOS DE DATOS - FRONTEND ANGULAR
 * Interfaces que corresponden a los schemas del backend FastAPI
 */

/**
 * MODELOS DE DATOS - FRONTEND ANGULAR
 * Interfaces que corresponden a los schemas del backend FastAPI
 */

// ========== ENUMS ==========

export enum SentimentType {
  POSITIVO = 'Positivo',
  NEUTRAL = 'Neutral',
  NEGATIVO = 'Negativo'
}

export enum ConfidenceLevel {
  HIGH = 'Alta',
  MEDIUM = 'Media',
  LOW = 'Baja'
}

// ========== REQUEST INTERFACES ==========

export interface CommentAnalysisRequest {
  text: string;
  include_details?: boolean;
  include_suggestions?: boolean;
}

export interface BatchAnalysisRequest {
  texts: string[];
  batch_size?: number;
  include_details?: boolean;
}

// ========== RESPONSE INTERFACES ==========

export interface SentimentProbabilities {
  negativo: number;
  neutral: number;
  positivo: number;
}

export interface CommentFeatures {
  emoji_score: number;
  pos_word_score: number;
  neg_word_score: number;
  word_count: number;
  char_count?: number;
  avg_word_length?: number;
  sentiment_diff?: number;
}

export interface SentimentAnalysisResponse {
  success: boolean;
  comment: string;
  sentiment: string;
  confidence: number;
  confidence_level: string;
  probabilities: SentimentProbabilities;
  features?: CommentFeatures;
  timestamp?: string;
  error?: string | null;
}

export interface BatchAnalysisResponse {
  results: SentimentAnalysisResponse[];
  summary: {
    sentiment_distribution: {
      [key: string]: number;
    };
    avg_confidence: number;
    positive_percentage?: number;
    negative_percentage?: number;
    neutral_percentage?: number;
  };
  total_analyzed: number;
  timestamp: string;
}

// ========== ESTADÍSTICAS MEJORADAS ==========

export interface SentimentDistribution {
  positive: number;
  neutral: number;
  negative: number;
}

export interface TopicSentiment {
  name: string;
  positive: number;
  neutral: number;
  negative: number;
  total: number;
}

// Alias para compatibilidad con el frontend
export type { TopicSentiment as TopicData };

export interface RecentComment {
  text: string;
  sentiment: string;
  confidence: number;
  date: string;
  engagement?: number;
  features?: CommentFeatures;
}

export interface TrendData {
  date: string;
  positive: number;
  neutral: number;
  negative: number;
}

export interface CategoryScore {
  category: string;
  score: number;
  max_score: number;
}

// Interfaz principal de estadísticas (MEJORADA)
export interface StatisticsResponse {
  // Estadísticas básicas
  total_comments: number;
  distribution: {
    [key: string]: number;
  };
  
  // Distribución de sentimientos (formato específico)
  sentiment_distribution: SentimentDistribution;
  
  // Métricas calculadas
  avg_comment_length: number;
  avg_confidence?: number;
  engagement_rate?: string;
  growth_rate?: string;
  
  // Palabras más comunes
  most_common_words: [string, number][];
  
  // Temas y categorías
  topics?: TopicSentiment[];
  categories?: CategoryScore[];
  
  // Comentarios recientes
  recent_comments?: RecentComment[];
  
  // Tendencias temporales
  trends?: TrendData[];
  
  // Información del modelo
  model_info?: {
    accuracy: number;
    f1_weighted: number;
    version: string;
    last_trained?: string;
  };
  
  timestamp: string;
}

// ========== DATASET ==========

export interface DatasetInfo {
  total_records: number;
  columns: string[];
  sentiment_distribution: {
    [key: string]: number;
  };
  date_loaded?: string;
  file_name?: string;
  file_size?: number;
}

export interface ModelTrainingResponse {
  status: string;
  accuracy: number;
  f1_weighted: number;
  train_size: number;
  test_size: number;
  features: number;
  training_date: string;
  model_path?: string;
}

// ========== REPORTES ==========

export interface ReportSummary {
  total_comments: number;
  positive_percentage: number;
  negative_percentage?: number;
  neutral_percentage?: number;
  general_perception: string;
  engagement_rate?: number;
  model_confidence?: number;
}

export interface ReportStatistics {
  sentiment_distribution: {
    [key: string]: number;
  };
  avg_comment_length: number;
  most_common_words: [string, number][];
  topics?: TopicSentiment[];
}

export interface ReportResponse {
  title: string;
  period: string;
  summary: ReportSummary;
  statistics: ReportStatistics;
  insights: string[];
  recommendations: string[];
  generated_at: string;
  format?: string;
}

// ========== HEALTH CHECK ==========

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  components: {
    api: string;
    analyzer: string;
    dataset: string;
    model: string;
  };
  dataset_size?: number;
  model_accuracy?: string;
  uptime?: string;
}

// ========== ERROR HANDLING ==========

export interface ErrorResponse {
  error: string;
  message: string;
  detail?: string;
  timestamp: string;
  status_code?: number;
}

// ========== HELPER TYPES ==========

export interface ApiResponse<T> {
  data?: T;
  error?: ErrorResponse;
  loading: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// ========== DASHBOARD ESPECÍFICO ==========

export interface DashboardKPI {
  title: string;
  value: string | number;
  change: string;
  trend: 'up' | 'down' | 'neutral';
  icon: string;
  color: string;
}

export interface DashboardData {
  kpis: DashboardKPI[];
  sentiment_distribution: SentimentDistribution;
  topics: TopicSentiment[];
  recent_comments: RecentComment[];
  trends: TrendData[];
  categories: CategoryScore[];
  timestamp: string;
}

// ========== ANÁLISIS ESPECÍFICO ==========

export interface AnalysisResult {
  comment: string;
  sentiment: string;
  confidence: number;
  probabilities: SentimentProbabilities;
  features?: CommentFeatures;
  timestamp: string;
  suggestions?: string[];
}