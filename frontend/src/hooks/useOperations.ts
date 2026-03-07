import { useState } from "react";
import { api } from "../services/api";

export const useOperations = (onSuccessCallback: () => void) => {
  const [isLoading, setIsLoading] = useState(false);

  const registerCleaning = async (roomId: string, employeeName: string, cleanedAt: string) => {
    setIsLoading(true);
    try {
      await api.post(`/rooms/${roomId}/clean`, { employee_name: employeeName, cleaned_at: cleanedAt });
      onSuccessCallback();
    } finally { setIsLoading(false); }
  };

  const registerMaintenance = async (roomId: string, data: any) => {
    setIsLoading(true);
    try {
      await api.post(`/rooms/${roomId}/maintenance`, data);
      onSuccessCallback();
    } finally { setIsLoading(false); }
  };

  // Libera o quarto devolvendo-o para o estado FREE após o conserto
  const finishMaintenance = async (roomId: string) => {
    setIsLoading(true);
    try {
      await api.patch(`/rooms/${roomId}/status?new_status=FREE`);
      onSuccessCallback();
    } finally { setIsLoading(false); }
  };

  const addNote = async (roomId: string, content: string) => {
    setIsLoading(true);
    try {
      await api.post(`/rooms/${roomId}/notes`, { content });
      onSuccessCallback();
    } finally { setIsLoading(false); }
  };

  const resolveNote = async (roomId: string, noteId: number) => {
    setIsLoading(true);
    try {
      await api.patch(`/rooms/${roomId}/notes/${noteId}/resolve`);
      onSuccessCallback();
    } finally { setIsLoading(false); }
  };

  return { registerCleaning, registerMaintenance, finishMaintenance, addNote, resolveNote, isLoading };
};