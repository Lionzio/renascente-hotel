// frontend/src/components/atoms/Button.tsx
import React from 'react';
import '../../styles/theme.css'; // Vamos criar as variáveis solares aqui depois

// Tipagem estrita de propriedades, evitando "any" e garantindo previsibilidade
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  isLoading?: boolean;
  variant?: 'primary' | 'secondary';
  onClick: () => void;
}

/**
 * Átomo Button: Componente base para interações do usuário.
 * Aplica feedback visual de carregamento (Loading State) e obedece ao Design System.
 */
export const Button: React.FC<ButtonProps> = ({
  label,
  isLoading = false,
  variant = 'primary',
  onClick,
  disabled,
  ...rest
}) => {
  // O estilo será alimentado por variáveis CSS para evitar cores hardcoded no JS
  const baseStyle = {
    padding: '0.75rem 1.5rem',
    borderRadius: '8px',
    border: 'none',
    fontWeight: 'bold',
    cursor: isLoading || disabled ? 'not-allowed' : 'pointer',
    opacity: isLoading || disabled ? 0.7 : 1,
    transition: 'background-color 0.3s ease, transform 0.1s ease',
    backgroundColor: variant === 'primary' ? 'var(--sun-primary)' : 'var(--sun-secondary)',
    color: variant === 'primary' ? '#FFFFFF' : '#333333',
  };

  return (
    <button 
      style={baseStyle} 
      onClick={onClick} 
      disabled={isLoading || disabled}
      {...rest}
    >
      {isLoading ? (
        <span className="loading-spinner">⏳ Processando...</span>
      ) : (
        label
      )}
    </button>
  );
};