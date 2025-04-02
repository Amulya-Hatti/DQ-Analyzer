import { FaFileAlt, FaTable, FaColumns, FaCheckCircle, FaClone, FaShieldAlt, FaSearch } from 'react-icons/fa';
import './Results.css';

export default function Results({ data, onReset }) {
  return (
    <div className="results-container">
      <div className="header-section">
        <h2>📊 Analysis Report</h2>
        <div className="header-actions">
          <button onClick={onReset} className="action-btn new-analysis">
            🔄 Analyze New File
          </button>
        </div>
      </div>

      <div className="summary-section">
        <div className="summary-card">
          <h3>Dataset Overview</h3>
          <div className="metrics-grid">
            <MetricItem icon={<FaFileAlt />} label="File Name" value={data.business_summary.dataset_name} />
            <MetricItem icon={<FaTable />} label="Total Rows" value={data.business_summary.total_rows} />
            <MetricItem icon={<FaColumns />} label="Total Columns" value={data.business_summary.total_columns} />
            <MetricItem icon={<FaCheckCircle />} label="Complete Data" value={`${data.business_summary.complete_records_percentage}%`} />
            <MetricItem icon={<FaClone />} label="Duplicates" value={`${data.business_summary.duplicate_records_percentage}%`} />
            <MetricItem icon={<FaShieldAlt />} label="Rule Coverage" value={`${data.business_summary.rule_coverage_percentage}%`} />
          </div>
        </div>
      </div>

      <div className="rules-section">
        <h3>Data Quality Rules</h3>
        <div className="rules-grid">
          {data.generated_rules.rules.map((rule, index) => (
            <div key={index} className="rule-card">
              <div className="rule-header">
                <span className="rule-icon"><FaSearch /></span>
                <h4>{rule.column}</h4>
              </div>
              <div className="rule-content">
                {rule.rules.map((r, idx) => (
                  <div key={idx} className="rule-item">
                    <p className="rule-definition">
                      <strong>Validation Rule:</strong> {r.rule}
                    </p>
                    <p className="rule-reason">
                      <strong>Importance:</strong> {r.reason}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const MetricItem = ({ icon, label, value }) => (
  <div className="metric-item">
    <span className="metric-icon">{icon}</span>
    <div className="metric-text">
      <span className="metric-label">{label}</span>
      <span className="metric-value">{value}</span>
    </div>
  </div>
);
