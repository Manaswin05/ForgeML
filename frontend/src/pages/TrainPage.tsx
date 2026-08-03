import { useState, useEffect } from 'react';
import { Cpu, AlertCircle, CheckCircle, Download } from 'lucide-react';
import { apiService } from '../api';
import type { SessionStatus, ProfileResponse, TrainingResponse } from '../api';

interface TrainPageProps {
  onTrain: () => void;
}

const MODEL_OPTIONS = {
  classification: [
    { value: 'logistic_regression', label: 'Logistic Regression' },
    { value: 'random_forest', label: 'Random Forest' },
    { value: 'svm', label: 'SVM' },
    { value: 'gradient_boosting', label: 'Gradient Boosting' },
    { value: 'knn', label: 'K-Nearest Neighbors' },
  ],
  regression: [
    { value: 'linear_regression', label: 'Linear Regression' },
    { value: 'random_forest', label: 'Random Forest' },
    { value: 'svr', label: 'SVR' },
    { value: 'gradient_boosting', label: 'Gradient Boosting' },
    { value: 'ridge', label: 'Ridge Regression' },
  ],
};

const CLEANING_OPTIONS = [
  { value: 'drop_duplicates', label: 'Drop Duplicates' },
  { value: 'fill_missing_median', label: 'Fill Missing (Median)' },
  { value: 'fill_missing_mean', label: 'Fill Missing (Mean)' },
  { value: 'fill_missing_mode', label: 'Fill Missing (Mode)' },
  { value: 'drop_missing', label: 'Drop Rows with Missing' },
  { value: 'encode_categorical', label: 'Encode Categorical Columns' },
  { value: 'normalize', label: 'Normalize Features' },
];

export default function TrainPage({ onTrain }: TrainPageProps) {
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [featureCols, setFeatureCols] = useState<string[]>([]);
  const [targetCol, setTargetCol] = useState('');
  const [modelType, setModelType] = useState('random_forest');
  const [modelName, setModelName] = useState('');
  const [taskType, setTaskType] = useState<'auto' | 'classification' | 'regression'>('auto');
  const [testSize, setTestSize] = useState(0.2);
  const [cleaningOps, setCleaningOps] = useState<string[]>(['drop_duplicates', 'fill_missing_median', 'encode_categorical']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<TrainingResponse | null>(null);
  const [exportLoading, setExportLoading] = useState(false);
  const [exportedFile, setExportedFile] = useState('');

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const s = await apiService.getStatus();
      setStatus(s.data);
      if (s.data.has_data) {
        const p = await apiService.getProfile();
        setProfile(p.data);
        const cols = Object.keys(p.data.columns);
        setTargetCol(cols[cols.length - 1]);
        setFeatureCols(cols.slice(0, -1));
      }
    } catch { /* ignore */ }
  };

  const toggleFeature = (col: string) => {
    setFeatureCols((prev) => prev.includes(col) ? prev.filter((c) => c !== col) : [...prev, col]);
  };

  const toggleCleaning = (op: string) => {
    setCleaningOps((prev) => prev.includes(op) ? prev.filter((o) => o !== op) : [...prev, op]);
  };

  const getModelOptions = () => {
    if (taskType !== 'auto') return MODEL_OPTIONS[taskType];
    return [...MODEL_OPTIONS.classification, ...MODEL_OPTIONS.regression];
  };

  const handleTrain = async () => {
    if (featureCols.length === 0) { setError('Select at least one feature column'); return; }
    if (!targetCol) { setError('Select a target column'); return; }
    setError('');
    setLoading(true);
    setResult(null);
    try {
      const res = await apiService.trainModel({
        feature_columns: featureCols,
        target_column: targetCol,
        model_type: modelType,
        model_name: modelName || modelType,
        test_size: testSize,
        cleaning_operations: cleaningOps,
        hyperparameters: {},
      });
      setResult(res.data);
      onTrain();
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Training failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    setExportLoading(true);
    try {
      const res = await apiService.exportModel();
      setExportedFile(res.data.filename);
      window.open(apiService.downloadModel(res.data.filename), '_blank');
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Export failed');
    } finally {
      setExportLoading(false);
    }
  };

  if (!status?.has_data) {
    return (
      <div className="card">
        <div className="empty-state">
          <div className="empty-state-icon">🤖</div>
          <div className="empty-state-title">No Dataset Loaded</div>
          <div className="empty-state-sub">Upload a dataset first before training a model.</div>
        </div>
      </div>
    );
  }

  const allCols = profile ? Object.keys(profile.columns) : [];

  return (
    <div className="fade-in">
      <div className="page-grid-2" style={{ marginBottom: 20, alignItems: 'start' }}>
        {/* Left: Columns */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="card">
            <div className="card-title"><Cpu size={16} /> Columns</div>

            <div className="form-group">
              <label className="form-label">Target Column</label>
              <select
                className="form-select"
                value={targetCol}
                onChange={(e) => {
                  setTargetCol(e.target.value);
                  setFeatureCols((prev) => prev.filter((c) => c !== e.target.value));
                }}
              >
                {allCols.map((col) => <option key={col} value={col}>{col}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Feature Columns <span style={{ color: 'var(--text-muted)' }}>({featureCols.length} selected)</span></label>
              <div className="column-selector">
                {allCols.map((col) => (
                  <span
                    key={col}
                    className={`column-chip${featureCols.includes(col) ? ' selected' : ''}`}
                    onClick={() => col !== targetCol && toggleFeature(col)}
                    style={col === targetCol ? { opacity: 0.35, cursor: 'not-allowed' } : {}}
                  >
                    {col}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-title">🧹 Cleaning Operations</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7, marginTop: 4 }}>
              {CLEANING_OPTIONS.map((op) => (
                <span
                  key={op.value}
                  className={`column-chip${cleaningOps.includes(op.value) ? ' selected' : ''}`}
                  onClick={() => toggleCleaning(op.value)}
                >
                  {op.label}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Model Config */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="card">
            <div className="card-title">⚙️ Model Configuration</div>

            <div className="form-group">
              <label className="form-label">Model Name (optional)</label>
              <input
                className="form-input"
                placeholder="e.g. my_iris_classifier"
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Task Type</label>
              <select className="form-select" value={taskType} onChange={(e) => setTaskType(e.target.value as any)}>
                <option value="auto">Auto-Detect</option>
                <option value="classification">Classification</option>
                <option value="regression">Regression</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Model Algorithm</label>
              <select className="form-select" value={modelType} onChange={(e) => setModelType(e.target.value)}>
                {getModelOptions().map((m) => <option key={m.value} value={m.value}>{m.label}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Test Split — {Math.round(testSize * 100)}%</label>
              <input
                type="range" min="0.1" max="0.4" step="0.05"
                value={testSize}
                onChange={(e) => setTestSize(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent-primary)' }}
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>
                <span>10% test</span><span>40% test</span>
              </div>
            </div>

            {error && <div className="alert alert-error"><AlertCircle size={16} style={{ flexShrink: 0 }} />{error}</div>}

            <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }} onClick={handleTrain} disabled={loading}>
              {loading ? <><span className="spinner" /> Training…</> : <><Cpu size={15} /> Train Model</>}
            </button>
          </div>

          {/* Results */}
          {result && (
            <div className="card fade-in">
              <div className="card-title"><CheckCircle size={16} style={{ color: 'var(--accent-success)' }} /> Training Complete</div>
              <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap' }}>
                <span className="badge badge-primary">{result.model_type}</span>
                <span className="badge badge-info">{result.task_type}</span>
                <span className="badge badge-muted">Train: {result.train_set_size} | Test: {result.test_set_size}</span>
              </div>

              <div className="metrics-grid">
                {Object.entries(result.metrics).map(([k, v]) => (
                  <div key={k} className="metric-card">
                    <div className="metric-card-label">{k.replace(/_/g, ' ')}</div>
                    <div className="metric-card-value">{typeof v === 'number' ? v.toFixed(4) : v}</div>
                  </div>
                ))}
              </div>

              <div style={{ marginTop: 16 }}>
                <button className="btn btn-success" onClick={handleExport} disabled={exportLoading}>
                  {exportLoading ? <span className="spinner" /> : <Download size={14} />}
                  Export Model (.pkl)
                </button>
                {exportedFile && <span style={{ fontSize: 12, color: 'var(--accent-success)', marginLeft: 10 }}>✓ Saved as {exportedFile}</span>}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
