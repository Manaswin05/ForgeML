import { useState, useEffect } from 'react';
import { BarChart2, AlertCircle, RefreshCw, Info } from 'lucide-react';
import { apiService } from '../api';
import type { SessionStatus, ProfileResponse, ModelComparison } from '../api';

export default function AnalysisPage() {
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [featureCols, setFeatureCols] = useState<string[]>([]);
  const [targetCol, setTargetCol] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [analysis, setAnalysis] = useState<{
    correlation_matrix: string | null;
    pairplot: string | null;
    boxplots: string | null;
    model_comparisons: ModelComparison[];
  } | null>(null);
  const [activeTab, setActiveTab] = useState<'correlation' | 'pairplot' | 'boxplots' | 'models'>('correlation');

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
        setFeatureCols(cols.slice(0, -1));
        setTargetCol(cols[cols.length - 1]);
      }
    } catch {
      // ignore
    }
  };

  const toggleFeature = (col: string) => {
    setFeatureCols((prev) =>
      prev.includes(col) ? prev.filter((c) => c !== col) : [...prev, col]
    );
  };

  const runAnalysis = async () => {
    if (!targetCol || featureCols.length === 0) {
      setError('Select at least one feature and a target column');
      return;
    }
    if (featureCols.includes(targetCol)) {
      setError('Target column cannot also be a feature column');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await apiService.generateAnalysis({
        feature_columns: featureCols,
        target_column: targetCol,
      });
      setAnalysis(res.data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  if (!status?.has_data) {
    return (
      <div className="card">
        <div className="empty-state">
          <div className="empty-state-icon">📊</div>
          <div className="empty-state-title">No Dataset Loaded</div>
          <div className="empty-state-sub">Upload a dataset from the Home page or load one from the Dataset Store to run analysis.</div>
        </div>
      </div>
    );
  }

  const allCols = profile ? Object.keys(profile.columns) : [];

  return (
    <div className="fade-in">
      {/* Config Card */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title"><BarChart2 size={16} /> Configure Analysis</div>
        <div className="card-subtitle">Select features and a target column to analyze</div>

        <div className="page-grid-2">
          <div>
            <div className="section-title">Feature Columns</div>
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

          <div>
            <div className="form-group">
              <label className="form-label">Target Column</label>
              <select
                className="form-select"
                value={targetCol}
                onChange={(e) => {
                  const v = e.target.value;
                  setTargetCol(v);
                  setFeatureCols((prev) => prev.filter((c) => c !== v));
                }}
              >
                {allCols.map((col) => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>

            {profile && (
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <div className="stat-card" style={{ padding: '12px 16px', flex: 1 }}>
                  <div className="stat-label">Rows</div>
                  <div className="stat-value" style={{ fontSize: 20 }}>{profile.shape[0].toLocaleString()}</div>
                </div>
                <div className="stat-card" style={{ padding: '12px 16px', flex: 1 }}>
                  <div className="stat-label">Missing</div>
                  <div className="stat-value" style={{ fontSize: 20, color: profile.missing_total > 0 ? 'var(--accent-warning)' : 'var(--accent-success)' }}>
                    {profile.missing_total}
                  </div>
                </div>
                <div className="stat-card" style={{ padding: '12px 16px', flex: 1 }}>
                  <div className="stat-label">Duplicates</div>
                  <div className="stat-value" style={{ fontSize: 20, color: profile.duplicates > 0 ? 'var(--accent-warning)' : 'var(--accent-success)' }}>
                    {profile.duplicates}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {error && <div className="alert alert-error" style={{ marginTop: 16 }}><AlertCircle size={16} style={{ flexShrink: 0 }} />{error}</div>}

        <div style={{ marginTop: 20 }}>
          <button className="btn btn-primary" onClick={runAnalysis} disabled={loading}>
            {loading ? <><span className="spinner" /> Running Analysis…</> : <><RefreshCw size={15} /> Run Analysis</>}
          </button>
          {loading && (
            <span style={{ fontSize: 12, color: 'var(--text-muted)', marginLeft: 12 }}>
              This can take 30–60s for large datasets. Model comparison includes 3 CV runs.
            </span>
          )}
        </div>
      </div>

      {/* Results */}
      {analysis && (
        <div className="card fade-in">
          <div className="card-title"><Info size={15} /> Analysis Results</div>

          <div className="tabs">
            {(['correlation', 'pairplot', 'boxplots', 'models'] as const).map((tab) => (
              <button key={tab} className={`tab${activeTab === tab ? ' active' : ''}`} onClick={() => setActiveTab(tab)}>
                {tab === 'correlation' ? '🔥 Correlation' :
                  tab === 'pairplot' ? '🔵 Pairplot' :
                  tab === 'boxplots' ? '📦 Boxplots' : '🤖 Model Comparison'}
              </button>
            ))}
          </div>

          {activeTab === 'correlation' && (
            analysis.correlation_matrix
              ? <img src={analysis.correlation_matrix} alt="Correlation Matrix" className="analysis-image" />
              : <div className="empty-state" style={{ padding: 40 }}><div className="empty-state-sub">Need at least 2 numeric columns for a correlation matrix.</div></div>
          )}
          {activeTab === 'pairplot' && (
            analysis.pairplot
              ? <img src={analysis.pairplot} alt="Pair Plot" className="analysis-image" />
              : <div className="empty-state" style={{ padding: 40 }}><div className="empty-state-sub">Not enough numeric data for a pairplot.</div></div>
          )}
          {activeTab === 'boxplots' && (
            analysis.boxplots
              ? <img src={analysis.boxplots} alt="Box Plots" className="analysis-image" />
              : <div className="empty-state" style={{ padding: 40 }}><div className="empty-state-sub">No numeric feature columns available for boxplots.</div></div>
          )}
          {activeTab === 'models' && (
            <div>
              {analysis.model_comparisons.length > 0 ? analysis.model_comparisons.map((m, i) => (
                <div key={i} className="model-comp-row">
                  <div>
                    <div className="model-comp-name">{m.model}</div>
                  </div>
                  <div className="model-comp-metric">
                    <div className="model-comp-metric-label">{m.metric1_name}</div>
                    <div className="model-comp-metric-value">{m.metric1_value}</div>
                  </div>
                  <div className="model-comp-metric">
                    <div className="model-comp-metric-label">{m.metric2_name}</div>
                    <div className="model-comp-metric-value">{m.metric2_value}</div>
                  </div>
                </div>
              )) : (
                <div className="empty-state"><div className="empty-state-sub">Model comparison results unavailable.</div></div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
