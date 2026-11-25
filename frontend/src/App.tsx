
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import type { ReactNode } from "react";
import Quizzes from "./pages/quizzes/Quizzes";
import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";
import Dashboard from "./pages/dashboard/Dashboard";
import Notes from "./pages/notes/Notes";
import Flashcards from "./pages/flashcards/Flashcards";
import Documents from "./pages/documents/Documents";
import AIAssistant from "./pages/ai-assistant/AIAssistant";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";

import "./App.css";

// Reusable layout for all authenticated pages
interface DashboardLayoutProps {
  children: ReactNode;
}

function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="app-container">
      <Sidebar />

      <main className="main-content">
        <Topbar />

        <div className="page-content">
          {children}
        </div>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route
              path="/dashboard"
              element={
                <DashboardLayout>
                  <Dashboard />
                </DashboardLayout>
              }
            />

            <Route
              path="/notes"
              element={
                <DashboardLayout>
                  <Notes />
                </DashboardLayout>
              }
            />
          </Route>

          {/* Default routes */}
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />
          <Route
                path="/flashcards"
                element={
                  <DashboardLayout>
                    <Flashcards />
                  </DashboardLayout>
                }
              />
               <Route
                  path="/documents"
                  element={
                    <DashboardLayout>
                      <Documents />
                    </DashboardLayout>
                  }
                />
                <Route
                  path="/ai-assistant"
                  element={
                    <DashboardLayout>
                      <AIAssistant />
                    </DashboardLayout>
                  }
                />
              <Route
                path="/quizzes"
                element={
                  <DashboardLayout>
                    <Quizzes />
                  </DashboardLayout>
                }
              />
            <Route
            path="*"
            element={<Navigate to="/login" replace />}
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
