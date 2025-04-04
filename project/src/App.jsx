import React, { useState, useEffect } from 'react';
import { DatabaseIcon, TableIcon, CheckCircleIcon, XCircleIcon, BarChart3Icon } from 'lucide-react';

function App() {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [tableSummaries, setTableSummaries] = useState([]);
  const [recentValidations, setRecentValidations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTables();
    fetchDashboardData();
  }, []);

  const fetchTables = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/tables/');
      const data = await response.json();
      setTables(data.tables);
    } catch (error) {
      console.error('Error fetching tables:', error);
    }
  };

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/validation/dashboard-data/');
      const data = await response.json();
      setTableSummaries(data.table_summaries);
      setRecentValidations(data.recent_validations);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const analyzeTable = async (tableName) => {
    try {
      setSelectedTable(tableName);
      const response = await fetch(`http://localhost:8000/api/v1/analyze-table/?table_name=${tableName}`);
      const data = await response.json();
      await fetch('http://localhost:8000/api/v1/validation/store-rules/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          table_name: tableName,
          rules_data: data.generated_rules,
        }),
      });
      fetchDashboardData();
    } catch (error) {
      console.error('Error analyzing table:', error);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      <nav className="nav">
        <div className="nav-content">
          <div className="nav-brand">
            <DatabaseIcon size={24} color="#2563eb" />
            <span>Data Quality Analyzer</span>
          </div>
        </div>
      </nav>

      <main className="main">
        <div className="dashboard-grid">
          {tableSummaries.map((summary) => (
            <div key={summary.table_name} className="card">
              <div className="card-header">
                <div className="card-title">
                  <TableIcon size={20} color="#2563eb" />
                  <span>{summary.table_name}</span>
                </div>
                <button
                  onClick={() => analyzeTable(summary.table_name)}
                  className="analyze-btn"
                >
                  Analyze
                </button>
              </div>
              <div className="stats-grid">
                <div>
                  <p className="stat-label">Rules</p>
                  <p className="stat-value">{summary.total_rules}</p>
                </div>
                <div>
                  <p className="stat-label">Compliance</p>
                  <p className="stat-value">
                    {summary.avg_compliance_rate ? `${Math.round(summary.avg_compliance_rate)}%` : 'N/A'}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="table-container">
          <div className="table-header">
            <BarChart3Icon size={20} color="#2563eb" />
            <h2>Recent Validations</h2>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Table</th>
                  <th>Column</th>
                  <th>Rule</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentValidations.map((validation, index) => (
                  <tr key={`${validation.rule_id}-${index}`}>
                    <td>{validation.table_name}</td>
                    <td>{validation.column_name}</td>
                    <td>{validation.rule_text}</td>
                    <td>
                      <div className="status">
                        {validation.compliance_rate >= 90 ? (
                          <CheckCircleIcon size={16} color="#059669" />
                        ) : (
                          <XCircleIcon size={16} color="#DC2626" />
                        )}
                        {Math.round(validation.compliance_rate)}% Compliant
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;