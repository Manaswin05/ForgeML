import { useState, useRef, type DragEvent } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle, BarChart2, Database } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../api';
import type { UploadResponse } from '../api';

interface HomePageProps {
  onUpload: () => void;
}

export default function HomePage({ onUpload }: HomePageProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<UploadResponse | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleFile = async (file: File) => {
    if (!file.name.match(/\.(csv|xlsx)$/i)) {
      setError('Only CSV and Excel files are supported.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await apiService.uploadDataset(file);
      setResult(res.data);
      onUpload();
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Failed to upload dataset');
    } finally {
      setLoading(false);
    }
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const info = result?.info;

  return (
    <div className="fade-in">
      <div className="page-grid-2" style={{ marginBottom: 24 }}>
        {/* Upload Card */}
        <div className="card">
          <div className="card-title"><Upload size={16} /> Upload Dataset</div>
          <div className="card-subtitle">Drag & drop a CSV or Excel file, or click to browse</div>

          {error && (
            <div className="alert alert-error" style={{ marginBottom: 16 }}>
              <AlertCircle size={16} style={{ flexShrink: 0 }} /> {error}
            </div>
          )}

          {result && !error && (
            <div className="alert alert-success" style={{ marginBottom: 16 }}>
              <CheckCircle size={16} style={{ flexShrink: 0 }} />
              Dataset loaded: <strong>{info!.rows.toLocaleString()}</strong> rows, <strong>{info!.columns}</strong> columns
            </div>
          )}

          <div
            className={`dropzone${isDragging ? ' dragging' : ''}`}
            onDrop={onDrop}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onClick={() => fileRef.current?.click()}
          >
            {loading ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
                <div className="spinner spinner-lg" />
                <div className="dropzone-text">Uploading...</div>
              </div>
            ) : (
              <>
                <div className="dropzone-icon">📂</div>
                <div className="dropzone-text">Drop your dataset here</div>
                <div className="dropzone-subtext">Supports CSV and Excel (.xlsx)</div>
              </>
            )}
            <input
              ref={fileRef}
              type="file"
              accept=".csv,.xlsx"
              style={{ display: 'none' }}
              onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
            />
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="card-title"><FileText size={16} /> Quick Actions</div>
          <div className="card-subtitle">Jump to any step after loading a dataset</div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 8 }}>
            <button className="btn btn-secondary" style={{ justifyContent: 'flex-start' }} onClick={() => navigate('/datasets')}>
              <Database size={15} /> Browse Dataset Store
            </button>
            <button className="btn btn-secondary" style={{ justifyContent: 'flex-start' }} onClick={() => navigate('/analysis')} disabled={!result}>
              <BarChart2 size={15} /> Run Analysis
            </button>
          </div>

          {result && (
            <div style={{ marginTop: 20 }}>
              <div className="section-title">Columns</div>
              <div className="column-selector">
                {info!.column_names.map((col) => (
                  <span key={col} className="column-chip">
                    <span className="badge badge-muted" style={{ padding: '1px 6px', fontSize: 10 }}>
                      {info!.data_types[col]?.replace('object', 'str') ?? '?'}
                    </span>
                    {col}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Dataset Preview */}
      {result && (
        <div className="card fade-in">
          <div className="card-title"><FileText size={15} /> Data Preview</div>
          <div className="card-subtitle">First 10 rows of your dataset</div>

          <div className="stats-grid" style={{ marginBottom: 16 }}>
            <div className="stat-card">
              <div className="stat-label">Rows</div>
              <div className="stat-value">{info!.rows.toLocaleString()}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Columns</div>
              <div className="stat-value">{info!.columns}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Memory</div>
              <div className="stat-value">{info!.memory_usage_mb.toFixed(2)}</div>
              <div className="stat-sub">MB</div>
            </div>
          </div>

          <div className="table-wrapper">
            <table className="table">
              <thead>
                <tr>
                  {info!.column_names.map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.preview.map((row, i) => (
                  <tr key={i}>
                    {info!.column_names.map((col) => (
                      <td key={col}>{row[col] === null || row[col] === undefined ? <span style={{ color: 'var(--accent-warning)' }}>null</span> : String(row[col])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
