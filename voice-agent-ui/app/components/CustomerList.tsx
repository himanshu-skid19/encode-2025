'use client';

import { useEffect, useState } from 'react';
import { customerService } from '../api/services/customers';
import type { ICustomer } from '@/app/api/types';

export default function CustomerList() {
  const [customers, setCustomers] = useState<ICustomer[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const data = await customerService.getAll();
        setCustomers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch customers');
      }
    };

    fetchCustomers();
  }, []);

  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {customers.map((customer) => (
        <div key={customer.customer_id}>
          <h3>{customer.name}</h3>
          <p>Customer ID: {customer.customer_id}</p>
          <p>Score: {customer.customer_score}</p>
        </div>
      ))}
    </div>
  );
}