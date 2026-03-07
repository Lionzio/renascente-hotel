import React from "react";
import type { Room } from "../../types/room";
import { RoomCard } from "../molecules/RoomCard";

interface RoomGridProps {
  rooms: Room[];
  onRoomClick: (room: Room) => void;
}

export const RoomGrid: React.FC<RoomGridProps> = ({ rooms, onRoomClick }) => {
  // Blindagem: Garante que não vai quebrar se a API retornar algo inesperado
  if (!rooms || rooms.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "2rem", color: "#7F8C8D" }}>
        <p>Nenhum quarto cadastrado ainda. O hotel está vazio! 🌅</p>
      </div>
    );
  }

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
      gap: "1.5rem",
      marginTop: "2rem"
    }}>
      {rooms.map((room) => (
        <RoomCard 
          key={room.id} 
          room={room} 
          onClick={onRoomClick} 
        />
      ))}
    </div>
  );
};