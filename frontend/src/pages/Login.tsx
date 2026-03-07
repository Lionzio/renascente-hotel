import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { Button } from '../components/atoms/Button';

export const Login: React.FC = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const formData = new URLSearchParams();
      formData.append('username', name.trim()); 
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      await login(response.data.access_token);
      navigate('/dashboard'); 
      
    } catch (err: any) {
      console.error("[Login Debug] Falha de credenciais:", err);
      setError(err.response?.data?.detail || 'Erro ao fazer login. Verifique as suas credenciais.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: 'var(--bg-light)' }}>
      <form onSubmit={handleLogin} style={{ background: '#fff', padding: '3rem', borderRadius: '12px', boxShadow: '0 10px 25px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ color: 'var(--sun-primary)', margin: 0 }}>Renascente Hotel</h1>
          <p style={{ color: 'var(--text-main)', marginTop: '0.5rem' }}>Acesso Restrito ☀️</p>
        </div>

        {error && <div style={{ background: '#FDEDEC', color: '#E74C3C', padding: '0.75rem', borderRadius: '8px', textAlign: 'center', fontSize: '0.9rem', fontWeight: 'bold' }}>{error}</div>}

        <input 
          type="text" 
          placeholder="Nome do Funcionário" 
          value={name} 
          onChange={e => setName(e.target.value)} 
          required 
          style={{ padding: '0.75rem', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem' }} 
        />
        
        <input 
          type="password" 
          placeholder="Palavra-passe" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
          required 
          style={{ padding: '0.75rem', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem' }} 
        />

        <Button label="Entrar" type="submit" isLoading={isLoading} />
      </form>
    </div>
  );
};