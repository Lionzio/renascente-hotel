import React, { useState } from "react";
import { useRooms } from "../hooks/useRooms";
import { RoomGrid } from "../components/organisms/RoomGrid";
import { Button } from "../components/atoms/Button";
import { RoomModal } from "../components/organisms/RoomModal";
import type { Room } from "../types/room";

export const Dashboard: React.FC = () => {
  const { rooms, isLoading, error, refetchRooms, addRoom } = useRooms();

  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  
  // Estados para criação de novo quarto
  const [showAddRoom, setShowAddRoom] = useState(false);
  const [newRoomNum, setNewRoomNum] = useState("");
  const [newRoomCap, setNewRoomCap] = useState("2");
  const [newRoomAc, setNewRoomAc] = useState(true);
  const [newRoomBrk, setNewRoomBrk] = useState(true);

  const handleRoomClick = (room: Room) => {
    setSelectedRoom(room);
    setIsModalOpen(true);
  };

  const handleCreateRoom = async () => {
    if (!newRoomNum) return;
    const success = await addRoom(newRoomNum, parseInt(newRoomCap), newRoomAc, newRoomBrk);
    if (success) {
      setNewRoomNum("");
      setShowAddRoom(false);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedRoom(null);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "2px solid var(--sun-secondary)", paddingBottom: "1rem" }}>
        <div>
          <h1 style={{ margin: 0, color: "var(--sun-primary)" }}>Dashboard Operacional ☀️</h1>
          <p style={{ margin: "0.5rem 0 0 0", color: "var(--text-main)" }}>Gestão do Renascente Hotel</p>
        </div>
        
        <div style={{ display: "flex", gap: "1rem" }}>
          <Button label="+ Novo Quarto" onClick={() => setShowAddRoom(!showAddRoom)} variant="secondary" />
          <Button label="Sincronizar" onClick={refetchRooms} isLoading={isLoading} />
        </div>
      </header>

      <main>
        {/* Formulário de Criação de Quarto */}
        {showAddRoom && (
          <div style={{ background: "#fff", padding: "1.5rem", borderRadius: "12px", marginTop: "2rem", boxShadow: "0 4px 6px rgba(0,0,0,0.05)", border: "1px solid #ddd" }}>
            <h3 style={{ margin: "0 0 1rem 0", color: "var(--sun-primary)" }}>Cadastrar Novo Quarto</h3>
            <div style={{ display: "flex", gap: "1rem", alignItems: "center", flexWrap: "wrap" }}>
              <input type="text" placeholder="Número (ex: 401)" value={newRoomNum} onChange={e => setNewRoomNum(e.target.value)} style={{ padding: "0.5rem", borderRadius: "8px", border: "1px solid #ccc" }} />
              <input type="number" placeholder="Capacidade" value={newRoomCap} onChange={e => setNewRoomCap(e.target.value)} style={{ padding: "0.5rem", borderRadius: "8px", border: "1px solid #ccc", width: "100px" }} title="Capacidade" />
              <label><input type="checkbox" checked={newRoomAc} onChange={e => setNewRoomAc(e.target.checked)} /> Ar Condicionado</label>
              <label><input type="checkbox" checked={newRoomBrk} onChange={e => setNewRoomBrk(e.target.checked)} /> Café da Manhã</label>
              <Button label="Salvar Quarto" onClick={handleCreateRoom} isLoading={isLoading} />
            </div>
          </div>
        )}

        {error && <div style={{ backgroundColor: "#FDEDEC", color: "#E74C3C", padding: "1rem", borderRadius: "8px", marginTop: "2rem" }}><strong>Erro:</strong> {error}</div>}

        {isLoading && !error ? (
          <div style={{ textAlign: "center", padding: "4rem" }}>
            <h2 style={{ color: "var(--sun-primary)" }}>⏳ Carregando quartos...</h2>
            <p>Conectando ao servidor solar...</p>
          </div>
        ) : (
          !error && <RoomGrid rooms={rooms} onRoomClick={handleRoomClick} />
        )}
      </main>

      <RoomModal isOpen={isModalOpen} onClose={closeModal} room={selectedRoom} onRoomUpdated={refetchRooms} />
    </div>
  );
};