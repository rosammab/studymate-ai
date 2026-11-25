
import {
  LayoutDashboard,
  BookOpen,
  Layers,
  Brain,
  FileText,
  Bot,
  CalendarDays,
  ChartNoAxesCombined,
  Settings,
  GraduationCap,
  LogOut,
} from "lucide-react";

import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const menuItems = [
  { name: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
  { name: "My Notes", icon: BookOpen, path: "/notes" },
  { name: "Flashcards", icon: Layers, path: "/flashcards" },
  { name: "Quizzes", icon: Brain, path: "/quizzes" },
  { name: "Documents", icon: FileText, path: "/documents" },
  { name: "AI Assistant", icon: Bot, path: "/ai-assistant" },
  { name: "Study Planner", icon: CalendarDays, path: "/study-planner" },
  { name: "My Progress", icon: ChartNoAxesCombined, path: "/progress" },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/login", { replace: true });
    } catch {
      alert("Unable to log out. Please try again.");
    }
  };

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="brand">
        <div className="brand-icon">
          <GraduationCap size={25} />
        </div>

        <div>
          <h2>
            StudyMate<span>AI</span>
          </h2>
          <p>YOUR LEARNING SPACE</p>
        </div>
      </div>

      {/* Workspace menu */}
      <p className="menu-label">WORKSPACE</p>

      <nav className="sidebar-menu">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `menu-item ${isActive ? "active" : ""}`
              }
            >
              <Icon size={19} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom section */}
      <div className="sidebar-bottom">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `menu-item ${isActive ? "active" : ""}`
          }
        >
          <Settings size={19} />
          <span>Settings</span>
        </NavLink>

        {/* User profile */}
        <div className="user-profile">
          <div className="avatar">
            {user?.username?.charAt(0).toUpperCase() || "S"}
          </div>

          <div>
            <strong>{user?.username || "Student"}</strong>
            <p>{user?.email || "Student Account"}</p>
          </div>
        </div>

        {/* Logout */}
        <button
          className="menu-item logout-button"
          onClick={handleLogout}
        >
          <LogOut size={19} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
