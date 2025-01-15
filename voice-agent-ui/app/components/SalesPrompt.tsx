'use client';

import { useEffect, useState } from 'react';
import { customerService } from '../api/services/customers';
import { PromptService } from '../lib/services/promptService';
import type { CustomerData } from '../lib/types/prompt';

export default function SalesPrompt({ customerId }: { customerId: number }) {
  const [prompt, setPrompt] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const generatePrompt = async () => {
      try {
        // Fetch customer data
        const customerData = await customerService.getById(customerId);
        
        // Generate customized prompt
        const customizedPrompt = PromptService.generateCustomPrompt(customerData);
        setPrompt(customizedPrompt);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to generate prompt');
      }
    };

    generatePrompt();
  }, [customerId]);

  if (error) return <div>Error: {error}</div>;
  if (!prompt) return <div>Loading...</div>;

  return (
    <div className="whitespace-pre-wrap">
      {prompt}
    </div>
  );
}