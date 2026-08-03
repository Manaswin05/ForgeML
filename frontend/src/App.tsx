import { BrowserRouter, Routes, Route, NavLink, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import {
  Home, Database, BarChart2, Cpu, Zap, RefreshCw
} from 'lucide-react';
import { apiService } from './api';
import type { SessionStatus } from './api';
import HomePage from './pages/HomePage';
import DatasetsPage from './pages/DatasetsPage';
import AnalysisPage from './pages/AnalysisPage';
import TrainPage from './pages/TrainPage';
import PredictPage from './pages/PredictPage';
import './index.css';

const navItems = [
  { to: '/', label: 'Home', icon: Home, end: true },
  { to: '/datasets', label: 'Datasets', icon: Database, end: false },
  { to: '/analysis', label: 'Analysis', icon: BarChart2, end: false },
  { to: '/train', label: 'Train', icon: Cpu, end: false },
  { to: '/predict', label: 'Predict', icon: Zap, end: false },
];

function Sidebar({ status }: { status: SessionStatus | null }) {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">🔥</div>
        <div>
          <div className="sidebar-logo-text">ForgeML</div>
          <div className="sidebar-logo-version">v1.2.0</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navigation</div>
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
          >
            <Icon size={16} className="nav-item-icon" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="session-badge">
          <div className={`session-dot${status?.has_data ? ' active' : ''}`} />
          {status?.has_data
            ? `${status.data_rows.toLocaleString()} rows loaded`
            : 'No dataset loaded'}
        </div>
        {status?.has_model && (
          <div className="session-badge" style={{ marginTop: 6 }}>
            <div className="session-dot active" />
            {status.model_type} model ready
          </div>
        )}
      </div>
    </aside>
  );
}

function TopBar({ status, onReset }: { status: SessionStatus | null; onReset: () => void }) {
  const location = useLocation();
  const pageMap: Record<string, { title: string; subtitle: string }> = {
    '/': { title: 'Home', subtitle: 'Upload datasets and view session status' },
    '/datasets': { title: 'Dataset Store', subtitle: 'Search and load public datasets' },
    '/analysis': { title: 'Analysis', subtitle: 'Visualize data and compare models' },
    '/train': { title: 'Train Model', subtitle: 'Configure features and hyperparameters' },
    '/predict': { title: 'Predict', subtitle: 'Run inference with your trained model' },
  };

  const page = pageMap[location.pathname] ?? { title: 'ForgeML', subtitle: '' };

  return (
    <header className="topbar">
      <div>
        <div className="topbar-title">{page.title}</div>
        {page.subtitle && <div className="topbar-subtitle">{page.subtitle}</div>}
      </div>
      <div className="topbar-actions">
        {status?.has_data && (
          <button className="btn btn-danger btn-sm" onClick={onReset}>
            <RefreshCw size={13} />
            Reset Session
          </button>
        )}
      </div>
    </header>
  );
}

function App() {
  const [status, setStatus] = useState<SessionStatus | null>(null);

  const fetchStatus = async () => {
    try {
      const res = await apiService.getStatus();
      setStatus(res.data);
    } catch {
      // Backend may be starting up
    }
  };

  const handleReset = async () => {
    try {
      await apiService.resetSession();
      await fetchStatus();
    } catch {
      // ignore
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar status={status} />
        <div className="main-content">
          <TopBar status={status} onReset={handleReset} />
          <main className="page-content">
            <Routes>
              <Route path="/" element={<HomePage onUpload={fetchStatus} />} />
              <Route path="/datasets" element={<DatasetsPage onLoad={fetchStatus} />} />
              <Route path="/analysis" element={<AnalysisPage />} />
              <Route path="/train" element={<TrainPage onTrain={fetchStatus} />} />
              <Route path="/predict" element={<PredictPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
