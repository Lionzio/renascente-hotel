import React, { useState } from 'react'
import { Button } from './components/atoms/Button'

export default function App() {
  const [loading, setLoading] = useState(false)

  const handleTestClick = () => {
    setLoading(true)
    setTimeout(() => setLoading(false), 2000)
  }

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Bem-vindo ao Renascente Hotel ☀️⛅</h1>
      <p>O Design System está funcionando!</p>
      <Button 
        label="Testar Botão Solar" 
        onClick={handleTestClick} 
        isLoading={loading} 
      />
    </div>
  )
}
