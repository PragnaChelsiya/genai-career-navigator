import React from "react";
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

function RadarChart({ data }) {
  return (
    <div className="radar-container">
      <ResponsiveContainer width="100%" height={300}>
        <RechartsRadarChart data={data}>
          <PolarGrid stroke="#29344a" />

          <PolarAngleAxis
            dataKey="skill"
            tick={{
              fill: "#94a3b8",
              fontSize: 11,
            }}
          />

          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={{
              fill: "#64748b",
              fontSize: 9,
            }}
          />

          <Radar
            name="Skill Level"
            dataKey="value"
            stroke="#8b5cf6"
            fill="#8b5cf6"
            fillOpacity={0.25}
            strokeWidth={2}
          />

          <Tooltip
            contentStyle={{
              background: "#111827",
              border: "1px solid #29344a",
              borderRadius: "10px",
              color: "#fff",
            }}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RadarChart;