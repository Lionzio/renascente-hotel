import axios from "axios";

/**
 * Instância global do Axios apontando para o nosso backend (Porta 8001).
 * Centraliza a comunicação HTTP e aplica o DRY (Don't Repeat Yourself).
 */
export const api = axios.create({
  baseURL: "http://localhost:8001/api/v1",
  timeout: 10000, // Timeout de 10 segundos (útil para quando a IA demorar a processar)
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptador de Resposta: Tratamento Global de Erros
api.interceptors.response.use(
  (response) => {
    // Se a requisição deu certo, apenas retorna os dados
    return response;
  },
  (error) => {
    // Aqui capturamos erros 400, 404, 500 ou quedas de rede antes do componente saber
    const errorMessage = error.response?.data?.detail || "Erro de conexão com o servidor. O sol se escondeu atrás das nuvens ⛅.";
    
    // Em uma Sprint futura, podemos acoplar um Toast (Aviso em tela) aqui
    console.error("[Axios Interceptor] Erro Global:", errorMessage);
    
    return Promise.reject(error);
  }
);
