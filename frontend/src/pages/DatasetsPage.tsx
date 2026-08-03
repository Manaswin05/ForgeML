import { useState, useEffect } from 'react';
import { Search, ExternalLink, Download, AlertCircle, CheckCircle, Globe } from 'lucide-react';
import { apiService } from '../api';
import type { DatasetSearchResult, UploadResponse } from '../api';

interface DatasetsPageProps {
  onLoad: () => void;
}

const SOURCE_COLORS: Record<string, string> = {
  'GitHub (Curated)': '#48bb78',
  'OpenML Public Datasets': '#63b3ed',
  'Kaggle': '#20BEFF',
  'Google Dataset Search': '#4285F4',
  'GitHub Repositories': '#6e40c9',
};

export default function DatasetsPage({ onLoad }: DatasetsPageProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<DatasetSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingUrl, setLoadingUrl] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [successName, setSuccessName] = useState('');
  const [loadedResult, setLoadedResult] = useState<UploadResponse | null>(null);
  const [customUrl, setCustomUrl] = useState('');

  const search = async (q = query) => {
    setLoading(true);
    setError('');
    try {
      const res = await apiService.searchDatasets(q);
      setResults(res.data.results);
    } catch (e: any) {
      setError('Failed to search datasets');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    search('');
  }, []);

  const loadDataset = async (url: string, name: string) => {
    setLoadingUrl(url);
    setError('');
    setSuccessName('');
    try {
      const res = await apiService.loadDatasetFromUrl(url);
      setLoadedResult(res.data);
      setSuccessName(name);
      onLoad();
    } catch (e: any) {
      setError(e?.response?.data?.detail || `Failed to load ${name}`);
    } finally {
      setLoadingUrl(null);
    }
  };

  const loadCustomUrl = () => {
    if (customUrl.trim()) loadDataset(customUrl.trim(), 'custom dataset');
  };

  return (
    <div className="fade-in">
      {/* Search bar */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title"><Search size={16} /> Dataset Store</div>
        <div className="card-subtitle">Search curated datasets from GitHub, OpenML, and more</div>

        <div style={{ display: 'flex', gap: 10, marginBottom: 12 }}>
          <input
            className="form-input"
            placeholder="Search datasets (e.g. iris, titanic, housing...)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && search()}
          />
          <button className="btn btn-primary" onClick={() => search()} disabled={loading}>
            {loading ? <span className="spinner" /> : <Search size={15} />}
            Search
          </button>
        </div>

        {/* Custom URL */}
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <Globe size={14} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
          <input
            className="form-input"
            placeholder="Or paste a direct CSV URL..."
            value={customUrl}
            onChange={(e) => setCustomUrl(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && loadCustomUrl()}
          />
          <button
            className="btn btn-secondary"
            style={{ whiteSpace: 'nowrap' }}
            onClick={loadCustomUrl}
            disabled={!customUrl.trim() || !!loadingUrl}
          >
            <Download size={14} /> Load URL
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-error"><AlertCircle size={16} style={{ flexShrink: 0 }} /> {error}</div>
      )}
      {successName && loadedResult && (
        <div className="alert alert-success">
          <CheckCircle size={16} style={{ flexShrink: 0 }} />
          Loaded <strong>{successName}</strong> — {loadedResult.info.rows.toLocaleString()} rows, {loadedResult.info.columns} columns
        </div>
      )}

      {/* Results */}
      {loading ? (
        <div className="loading-overlay"><div className="spinner spinner-lg" /><span>Searching...</span></div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {results.map((item, i) => (
            <div key={i} className="dataset-card">
              <div
                className="dataset-card-icon"
                style={{
                  background: `${SOURCE_COLORS[item.source] ?? '#7c6af7'}22`,
                  color: SOURCE_COLORS[item.source] ?? 'var(--accent-primary)',
                }}
              >
                {item.is_external ? '🔍' : '📦'}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div className="dataset-card-name">{item.name}</div>
                <div className="dataset-card-meta">
                  <span className="badge badge-info" style={{ marginRight: 6, fontSize: 10 }}>{item.source}</span>
                  {item.repository}
                </div>
              </div>
              <div className="dataset-card-actions">
                <a href={item.html_url} target="_blank" rel="noreferrer" className="btn btn-ghost btn-sm">
                  <ExternalLink size={13} /> View
                </a>
                {!item.is_external && item.url && (
                  <button
                    className="btn btn-primary btn-sm"
                    onClick={() => loadDataset(item.url, item.name)}
                    disabled={loadingUrl === item.url}
                  >
                    {loadingUrl === item.url ? <span className="spinner" /> : <Download size={13} />}
                    Load
                  </button>
                )}
              </div>
            </div>
          ))}

          {results.length === 0 && !loading && (
            <div className="empty-state">
              <div className="empty-state-icon">🔍</div>
              <div className="empty-state-title">No results found</div>
              <div className="empty-state-sub">Try a different keyword or paste a direct CSV URL above</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
