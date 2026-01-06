/**
 * MODELOS DE REPORTES - ✅ SINCRONIZADOS CON BACKEND
 * Alineados con los schemas Pydantic de FastAPI
 */

// ========== REQUEST ==========

export interface ReportRequest {
  period: 'current' | 'last' | 'quarter' | 'year' | 'custom';
  format?: 'json' | 'pdf' | 'excel';
  start_date?: string;
  end_date?: string;
  include_details?: boolean;
}

// ========== SUMMARY ==========

export interface ReportSummary {
  total_comments: number;
  positive_count: number;
  neutral_count: number;
  negative_count: number;
  positive_percentage: number;
  negative_percentage: number;
  neutral_percentage: number;
  general_perception: 'positiva' | 'neutral' | 'negativa';
  engagement_rate: number;
  model_confidence: number;
  avg_comment_length: number;
}

// ========== STATISTICS ==========

export interface ReportStatistics {
  sentiment_distribution: { [key: string]: number };
  avg_comment_length: number;
  total_words: number;
  unique_words: number;
  most_common_words: [string, number][];
}

// ========== CATEGORIES ==========

export interface CategoryScore {
  name: string;
  score: number;
  description: string;
  positive_count: number;
  neutral_count: number;
  negative_count: number;
  total_count: number;
}

// ========== INSIGHTS ==========

export interface ReportInsight {
  type: 'positive' | 'warning' | 'info' | 'critical';
  title: string;
  description: string;
  metric: number;
  icon: string;
}

// ========== RECOMMENDATIONS ==========

export interface ReportRecommendation {
  category: 'potenciar' | 'mejorar' | 'monitorear' | 'urgente';
  title: string;
  items: string[];
  priority: 'high' | 'medium' | 'low';
}

// ========== WORD TAG ==========

export interface WordTag {
  text: string;
  size: number;
  count: number;
}

// ========== RESPONSE ==========

export interface ReportResponse {
  success: boolean;
  title: string;
  period: string;
  period_text: string;
  generated_at: string;
  summary: ReportSummary;
  statistics: ReportStatistics;
  categories: CategoryScore[];
  insights: ReportInsight[];
  recommendations: ReportRecommendation[];
  top_words: WordTag[];
  best_day: string;
  best_day_engagement: number;
  best_time: string;
  best_time_range: string;
  error?: string;
}

// ========== OPCIONES ==========

export interface PeriodOption {
  value: 'current' | 'last' | 'quarter' | 'year' | 'custom';
  label: string;
}

export type ReportFormat = 'pdf' | 'excel' | 'csv' | 'json';