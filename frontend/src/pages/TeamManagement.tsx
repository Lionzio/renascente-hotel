import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Button } from '../components/atoms/Button';
import type { User } from '../types/user';
import { useNavigate } from 'react-router-dom';

export const TeamManagement: React.FC = () => {
  const [team, setTeam] = useState<User[]>([]);
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('EMPLOYEE');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchTeam = async () => {
    try {
      const res = await api.get('/users/');
      setTeam(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Falha ao carregar equipa.");
    }
  };

  useEffect(() => { fetchTeam(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      await api.post('/users/', { name: name.trim(), password, role });
      setName(''); setPassword('');
      await fetchTeam();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao criar funcionário.');
    } finally { setIsLoading(false); }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem a certeza que deseja excluir este membro do sistema?')) {
      try {
        await api.delete(`/users/${id}`);
        await fetchTeam();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Erro ao excluir.');
      }
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', borderBottom: '2px solid var(--sun-secondary)', paddingBottom: '1rem' }}>
        <div>
           <h2 style={{ margin: 0, color: 'var(--sun-primary)' }}>Gestão de Equipa</h2>
           <p style={{ margin: '0.5rem 0 0 0', color: 'var(--text-main)' }}>Painel de Administração Suprema</p>
        </div>
        <Button label="Voltar ao Dashboard" onClick={() => navigate('/dashboard')} variant="secondary" />
      </div>

      {error && <div style={{ backgroundColor: "#FDEDEC", color: "#E74C3C", padding: "1rem", borderRadius: "8px", marginBottom: "2rem" }}><strong>Aviso:</strong> {error}</div>}

      <form onSubmit={handleCreate} style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', display: 'flex', gap: '1rem', marginBottom: '2rem', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', flexWrap: 'wrap' }}>
        <div style={{ flex: '1 1 200px' }}>
          <input type="text" placeholder="Nome Completo" value={name} onChange={e=>setName(e.target.value)} required style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
        </div>
        <div style={{ flex: '1 1 200px' }}>
          <input type="password" placeholder="Senha de Acesso" value={password} onChange={e=>setPassword(e.target.value)} required style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
        </div>
        <div style={{ flex: '1 1 150px' }}>
          <select value={role} onChange={e=>setRole(e.target.value)} style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}>
            <option value="EMPLOYEE">Funcionário Normal</option>
            <option value="MANAGER">Gerente</option>
          </select>
        </div>
        <Button label="Adicionar" type="submit" isLoading={isLoading} />
      </form>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {team.map(member => (
          <li key={member.id} style={{ background: '#fff', padding: '1rem', marginBottom: '0.75rem', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', borderLeft: `4px solid ${member.role === 'SUPER_ADMIN' ? '#8E44AD' : member.role === 'MANAGER' ? '#F39C12' : '#3498DB'}` }}>
            <div>
              <strong style={{ fontSize: '1.1rem' }}>{member.name}</strong>
              <span style={{ display: 'block', fontSize: '0.85rem', color: '#666', marginTop: '0.25rem' }}>Perfil: {member.role}</span>
            </div>
            {member.role !== 'SUPER_ADMIN' && (
              <button onClick={() => handleDelete(member.id)} style={{ background: 'none', border: 'none', color: '#E74C3C', cursor: 'pointer', fontWeight: 'bold' }}>Remover</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};