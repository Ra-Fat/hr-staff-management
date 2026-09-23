"use client";

import { strFromU8, unzlibSync } from 'fflate';
import type { AuthUser } from "../types/auth.type";

const ACCESS_KEY = "fp_access_token";
const REFRESH_KEY = "fp_refresh_token";
const COOKIE_NAME = "auth-token";

const COOKIE_PRESENCE_VALUE = '1';

export interface JwtPayload {
  sub: string;
  email?: string;
  role?: string;
  role_id?: number;
  permissions?: string[];
  full_name?: string;
  exp?: number;
}

interface RawJwtPayload extends JwtPayload {
  perms_z?: string;
}

// helper function to ....
function base64UrlToBytes(text: string): Uint8Array {
  const binary = atob(text.replace(/-/g, "+").replace(/_/g, "/"));
  return Uint8Array.from(binary, (c) => c.charCodeAt(0));
}


export function decodeJwt(token: string): JwtPayload | null{
    try{
        const payload = JSON.parse(strFromU8(base64UrlToBytes(token.split('.')[1])))
        const {perms_z: packed, ...claims} = payload;
        if(packed !== undefined){
            claims.permissions = JSON.parse(strFromU8(unzlibSync(base64UrlToBytes(packed)))) as string[];
        }
        return claims;
    }catch {
        return null;
    }
}

export function isExpired(payload: JwtPayload | null): boolean{
    if(!payload?.exp) return false;
    return payload.exp * 1000 <= Date.now();
}

export function getAccessToken(): string | null{
    if(typeof window === 'undefined') return null;
    return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(REFRESH_KEY);
}

export function saveSession(accessToken: string, refreshToken: string): void{
    if(typeof window === 'undefined') return;
    localStorage.setItem(ACCESS_KEY, accessToken);
    localStorage.setItem(REFRESH_KEY, refreshToken);
    document.cookie = `${COOKIE_NAME}=${COOKIE_PRESENCE_VALUE}; path=/; max-age=604800; SameSite=Lax`;
}

export function clearSession(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  document.cookie = `${COOKIE_NAME}=; path=/; max-age=0; SameSite=Lax`;
}