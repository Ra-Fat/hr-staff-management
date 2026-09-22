export type Permission = string;

export interface AuthUser{
    id: string;
    name: string;
    email: string;
    role: string;
    roleId?: number;
    permissions: string[];
    // expiresAt?: string | null;
}