import { apiClient, ApiError } from './index';
import type { IProduct } from '../types';

export const productService = {
  getAll: async (): Promise<IProduct[]> => {
    try {
      const { data } = await apiClient.get<IProduct[]>('/products');
      return data;
    } catch (error : any) {
      throw new ApiError(error.response?.status || 500, error.message);
    }
  },

  getById: async (productId: string): Promise<IProduct> => {
    try {
      const { data } = await apiClient.get<IProduct>(`/products/${productId}`);
      return data;
    } catch (error : any) {
      throw new ApiError(error.response?.status || 500, error.message);
    }
  },
};