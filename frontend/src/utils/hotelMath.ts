export const hotelMath = {
  // Usa o tempo dinâmico atual
  calculateStayDays: (checkInDateString: string): number => {
    const checkInDate = new Date(checkInDateString);
    const timeDifferenceMs = new Date().getTime() - checkInDate.getTime();
    const hours = timeDifferenceMs / (1000 * 60 * 60);
    return Math.max(1, Math.ceil(hours / 24));
  },

  formatConsumptionItem: (c: any, defaultConsumer: string): string => {
    const parts = c.item_name.split(" || ");
    const consumerName = parts.length > 1 ? parts[0] : defaultConsumer;
    const itemName = parts.length > 1 ? parts[1] : c.item_name;
    const totalValue = (c.price * c.quantity).toFixed(2).replace('.', ',');
    
    const dateObj = c.timestamp ? new Date(c.timestamp) : new Date();
    const dateStr = dateObj.toLocaleDateString("pt-BR", { timeZone: 'America/Recife' });
    const timeStr = dateObj.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", timeZone: 'America/Recife' });

    return `${dateStr} às ${timeStr}h - ${consumerName} - ${itemName} - ${c.quantity} - R$${totalValue}`;
  }
};