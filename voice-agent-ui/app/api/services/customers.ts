import { apiClient, ApiError } from './index';
import type { ICustomer } from '../types';

export const customerService = {
  getAll: async (): Promise<ICustomer[]> => {
    try {
      const { data } = await apiClient.get<ICustomer[]>('/customers');
      return data;
    } catch (error: any) {
      throw new ApiError(
        error.response?.status || 500,
        error.response?.data?.message || 'Failed to fetch customers'
      );
    }
  },

  getById: async (customerId: number): Promise<ICustomer> => {
    try {
      const { data } = await apiClient.get<ICustomer>(`/customers/${customerId}`);
      
      // Verify that we received valid customer data
      if (!data || !data.customer_id) {
        throw new ApiError(400, 'Invalid customer data received');
      }

      return data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        throw new ApiError(404, 'Customer not found');
      }
      throw new ApiError(
        error.response?.status || 500,
        error.response?.data?.message || 'Failed to fetch customer'
      );
    }
  },

  create: async (customerData: Omit<ICustomer, 'createdAt' | 'updatedAt'>): Promise<ICustomer> => {
    try {
      // Validate required fields
      if (!customerData.customer_number || !customerData.name || !customerData.customer_id) {
        throw new ApiError(400, 'Missing required customer information');
      }

      const { data } = await apiClient.post<ICustomer>('/customers', customerData);
      return data;
    } catch (error: any) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(
        error.response?.status || 500,
        error.response?.data?.message || 'Failed to create customer'
      );
    }
  },

  verifyCustomer: async (customerId: number): Promise<boolean> => {
    try {
      const customer = await customerService.getById(customerId);
      return Boolean(customer && customer.customer_id === customerId);
    } catch (error) {
      return false;
    }
  }
};