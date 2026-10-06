import React from "react";

function SkillBar({ skill, percentage, type = "normal" }) {
  return (
    <div className="skill-row">
      <div className="skill-row-header">
        <span>{skill}</span>

        <span className={`skill-percentage ${type}`}>
          {percentage}%
        </span>
      </div>

      <div className="skill-track">
        <div
          className={`skill-fill ${type}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

export default SkillBar;