export interface ApiResponse<T> {
  data: T;
  msg: string;
  code: number;
}

export interface PaginatedData<T> {
  total_records: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  lists: T[];
}

export type PaginatedResponse<T> = ApiResponse<PaginatedData<T>>;

export interface QueryParams {
  page?: number;
  limit?: number;
  search?: string;
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly details?: Record<string, string[]>,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
