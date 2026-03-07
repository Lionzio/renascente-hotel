export interface Consumption {
  id: string;
  item_name: string;
  price: number;
  quantity: number;
  timestamp: string;
}

export interface Stay {
  id: string;
  room_id: string;
  guest_name: string;
  check_in: string;
  check_out: string | null;
  is_active: boolean;
  total_amount: number;
  is_paid: boolean; // NOVO: Mapeamento de Fatura
  consumptions: Consumption[];
}