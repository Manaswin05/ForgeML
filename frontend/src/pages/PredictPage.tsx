import { useState, useEffect } from 'react';
import { Zap, AlertCircle, Plus, Trash2 } from 'lucide-react';
import { apiService } from '../api';
import type { SessionStatus, PredictionResponse } from '../api';

export default function PredictPage() {
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [featureCols, setFeatureCols] = useState<string[]>([]);
  const [inputs, setInputs] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<PredictionResponse | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const s = await apiService.getStatus();
        setStatus(s.data);
        if (s.data.has_model) {
          const p = await apiService.getProfile();
          const cols = Object.keys(p.data.columns);
          // Remove target col from inputs — use all numeric-ish cols
          setFeatureCols(cols.filter((_, i) => i < cols.length - 1));
        }
      } catch { /* ignore */ }
    };
    load();
  }, []);

  const handlePredict = async () => {
    setError('');
    setLoading(true);
    try {
      const data: Record<string, unknown> = {};
      featureCols.forEach((col) => {
        const v = inputs[col];
        const num = Number(v);
        data[col] = isNaN(num) ? v : num;
      });
      const res = await apiService.predict(data);
      setResult(res.data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  if (!status?.has_model) {
    return (
      <div className="card">
        <div className="empty-state">
          <div className="empty-state-icon">⚡</div>
          <div className="empty-state-title">No Trained Model</div>
          <div className="empty-state-sub">Train a model on the Train page before running predictions.</div>
        </div>
      </div>
    );
  }

  return (
    <div className="fade-in">
      <div className="page-grid-2" style={{ alignItems: 'start' }}>
        {/* Input Form */}
        <div className="card">
          <div className="card-title"><Zap size={16} /> Prediction Input</div>
          <div className="card-subtitle">
            Model: <span className="badge badge-primary" style={{ marginLeft: 4 }}>{status.model_type}</span>
            &nbsp;Task: <span className="badge badge-info" style={{ marginLeft: 4 }}>{status.task_type}</span>
          </div>

          <div className="predict-grid">
            {featureCols.map((col) => (
              <div key={col} className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">{col}</label>
                <input
                  className="form-input"
                  placeholder="Enter value"
                  value={inputs[col] ?? ''}
                  onChange={(e) => setInputs((prev) => ({ ...prev, [col]: e.target.value }))}
                />
              </div>
            ))}
          </div>

          {featureCols.length === 0 && (
            <div className="alert alert-warning">
              <AlertCircle size={15} style={{ flexShrink: 0 }} />
              Feature columns unknown. The model may still produce a prediction if you specify inputs manually.
            </div>
          )}

          {error && <div className="alert alert-error" style={{ marginTop: 12 }}><AlertCircle size={16} style={{ flexShrink: 0 }} />{error}</div>}

          <button
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center', marginTop: 16 }}
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? <><span className="spinner" /> Predicting…</> : <><Zap size={15} /> Run Prediction</>}
          </button>
        </div>

        {/* Result */}
        <div>
          {result ? (
            <div className="predict-result fade-in">
              <div className="predict-result-label">Prediction</div>
              <div className="predict-result-value">{result.prediction}</div>
              {result.confidence !== null && (
                <div className="predict-result-confidence">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                  <div className="progress-bar-wrap" style={{ marginTop: 10 }}>
                    <div
                      className="progress-bar-fill"
                      style={{ width: `${(result.confidence * 100).toFixed(1)}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="card" style={{ height: '100%' }}>
              <div className="empty-state">
                <div className="empty-state-icon">🎯</div>
                <div className="empty-state-title">No Prediction Yet</div>
                <div className="empty-state-sub">Fill in the feature values and click "Run Prediction"</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
