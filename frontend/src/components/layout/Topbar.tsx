import { Bell, Search } from "lucide-react";

export default function Topbar() {
  return (
    <header className="topbar">
      <div>
        <h2>Dashboard</h2>
        <p>Manage your learning activities</p>
      </div>

      <div className="topbar-actions">
        <div className="search-box">
          <Search size={18} />
          <input placeholder="Search anything..." />
        </div>

        <button className="notification-button" aria-label="Notifications">
          <Bell size={20} />
          <span />
        </button>

        <div className="topbar-avatar">S</div>
      </div>
    </header>
  );
}