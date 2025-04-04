import React from 'react';
import './StatCard.css';

const StatCard = ({ title, value, icon, color, description }) => {
  return (
    <div className="stat-card">
      <div className="stat-header">
        <div className="stat-title">{title}</div>
        <div className={`stat-icon ${color}`}>
          {icon}
        </div>
      </div>
      <div className="stat-value">{value}</div>
      {description && <div className="stat-description">{description}</div>}
    </div>
  );
};

export default StatCard;