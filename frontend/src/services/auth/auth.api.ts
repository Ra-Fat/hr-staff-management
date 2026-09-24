import { httpClient, BASE_URL } from "../http/client";

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface Envelope<T> {
  code: number;
  msg: string;
  data: T;
}

export interface AdminUserDto {
  id: number;
  full_name: string;
  email: string;
  role: { id: number; name: string } | null;
  status: "active" | "disabled";
  last_login: string | null;
  created_at: string | null;
}

export const authApi = {
  login: (email: string, password: string) =>
    httpClient.post<TokenResponse>(
      "/auth/login",
      { email, password },
      { baseUrl: BASE_URL },
    ),

  me: async (): Promise<AdminUserDto> => {
    const res = await httpClient.get<Envelope<AdminUserDto>>("/auth/me", {
      baseUrl: BASE_URL,
    });
    return res.data;
  },
  logout: () =>
    httpClient.post<unknown>("/auth/logout", {}, { baseUrl: BASE_URL }),

  refresh: (refreshToken: string) =>
    httpClient.post<TokenResponse>(
      "/auth/refresh",
      {
        refresh_token: refreshToken,
      },
      { baseUrl: BASE_URL },
    ),
};
