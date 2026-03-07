export type RoomStatus = "FREE" | "OCCUPIED" | "TO_BE_CLEANED" | "TO_BE_VACATED" | "MAINTENANCE";

export interface Note {
  id: number;
  content: string;
  is_resolved: boolean;
  created_at: string;
}

export interface Room {
  id: string;
  number: string;
  capacity: number;
  has_ac: boolean;
  has_breakfast: boolean;
  status: RoomStatus;
  notes?: Note[];
}