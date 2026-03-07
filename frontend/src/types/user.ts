export type UserRole = "EMPLOYEE" | "MANAGER" | "SUPER_ADMIN";

export interface User {
  id: string;
  name: string;
  role: UserRole;
}