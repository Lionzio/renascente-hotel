import { useState, useEffect, useCallback } from "react";
import { api } from "../services/api";
import type { Room } from "../types/room";

export const useRooms = () => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRooms = useCallback(async () => {
    setIsLoading(true); setError(null);
    try {
      const response = await api.get("/rooms/");
      setRooms(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Falha ao sincronizar quartos.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const addRoom = async (number: string, capacity: number, has_ac: boolean, has_breakfast: boolean) => {
    setIsLoading(true); setError(null);
    try {
      await api.post("/rooms/", { number, capacity, has_ac, has_breakfast, status: "FREE" });
      await fetchRooms(); return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao criar novo quarto."); return false;
    } finally { setIsLoading(false); }
  };

  const editRoom = async (id: string, number: string, capacity: number, has_ac: boolean, has_breakfast: boolean) => {
    setIsLoading(true); setError(null);
    try {
      await api.put(`/rooms/${id}`, { number, capacity, has_ac, has_breakfast, status: "FREE" });
      await fetchRooms(); return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao atualizar o quarto."); return false;
    } finally { setIsLoading(false); }
  };

  const deleteRoom = async (id: string) => {
    setIsLoading(true); setError(null);
    try {
      await api.delete(`/rooms/${id}`);
      await fetchRooms(); return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao excluir o quarto."); return false;
    } finally { setIsLoading(false); }
  };

  useEffect(() => { fetchRooms(); }, [fetchRooms]);

  return { rooms, isLoading, error, refetchRooms: fetchRooms, addRoom, editRoom, deleteRoom };
};