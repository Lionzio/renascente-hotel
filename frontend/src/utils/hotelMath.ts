// Data oficial do sistema (Recife-PE UTC-3) para cálculos estáticos
export const CURRENT_DATE = new Date("2026-03-07T14:00:00.000Z"); 

export const hotelMath = {
  // Calcula a quantidade de diárias com base nas horas passadas (arredonda para cima)
  calculateStayDays: (checkInDateString: string): number => {
    const checkInDate = new Date(checkInDateString);
    const timeDifferenceMs = CURRENT_DATE.getTime() - checkInDate.getTime();
    const hours = timeDifferenceMs / (1000 * 60 * 60);
    return Math.max(1, Math.ceil(hours / 24));
  },

  // Formata o extrato exatamente no padrão solicitado pelo gerente
  formatConsumptionItem: (c: any, defaultConsumer: string): string => {
    const parts = c.item_name.split(" || ");
    const consumerName = parts.length > 1 ? parts[0] : defaultConsumer;
    const itemName = parts.length > 1 ? parts[1] : c.item_name;
    const totalValue = (c.price * c.quantity).toFixed(2).replace('.', ',');
    
    const dateObj = c.timestamp ? new Date(c.timestamp) : CURRENT_DATE;
    const dateStr = dateObj.toLocaleDateString("pt-BR", { timeZone: 'America/Recife' });
    const timeStr = dateObj.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", timeZone: 'America/Recife' });

    // Padrão: 07/03/2026 às 12:13h - Renato - Água mineral 250ml - 3 - R$6,00
    return `${dateStr} às ${timeStr}h - ${consumerName} - ${itemName} - ${c.quantity} - R$${totalValue}`;
  }
};