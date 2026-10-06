import React from "react";

function StatCard({
  icon: Icon,
  label,
  value,
  description,
  className = "",
}) {
  return (
    <div className={`stat-card ${className}`}>
      <div className="stat-top">
        <div className="stat-icon">
          <Icon size={20} />
        </div>
      </div>

      <div className="stat-value">{value}</div>

      <div className="stat-label">{label}</div>

      {description && (
        <div className="stat-description">
          {description}
        </div>
      )}
    </div>
  );
}

export default StatCard;