import React from "react";
import {
  LayoutDashboard,
  Target,
  Map,
  FolderKanban,
  MessageSquare,
  Sparkles,
  Settings,
  BrainCircuit,
} from "lucide-react";

function Sidebar({ activePage, setActivePage }) {
  const menuItems = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      id: "skills",
      label: "Skill Analysis",
      icon: Target,
    },
    {
      id: "roadmap",
      label: "Career Roadmap",
      icon: Map,
    },
    {
      id: "projects",
      label: "Projects",
      icon: FolderKanban,
    },
    {
      id: "interview",
      label: "Interview Prep",
      icon: MessageSquare,
    },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <BrainCircuit size={25} />
        </div>

        <div>
          <h2>CareerNav</h2>
          <span>GenAI Navigator</span>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-title">WORKSPACE</p>

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              className={`nav-item ${
                activePage === item.id ? "active" : ""
              }`}
              onClick={() => setActivePage(item.id)}
            >
              <Icon size={19} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      <div className="sidebar-section">
        <p className="sidebar-title">AI TOOLS</p>

        <button
          className={`nav-item ${
            activePage === "ai" ? "active" : ""
          }`}
          onClick={() => setActivePage("ai")}
        >
          <Sparkles size={19} />
          <span>AI Career Assistant</span>
        </button>
      </div>

      <div className="sidebar-bottom">
        <button className="nav-item">
          <Settings size={19} />
          <span>Settings</span>
        </button>

        <div className="profile-mini">
          <div className="avatar">PC</div>

          <div>
            <strong>Pragna Chelsiya</strong>
            <span>BCA Student</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;