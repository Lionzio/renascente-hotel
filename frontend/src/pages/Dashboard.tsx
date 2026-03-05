import React from "react";
import { useRooms } from "../hooks/useRooms";
import { RoomGrid } from "../components/organisms/RoomGrid";
import { Button } from "../components/atoms/Button";

export const Dashboard: React.FC = () => {
  // Consome a lógica de requisição isolada no Hook
  const { rooms, isLoading, error, refetchRooms } = useRooms();

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "2px solid var(--sun-secondary)", paddingBottom: "1rem" }}>
        <div>
          <h1 style={{ margin: 0, color: "var(--sun-primary)" }}>Dashboard Operacional ☀️</h1>
          <p style={{ margin: "0.5rem 0 0 0", color: "var(--text-main)" }}>Gestão do Renascente Hotel</p>
        </div>
        
        <Button 
          label="Sincronizar" 
          onClick={refetchRooms} 
          isLoading={isLoading} 
        />
      </header>

      <main>
        {/* Tratamento de Erro Amigável e Estado de Carregamento Explícito */}
        {error && (
          <div style={{ backgroundColor: "#FDEDEC", color: "#E74C3C", padding: "1rem", borderRadius: "8px", marginTop: "2rem" }}>
            <strong>Erro:</strong> {error}
          </div>
        )}

        {isLoading && !error ? (
          <div style={{ textAlign: "center", padding: "4rem" }}>
            <h2 style={{ color: "var(--sun-primary)" }}>⏳ Carregando quartos...</h2>
            <p>Conectando ao servidor solar...</p>
          </div>
        ) : (
          !error && <RoomGrid rooms={rooms} />
        )}
      </main>
    </div>
  );
};
