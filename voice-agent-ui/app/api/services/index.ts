import axios from 'axios';
import { API_BASE_URL } from '../config';
import type { ICustomer, IProduct, ICall, ISurvey } from '../types';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = 'ApiError';
    }
}

export { apiClient };
