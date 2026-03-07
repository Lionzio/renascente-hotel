import React, { useState } from "react";
import { Button } from "../atoms/Button";
import type { Room } from "../../types/room";
import type { Stay } from "../../types/stay";
import { hotelMath, CURRENT_DATE } from "../../utils/hotelMath";

const inputStyle: React.CSSProperties = {
  padding: "0.5rem", borderRadius: "8px", border: "1px solid #ccc", width: "100%", boxSizing: "border-box"
};

// ==========================================================
// 1. PAINEL DE EDIÇÃO DE QUARTO
// ==========================================================
interface EditRoomPanelProps {
  room: Room;
  onSave: (num: string, cap: number, ac: boolean, brk: boolean) => void;
  onCancel: () => void;
  isLoading: boolean;
}

export const EditRoomPanel: React.FC<EditRoomPanelProps> = ({ room, onSave, onCancel, isLoading }) => {
  const [num, setNum] = useState(room.number);
  const [cap, setCap] = useState(room.capacity.toString());
  const [ac, setAc] = useState(room.has_ac);
  const [brk, setBrk] = useState(room.has_breakfast);

  return (
    <div style={{ background: "#fdf2e9", padding: "1.5rem", borderRadius: "8px", marginBottom: "1rem", border: "1px dashed #e67e22" }}>
      <h3 style={{ margin: "0 0 1rem 0", color: "#d35400" }}>Editar Quarto {room.number}</h3>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "1rem" }}>
        <div><label style={{ fontSize: "0.85rem", color: "#666" }}>Número</label><input type="text" value={num} onChange={e => setNum(e.target.value)} style={inputStyle} /></div>
        <div><label style={{ fontSize: "0.85rem", color: "#666" }}>Capacidade</label><input type="number" value={cap} onChange={e => setCap(e.target.value)} style={inputStyle} /></div>
      </div>
      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
        <label><input type="checkbox" checked={ac} onChange={e => setAc(e.target.checked)} /> Ar Condicionado</label>
        <label><input type="checkbox" checked={brk} onChange={e => setBrk(e.target.checked)} /> Café da Manhã</label>
      </div>
      <div style={{ display: "flex", gap: "1rem" }}>
        <Button label="Salvar Alterações" onClick={() => onSave(num, parseInt(cap), ac, brk)} isLoading={isLoading} />
        <Button label="Cancelar" onClick={onCancel} variant="secondary" />
      </div>
    </div>
  );
};

// ==========================================================
// 2. PAINEL DE CHECK-IN (SIMULADOR DE PREVISÃO)
// ==========================================================
interface FreeRoomPanelProps {
  room: Room;
  onCheckIn: (guestName: string, rate: string) => void;
  isLoading: boolean;
}

export const FreeRoomPanel: React.FC<FreeRoomPanelProps> = ({ room, onCheckIn, isLoading }) => {
  const [guestName, setGuestName] = useState("");
  const [previewCheckIn, setPreviewCheckIn] = useState(CURRENT_DATE.toISOString().split("T")[0]);
  const [previewCheckOut, setPreviewCheckOut] = useState("");
  const [previewRate, setPreviewRate] = useState("150");

  const calculatePreviewDays = () => {
    if (!previewCheckIn || !previewCheckOut) return 0;
    const start = new Date(previewCheckIn); 
    const end = new Date(previewCheckOut);
    if (end <= start) return 0;
    return Math.ceil(Math.abs(end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
  };

  const previewDays = calculatePreviewDays();
  const previewTotal = previewDays * parseFloat(previewRate || "0");

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <div style={{ background: "#f8f9fa", padding: "1rem", borderRadius: "8px", fontSize: "0.9rem" }}>
        <strong>Características do Quarto:</strong>
        <div style={{ display: "flex", gap: "1rem", marginTop: "0.5rem" }}>
          <span>👤 Capacidade: {room.capacity}</span>
          <span>❄️ Ar Condicionado: {room.has_ac ? "Sim" : "Não"}</span>
          <span>☕ Café da Manhã: {room.has_breakfast ? "Sim" : "Não"}</span>
        </div>
      </div>
      <h3 style={{ margin: "0.5rem 0 0 0" }}>Nova Hospedagem</h3>
      <input type="text" value={guestName} onChange={e => setGuestName(e.target.value)} placeholder="Nome completo do hóspede titular" style={inputStyle} />
      
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <div style={{ flex: 1 }}><label style={{ fontSize: "0.85rem", color: "#666" }}>Check-in</label><input type="date" value={previewCheckIn} onChange={e => setPreviewCheckIn(e.target.value)} style={inputStyle} /></div>
        <div style={{ flex: 1 }}><label style={{ fontSize: "0.85rem", color: "#666" }}>Check-out (Previsto)</label><input type="date" value={previewCheckOut} onChange={e => setPreviewCheckOut(e.target.value)} style={inputStyle} min={previewCheckIn} /></div>
      </div>
      <div>
        <label style={{ fontSize: "0.85rem", color: "#666" }}>Valor da Diária Negociada (R$)</label>
        <input type="number" value={previewRate} onChange={e => setPreviewRate(e.target.value)} style={inputStyle} />
      </div>

      {previewCheckOut && previewDays > 0 && (
        <div style={{ background: "#FFF3E0", padding: "1rem", borderRadius: "8px", border: "1px dashed var(--sun-primary)", textAlign: "center" }}>
          <p style={{ margin: "0 0 0.5rem 0", color: "#666" }}>Previsão de Pagamento ({previewDays} diárias)</p>
          <h3 style={{ margin: 0, color: "var(--sun-primary)" }}>R$ {previewTotal.toFixed(2).replace('.', ',')}</h3>
          <small style={{ color: "#999" }}>*O consumo será adicionado no fechamento da conta</small>
        </div>
      )}
      <Button label="Confirmar Check-in" onClick={() => onCheckIn(guestName, previewRate)} isLoading={isLoading} />
    </div>
  );
};

// ==========================================================
// 3. PAINEL: QUARTO OCUPADO E TOTAL AO VIVO
// ==========================================================
interface OccupiedRoomPanelProps {
  stay: Stay;
  dailyRate: string;
  stayDays: number;
  stayCost: number;
  totalAmountLive: number;
  onAiSubmit: (text: string) => void;
  onManualSubmit: (consumer: string, item: string, price: string, qty: string) => void;
  onCheckoutRequest: () => void;
  isLoading: boolean;
}

export const OccupiedRoomPanel: React.FC<OccupiedRoomPanelProps> = ({ 
  stay, dailyRate, stayDays, stayCost, totalAmountLive, onAiSubmit, onManualSubmit, onCheckoutRequest, isLoading 
}) => {
  const [aiText, setAiText] = useState("");
  const [showManual, setShowManual] = useState(false);
  const [consumer, setConsumer] = useState(stay.guest_name || "");
  const [item, setItem] = useState("");
  const [price, setPrice] = useState("");
  const [qty, setQty] = useState("1");

  const handleSubmitManual = () => {
    if (!item || !price) return;
    onManualSubmit(consumer, item, price, qty);
    setItem(""); setPrice(""); setQty("1");
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem" }}>
        <div>
          <h3 style={{ margin: "0 0 0.25rem 0" }}>Hóspede Titular: {stay.guest_name}</h3>
          <span style={{ fontSize: "0.85rem", color: "#666" }}>Entrada: {new Date(stay.check_in).toLocaleString("pt-BR")}</span>
        </div>
        <Button label="Ir para Check-out" onClick={onCheckoutRequest} variant="secondary" />
      </div>

      <div style={{ background: "#e8f5e9", padding: "1.2rem", borderRadius: "12px", marginBottom: "1.5rem", border: "2px solid #2ecc71" }}>
        <h2 style={{ margin: 0, color: "#27ae60", display: "flex", justifyContent: "space-between" }}>
          <span>Total a pagar ao vivo:</span>
          <span>R$ {totalAmountLive.toFixed(2).replace('.', ',')}</span>
        </h2>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.9rem", color: "#555", marginTop: "0.5rem" }}>
          <span>Diárias ({stayDays}x R${dailyRate}): R$ {stayCost.toFixed(2).replace('.', ',')}</span>
          <span>Consumo Extra: R$ {stay.total_amount.toFixed(2).replace('.', ',')}</span>
        </div>
      </div>

      <div style={{ background: "#f8f9fa", padding: "1rem", borderRadius: "8px", marginBottom: "1rem" }}>
        <h4 style={{ margin: "0 0 0.5rem 0" }}>Cérebro IA 🧠</h4>
        <textarea value={aiText} onChange={e=>setAiText(e.target.value)} placeholder="Ex: Pode anotar duas águas de 5 reais..." rows={2} style={{...inputStyle, marginBottom: "0.5rem"}} />
        <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
          <Button label="Registrar IA" onClick={() => { onAiSubmit(aiText); setAiText(""); }} isLoading={isLoading} />
          <button onClick={() => setShowManual(!showManual)} style={{ background: "none", border: "none", color: "#3498db", textDecoration: "underline", cursor: "pointer", fontSize: "0.9rem" }}>{showManual ? "Ocultar Manual" : "Lançamento Manual"}</button>
        </div>
      </div>

      {showManual && (
        <div style={{ background: "#FFF3E0", padding: "1rem", borderRadius: "8px", marginBottom: "1.5rem", border: "1px dashed var(--sun-primary)" }}>
          <h4 style={{ margin: "0 0 0.5rem 0", color: "var(--sun-primary)" }}>Lançamento Manual ✍️</h4>
          <input type="text" placeholder="Consumidor (Ex: Renato)" value={consumer} onChange={e=>setConsumer(e.target.value)} style={{...inputStyle, marginBottom: "0.5rem"}} />
          <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.5rem" }}>
            <input type="text" placeholder="Item" value={item} onChange={e=>setItem(e.target.value)} style={{...inputStyle, flex: 2}} />
            <input type="number" placeholder="R$" value={price} onChange={e=>setPrice(e.target.value)} style={{...inputStyle, flex: 1}} />
            <input type="number" placeholder="Qtd" value={qty} onChange={e=>setQty(e.target.value)} style={{...inputStyle, width: "60px"}} />
          </div>
          <Button label="Adicionar Item" onClick={handleSubmitManual} isLoading={isLoading} variant="secondary" />
        </div>
      )}

      <h4 style={{ borderBottom: "1px solid #ccc", paddingBottom: "0.5rem" }}>Extrato Detalhado de Consumo:</h4>
      {stay.consumptions.length === 0 ? <p style={{ color: "#999", fontSize: "0.9rem" }}>Nenhum consumo registrado.</p> : (
        <ul style={{ paddingLeft: "1.2rem", margin: 0, maxHeight: "200px", overflowY: "auto", color: "#444" }}>
          {stay.consumptions.map((c: any) => (
            <li key={c.id} style={{ marginBottom: "0.5rem", fontSize: "0.95rem" }}>
              {hotelMath.formatConsumptionItem(c, stay.guest_name)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

// ==========================================================
// 4. PAINEL DE CHECK-OUT FINAL
// ==========================================================
interface CheckoutPanelProps {
  stay: Stay;
  stayDays: number;
  dailyRate: string;
  setDailyRate: (val: string) => void;
  stayCost: number;
  totalAmountLive: number;
  onCancel: () => void;
  onConfirm: () => void;
  isLoading: boolean;
}

export const CheckoutPanel: React.FC<CheckoutPanelProps> = ({ 
  stay, stayDays, dailyRate, setDailyRate, stayCost, totalAmountLive, onCancel, onConfirm, isLoading 
}) => {
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h3 style={{ margin: 0 }}>Fatura Final</h3>
        <button onClick={onCancel} style={{ background: "none", border: "none", color: "#3498db", textDecoration: "underline", cursor: "pointer" }}>Voltar</button>
      </div>
      
      <div style={{ background: "#f8f9fa", padding: "1rem", borderRadius: "8px", marginBottom: "1.5rem" }}>
        <p><strong>Hóspede:</strong> {stay.guest_name}</p>
        <p style={{ display: "flex", justifyContent: "space-between" }}><span><strong>Permanência:</strong> {stayDays} diária(s)</span><span>Entrada: {new Date(stay.check_in).toLocaleDateString("pt-BR")}</span></p>
        <div style={{ marginTop: "1rem", borderTop: "1px solid #ddd", paddingTop: "1rem" }}>
          <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>Valor da Diária (R$):</label>
          <input type="number" value={dailyRate} onChange={e => setDailyRate(e.target.value)} style={{...inputStyle, width: "150px", fontSize: "1.1rem" }} />
        </div>
      </div>

      <div style={{ background: "#2C3E50", color: "#fff", padding: "1.5rem", borderRadius: "8px", marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}><span>Diárias ({stayDays}x R$ {parseFloat(dailyRate||"0").toFixed(2)}):</span><span>R$ {stayCost.toFixed(2).replace('.', ',')}</span></div>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem", borderBottom: "1px solid #4a627a", paddingBottom: "0.5rem" }}><span>Consumo Extra:</span><span>R$ {stay.total_amount.toFixed(2).replace('.', ',')}</span></div>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "1.5rem", fontWeight: "bold", marginTop: "1rem" }}><span>Total a Pagar:</span><span style={{ color: "var(--sun-secondary)" }}>R$ {totalAmountLive.toFixed(2).replace('.', ',')}</span></div>
      </div>
      <Button label="Registrar Pagamento e Liberar Quarto" onClick={onConfirm} isLoading={isLoading} />
    </div>
  );
};