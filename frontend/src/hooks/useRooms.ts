import { useState, useEffect, useCallback } from "react";
import { api } from "../services/api";
import type { Room } from "../types/room";

export const useRooms = () => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRooms = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.get("/rooms/");
      setRooms(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Falha ao sincronizar com o servidor solar. ⛅");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRooms();
  }, [fetchRooms]);

  return { rooms, isLoading, error, refetchRooms: fetchRooms };
};