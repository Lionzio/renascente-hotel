import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";

/**
 * Raiz da Aplicação (SPA).
 * Gerencia o roteamento entre páginas sem recarregar o navegador.
 */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota padrão redireciona para o Dashboard */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        
        {/* Rota principal de gestão de quartos */}
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* Rota de fallback (404 Not Found) */}
        <Route path="*" element={
          <div style={{ padding: "2rem", textAlign: "center" }}>
            <h2>404 - Rota não encontrada ⛅</h2>
          </div>
        } />
      </Routes>
    </BrowserRouter>
  );
}
