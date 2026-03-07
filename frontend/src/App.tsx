import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { Login } from "./pages/Login";
import { TeamManagement } from "./pages/TeamManagement";
import { AuthProvider, useAuth } from "./contexts/AuthContext";

/**
 * Guarda de Rota (Private Route):
 * Verifica se há token. Se 'requiredRole' for passado, verifica se o utilizador tem esse nível de acesso.
 */
const PrivateRoute: React.FC<{ children: React.ReactNode; requiredRole?: string }> = ({ children, requiredRole }) => {
  const { token, user, isLoadingAuth } = useAuth();
  
  if (isLoadingAuth) {
    return <div style={{ display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center' }}><h2>A validar credenciais... ⏳</h2></div>;
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  // O fragmento <> encapsula o ReactNode para evitar erros de renderização
  return <>{children}</>;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<Login />} />
          
          <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />

          <Route path="/team" element={
            <PrivateRoute requiredRole="SUPER_ADMIN">
              <TeamManagement />
            </PrivateRoute>
          } />
          
          <Route path="*" element={
            <div style={{ padding: "2rem", textAlign: "center" }}><h2>404 - Rota não encontrada ⛅</h2></div>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}