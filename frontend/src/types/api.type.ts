export interface ApiResponse<T>{
    data: T;
    message: string;
    success: boolean;
}

export interface PaginatedResponse<T>{
    data: T[];
    total: number;
    pageZ: number;
    totalPages: number;
}

export interface QueryParams {
  page?: number;
  limit?: number;
  search?: string;
}

export class ApiError extends Error{
    constructor(
        public readonly status: number,
        public readonly code: string,
        message: string,
        public readonly details?: Record<string, string[]>,
    ){
        super(message);
        this.name = 'ApiError'
    }
}