'use client';

import SalesPrompt from '@/app/components/SalesPrompt';
import Link from 'next/link';

export default function SalesDemoPage() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <Link 
            href="/"
            className="text-blue-600 hover:text-blue-800"
          >
            ← Back to Home
          </Link>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <SalesPrompt customerId={1001} /> {/* Using 1 as test ID */}
        </div>
      </div>
    </div>
  );
}