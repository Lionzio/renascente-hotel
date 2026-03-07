import React from "react";
import type { Room } from "../../types/room";

interface RoomCardProps {
  room: Room;
  onClick: (room: Room) => void;
}

export const RoomCard: React.FC<RoomCardProps> = ({ room, onClick }) => {
  const getStatusDisplay = (status: string) => {
    const statusMap: Record<string, { label: string; color: string }> = {
      FREE: { label: "Livre", color: "var(--status-free, #2ECC71)" },
      OCCUPIED: { label: "Ocupado", color: "var(--status-occupied, #E74C3C)" },
      TO_BE_CLEANED: { label: "A Arrumar", color: "#F39C12" },
      TO_BE_VACATED: { label: "Em Check-out", color: "#8E44AD" },
      MAINTENANCE: { label: "Manutenção", color: "var(--status-maintenance, #95A5A6)" },
    };
    return statusMap[status] || { label: "Desconhecido", color: "#333" };
  };

  const currentStatus = getStatusDisplay(room.status);
  const activeNotes = room.notes?.filter(n => !n.is_resolved) || [];

  return (
    <div 
      onClick={() => onClick(room)} 
      style={{
        border: "1px solid #E0E0E0", borderRadius: "12px", padding: "1.5rem",
        backgroundColor: "#FFFFFF", boxShadow: "0 4px 6px rgba(0,0,0,0.05)",
        display: "flex", flexDirection: "column", gap: "0.5rem",
        borderTop: `4px solid ${currentStatus.color}`, cursor: "pointer",
        transition: "transform 0.2s"
      }}
      onMouseOver={(e) => e.currentTarget.style.transform = "translateY(-5px)"}
      onMouseOut={(e) => e.currentTarget.style.transform = "translateY(0)"}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h3 style={{ margin: 0, color: "var(--sun-primary)" }}>Quarto {room.number}</h3>
        <span style={{ backgroundColor: currentStatus.color, color: "white", padding: "0.25rem 0.5rem", borderRadius: "4px", fontSize: "0.8rem", fontWeight: "bold" }}>
          {currentStatus.label}
        </span>
      </div>

      {activeNotes.length > 0 && (
        <div style={{ background: "#FFF9C4", padding: "0.5rem", borderRadius: "6px", fontSize: "0.8rem", color: "#F39C12", marginTop: "0.5rem" }}>
          🔔 <strong>Aviso:</strong> {activeNotes[0].content.substring(0, 30)}...
          {activeNotes.length > 1 && ` (+${activeNotes.length - 1})`}
        </div>
      )}
      
      <p style={{ margin: "0.5rem 0 0 0", color: "var(--text-main)" }}>
        <strong>Capacidade:</strong> {room.capacity} {room.capacity === 1 ? 'Pessoa' : 'Pessoas'}
      </p>
      
      <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
        {room.has_ac && <span title="Ar Condicionado">❄️</span>}
        {room.has_breakfast && <span title="Café da Manhã">☕</span>}
      </div>
    </div>
  );
};