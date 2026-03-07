import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import type { User } from '../types/user';

interface AuthContextData {
  user: User | null;
  token: string | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
  isLoadingAuth: boolean;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);

  useEffect(() => {
    const storagedToken = localStorage.getItem('@Renascente:token');
    
    if (storagedToken) {
      api.defaults.headers.common['Authorization'] = `Bearer ${storagedToken}`;
      setToken(storagedToken);
      
      api.get('/auth/me')
        .then(response => {
          setUser(response.data);
        })
        .catch((err) => {
          console.error("[Auth Debug] Token inválido ou expirado.", err);
          logout(); 
        })
        .finally(() => {
          setIsLoadingAuth(false);
        });
    } else {
      setIsLoadingAuth(false);
    }
  }, []);

  const login = async (newToken: string) => {
    localStorage.setItem('@Renascente:token', newToken);
    api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    setToken(newToken);
    
    try {
      const response = await api.get('/auth/me');
      setUser(response.data);
    } catch (err) {
      console.error("[Auth Debug] Falha ao recuperar perfil após login.", err);
      logout();
    }
  };

  const logout = () => {
    localStorage.removeItem('@Renascente:token');
    delete api.defaults.headers.common['Authorization'];
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoadingAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);