import { useState, useCallback } from "react";
import { api } from "../services/api";
import type { Stay } from "../types/stay";

export const useStays = () => {
  const [activeStay, setActiveStay] = useState<Stay | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchActiveStay = useCallback(async (roomId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.get(`/stays/room/${roomId}/active`);
      setActiveStay(response.data);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setActiveStay(null);
      } else {
        setError(err.response?.data?.detail || "Erro ao buscar hospedagem.");
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const checkIn = async (roomId: string, guestName: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.post("/stays/checkin", { room_id: roomId, guest_name: guestName });
      await fetchActiveStay(roomId);
      return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao realizar check-in.");
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const addConsumptionAI = async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.post("/ai/parse-consumption", { text });
      if (activeStay) await fetchActiveStay(activeStay.room_id);
      return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro na comunicação com a IA.");
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const addConsumptionManual = async (stayId: string, roomId: string, itemName: string, price: number, quantity: number) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.post("/stays/consumption", {
        stay_id: stayId,
        item_name: itemName,
        price: price,
        quantity: quantity,
      });
      await fetchActiveStay(roomId);
      return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao registrar consumo manual.");
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  // --- NOVA FUNÇÃO DE CHECK-OUT ---
  const checkOut = async (stayId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.post(`/stays/${stayId}/checkout`);
      setActiveStay(null); // Limpa a estadia ativa, pois o hóspede foi embora
      return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao realizar check-out.");
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  return { activeStay, isLoading, error, fetchActiveStay, checkIn, checkOut, addConsumptionAI, addConsumptionManual };
};