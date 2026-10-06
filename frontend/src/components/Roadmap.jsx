import React from "react";
import {
  BookOpen,
  Code2,
  Rocket,
  BriefcaseBusiness,
} from "lucide-react";

function Roadmap({ roadmap }) {
  const icons = [
    BookOpen,
    Code2,
    Rocket,
    BriefcaseBusiness,
  ];

  return (
    <div className="roadmap">
      {roadmap.map((item, index) => {
        const Icon = icons[index] || BookOpen;

        return (
          <div className="roadmap-item" key={index}>
            <div className="roadmap-number">
              {index + 1}
            </div>

            <div className="roadmap-icon">
              <Icon size={19} />
            </div>

            <div className="roadmap-content">
              <span className="week-label">
                WEEK {index + 1}
              </span>

              <h4>{item.title}</h4>

              <p>{item.description}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default Roadmap;