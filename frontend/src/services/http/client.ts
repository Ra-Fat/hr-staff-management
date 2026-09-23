import { ApiError } from "@/src/types/api.type";
import { logger } from "@/src/lib/logger";
import { getAccessToken, decodeJwt } from "@/src/lib/session";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL ?? "";

interface RequestOptions extends RequestInit {
  baseUrl?: string;
  suppressLog?: boolean;
}

async function request<T>(
  method: string,
  path: string,
  options?: RequestOptions,
): Promise<T> {
  const baseUrl = options?.baseUrl ?? BASE_URL;

  const url = `${baseUrl}${path}`;
  const token = getAccessToken();
  const payload = token ? decodeJwt(token) : null;
  const userId = payload?.sub;

  let response: Response;

  try {
    response = await fetch(url, {
      ...options,
      method,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(userId ? { "user-id": userId } : {}),
        ...options?.headers,
      },
    });
  } catch (cause) {
    const message =
      cause instanceof Error ? cause.message : "Unable to reach the API";
    throw new ApiError(0, "NETWORK_ERROR", message);
  }

  if (!response.ok) {
    let errorBody: {
      code?: string | number;
      message?: string;
      msg?: string;
      detail?: string | Array<{ msg?: string }>;
      details?: Record<string, string[]>;
    } = {};
    try {
      errorBody = await response.json();
    } catch {
      // non-JSON error body
    }
    const error = new ApiError(
      response.status,
      String(errorBody.code ?? "UNKNOWN_ERROR"),
      errorBody.message ??
        errorBody.msg ??
        (typeof errorBody.detail === "string" ? errorBody.detail : undefined) ??
        (Array.isArray(errorBody.detail)
          ? errorBody.detail
              .map((item) => item.msg)
              .filter(Boolean)
              .join("; ")
          : undefined) ??
        `HTTP ${response.status}`,
      errorBody.details,
    );
    if (!options?.suppressLog) {
      logger.error("API request failed", {
        url,
        status: response.status,
        code: error.code,
        errorBody,
      });
    }
    throw error;
  }
  return response.json() as Promise<T>;
}

export const httpClient = {
  get: <T>(path: string, options?: RequestOptions) => request<T>('GET', path, options),
  post: <T>(path: string, body: unknown, options?: RequestOptions) =>
    request<T>('POST', path, { ...options, body: JSON.stringify(body) }),
  put: <T>(path: string, body: unknown, options?: RequestOptions) =>
    request<T>('PUT', path, { ...options, body: JSON.stringify(body) }),
  patch: <T>(path: string, body: unknown, options?: RequestOptions) =>
    request<T>('PATCH', path, { ...options, body: JSON.stringify(body) }),
  delete: <T>(path: string, options?: RequestOptions) => request<T>('DELETE', path, options),
};