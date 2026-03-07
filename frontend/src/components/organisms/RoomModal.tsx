import React, { useEffect, useState } from "react";
import type { Room } from "../../types/room";
import { useStays } from "../../hooks/useStays";
import { useRooms } from "../../hooks/useRooms";
import { useOperations } from "../../hooks/useOperations";
import { EditRoomPanel, FreeRoomPanel, OccupiedRoomPanel, CheckoutPanel, HousekeepingPanel, MaintenancePanel, NotesSection } from "./RoomPanels";
import { hotelMath } from "../../utils/hotelMath";

interface RoomModalProps {
  isOpen: boolean;
  onClose: () => void;
  room: Room | null;
  onRoomUpdated: () => void;
}

export const RoomModal: React.FC<RoomModalProps> = ({ isOpen, onClose, room, onRoomUpdated }) => {
  const { activeStay, isLoading: stayLoading, error: stayError, fetchActiveStay, checkIn, checkOut, addConsumptionAI, addConsumptionManual } = useStays();
  const { editRoom, deleteRoom, isLoading: roomLoading, error: roomError } = useRooms();
  const { registerCleaning, registerMaintenance, finishMaintenance, addNote, resolveNote } = useOperations(onRoomUpdated);
  
  const [isEditingRoom, setIsEditingRoom] = useState(false);
  const [isCheckoutMode, setIsCheckoutMode] = useState(false);
  const [dailyRate, setDailyRate] = useState("150");

  useEffect(() => {
    if (isOpen && room) {
      if (room.status === "OCCUPIED") {
        fetchActiveStay(room.id);
        setIsCheckoutMode(false);
      }
      setIsEditingRoom(false);
    }
  }, [isOpen, room, fetchActiveStay]);

  if (!isOpen || !room) return null;

  const stayDays = activeStay ? hotelMath.calculateStayDays(activeStay.check_in) : 0;
  const stayCost = stayDays * parseFloat(dailyRate || "0");
  const totalAmountLive = activeStay ? (stayCost + activeStay.total_amount) : 0;

  const handleEditSave = async (num: string, cap: number, ac: boolean, brk: boolean) => {
    const success = await editRoom(room.id, num, cap, ac, brk);
    if (success) { setIsEditingRoom(false); onRoomUpdated(); onClose(); }
  };

  const handleDelete = async () => {
    if (window.confirm(`Tem certeza que deseja excluir o Quarto ${room.number}?`)) {
      const success = await deleteRoom(room.id);
      if (success) { onRoomUpdated(); onClose(); }
    }
  };

  const handleCheckIn = async (guestName: string, negotiatedRate: string) => {
    const success = await checkIn(room.id, guestName);
    if (success) { setDailyRate(negotiatedRate); onRoomUpdated(); onClose(); }
  };

  const handleManualConsumption = async (consumer: string, item: string, price: string, qty: string) => {
    if (!activeStay) return;
    const finalItemName = `${consumer.trim() || activeStay.guest_name} || ${item.trim()}`;
    await addConsumptionManual(activeStay.id, room.id, finalItemName, parseFloat(price), parseInt(qty, 10));
  };

  const handleCheckoutFinal = async () => {
    if (!activeStay) return;
    const success = await checkOut(activeStay.id);
    if (success) { onRoomUpdated(); onClose(); }
  };

  // LIBERAÇÃO ESTRATÉGICA DE CRUD:
  // Quartos podem ser editados ou apagados se estiverem Livres, Em Manutenção ou A Arrumar.
  // Somente quartos com Hóspedes são bloqueados fisicamente.
  const canEditOrDelete = room.status === "FREE" || room.status === "TO_BE_CLEANED" || room.status === "MAINTENANCE";

  const overlayStyle: React.CSSProperties = { position: "fixed", top: 0, left: 0, right: 0, bottom: 0, backgroundColor: "rgba(0, 0, 0, 0.5)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000 };
  const modalStyle: React.CSSProperties = { backgroundColor: "#fff", padding: "2rem", borderRadius: "12px", width: "90%", maxWidth: "600px", maxHeight: "90vh", overflowY: "auto", boxShadow: "0 10px 25px rgba(0,0,0,0.2)" };

  return (
    <div style={overlayStyle}>
      <div style={modalStyle}>
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
          <h2 style={{ margin: 0, color: "var(--sun-primary)" }}>Quarto {room.number}</h2>
          <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
            {canEditOrDelete && !isEditingRoom && (
              <>
                <button onClick={() => setIsEditingRoom(true)} style={{ background: "none", border: "none", color: "#f39c12", cursor: "pointer", fontWeight: "bold" }}>✏️ Editar</button>
                <button onClick={handleDelete} style={{ background: "none", border: "none", color: "#e74c3c", cursor: "pointer", fontWeight: "bold" }}>🗑️ Excluir</button>
              </>
            )}
            <button onClick={onClose} style={{ background: "none", border: "none", fontSize: "1.5rem", cursor: "pointer", paddingLeft: "1rem" }}>✖</button>
          </div>
        </header>

        {(stayError || roomError) && <div style={{ color: "#E74C3C", marginBottom: "1rem", padding: "0.75rem", background: "#FDEDEC", borderRadius: "8px", fontWeight: "bold" }}>{stayError || roomError}</div>}

        {isEditingRoom && <EditRoomPanel room={room} onSave={handleEditSave} onCancel={() => setIsEditingRoom(false)} isLoading={roomLoading} />}

        {room.status === "FREE" && !isEditingRoom && (
          <FreeRoomPanel room={room} onCheckIn={handleCheckIn} isLoading={stayLoading} />
        )}

        {room.status === "OCCUPIED" && activeStay && !isCheckoutMode && (
          <OccupiedRoomPanel stay={activeStay} dailyRate={dailyRate} stayDays={stayDays} stayCost={stayCost} totalAmountLive={totalAmountLive} onAiSubmit={(text: string) => addConsumptionAI(text)} onManualSubmit={handleManualConsumption} onCheckoutRequest={() => setIsCheckoutMode(true)} isLoading={stayLoading} />
        )}

        {room.status === "OCCUPIED" && activeStay && isCheckoutMode && (
          <CheckoutPanel stay={activeStay} stayDays={stayDays} dailyRate={dailyRate} setDailyRate={setDailyRate} stayCost={stayCost} totalAmountLive={totalAmountLive} onCancel={() => setIsCheckoutMode(false)} onConfirm={handleCheckoutFinal} isLoading={stayLoading} />
        )}

        {room.status === "TO_BE_CLEANED" && !isEditingRoom && (
          <HousekeepingPanel onClean={(empName: string, date: string) => registerCleaning(room.id, empName, date)} isLoading={stayLoading} />
        )}

        {room.status === "MAINTENANCE" && !isEditingRoom && (
           <MaintenancePanel 
              onSubmit={(data: any) => registerMaintenance(room.id, data)} 
              onFinish={() => finishMaintenance(room.id)}
              isLoading={stayLoading} 
           />
        )}

        {/* Anotações visíveis em qualquer tela operacional (exceto durante a edição das paredes físicas do quarto) */}
        {!isEditingRoom && (
          <NotesSection notes={room.notes} onAdd={(content: string) => addNote(room.id, content)} onResolve={(noteId: number) => resolveNote(room.id, noteId)} />
        )}
      </div>
    </div>
  );
};