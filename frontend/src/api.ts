import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
});

// ── Types ──────────────────────────────────────────────────────────

export interface DatasetInfo {
  rows: number;
  columns: number;
  column_names: string[];
  data_types: Record<string, string>;
  memory_usage_mb: number;
}

export interface UploadResponse {
  status: string;
  info: DatasetInfo;
  preview: Record<string, unknown>[];
}

export interface SessionStatus {
  status: string;
  has_data: boolean;
  has_model: boolean;
  data_rows: number;
  model_type: string | null;
  task_type: string | null;
}

export interface DatasetSearchResult {
  name: string;
  repository: string;
  url: string;
  source: string;
  html_url: string;
  is_external?: boolean;
}

export interface AnalysisRequest {
  feature_columns: string[];
  target_column: string;
}

export interface ModelComparison {
  model: string;
  metric1_name: string;
  metric1_value: string;
  metric2_name: string;
  metric2_value: string;
}

export interface AnalysisResponse {
  status: string;
  correlation_matrix: string | null;
  pairplot: string | null;
  boxplots: string | null;
  model_comparisons: ModelComparison[];
}

export interface TrainingRequest {
  feature_columns: string[];
  target_column: string;
  model_type: string;
  model_name: string;
  test_size: number;
  cleaning_operations: string[];
  hyperparameters: Record<string, unknown>;
}

export interface TrainingResponse {
  status: string;
  task_type: string;
  model_type: string;
  metrics: Record<string, number>;
  train_set_size: number;
  test_set_size: number;
}

export interface PredictionResponse {
  status: string;
  prediction: string | number;
  confidence: number | null;
}

export interface ProfileColumn {
  dtype: string;
  missing: number;
  missing_pct: number;
  unique: number;
  mean?: number;
  std?: number;
  min?: number;
  max?: number;
  top?: string | number;
  freq?: number;
}

export interface ProfileResponse {
  shape: [number, number];
  columns: Record<string, ProfileColumn>;
  missing_total: number;
  duplicates: number;
}

// ── API Calls ──────────────────────────────────────────────────────

export const apiService = {
  getStatus: () => api.get<SessionStatus>('/status'),
  resetSession: () => api.delete('/reset'),

  uploadDataset: (file: File) => {
    const form = new FormData();
    form.append('file', file);
    return api.post<UploadResponse>('/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  loadDatasetFromUrl: (url: string) =>
    api.post<UploadResponse>('/load_dataset_url', { url }),

  getProfile: () => api.get<ProfileResponse>('/profile'),

  searchDatasets: (query: string) =>
    api.get<{ status: string; results: DatasetSearchResult[] }>(`/search_datasets?query=${encodeURIComponent(query)}`),

  generateAnalysis: (data: AnalysisRequest) =>
    api.post<AnalysisResponse>('/analysis', data),

  trainModel: (data: TrainingRequest) =>
    api.post<TrainingResponse>('/train', data),

  predict: (data: Record<string, unknown>) =>
    api.post<PredictionResponse>('/predict', { data }),

  exportModel: () => api.post<{ status: string; filepath: string; filename: string }>('/export'),

  downloadModel: (filename: string) =>
    `${API_BASE}/download/${filename}`,
};
