"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface Customer {
  _id?: string;
  customer_id?: string;
  name: string;
  customer_number: string;
  products: { product_id: string; date_bought: string }[];
}

interface Product {
  _id?: string;
  id?: string;
  name: string;
  price: number;
  type: string;
  offers: string;
  description: string;
}

interface Call {
  customer_id: string;
  transcribed_call: string;
}

interface Survey {
  survey_info: string;
}

export default function Dashboard() {
  const [data, setData] = useState<{
    customers: Customer[];
    products: Product[];
    calls: Call[];
    surveys: Survey[];
  }>({
    customers: [],
    products: [],
    calls: [],
    surveys: [],
  });

  const [activeTab, setActiveTab] = useState<string>("customers");
  const API_ENDPOINT = "https://voice-bot-backend-txr4.onrender.com/api";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [customers, products, calls, surveys] = await Promise.all([
          axios.get(API_ENDPOINT + "/customers"),
          axios.get(API_ENDPOINT + "/products"),
          axios.get(API_ENDPOINT + "/calls"),
          axios.get(API_ENDPOINT + "/surveys"),
        ]);

        setData({
          customers: customers.data,
          products: products.data,
          calls: calls.data,
          surveys: surveys.data,
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="h-screen flex flex-col">
      {/* Top Navigation Bar */}
      <div className="bg-black text-white p-4 flex justify-center space-x-6">
        {["customers", "products", "calls", "surveys"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-2 rounded-md text-sm font-medium ${
              activeTab === tab
                ? "bg-gradient-to-r from-[#149AFB]/80 to-[#13EF93]/50 text-white"
                : "bg-black border border-gray-600 text-gray-400 hover:bg-gray-800 transition-colors"
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Main Content Area */}
      <div className="flex-1 bg-gray-900 overflow-auto">
        <main className="mx-auto max-w-7xl px-4 md:px-6 lg:px-8 py-6">
          {activeTab === "customers" && (
            <div className="grid grid-cols-1 gap-4">
              {data.customers.map((customer) => (
                <div
                  key={customer._id || customer.customer_id}
                  className="border rounded-lg p-4"
                >
                  <h3 className="text-xl font-bold">{customer.name}</h3>
                  <p>Customer Number: {customer.customer_number}</p>
                  <p>Customer ID: {customer.customer_id}</p>
                  <div className="mt-2">
                    <h4 className="font-semibold mb-2">Purchase History:</h4>
                    {customer.products.map((product, idx) => (
                      <div
                        key={idx}
                        className="bg-gray-50 p-2 rounded shadow-sm"
                      >
                        <p>Product ID: {product.product_id}</p>
                        <p>Purchase Date: {formatDate(product.date_bought)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === "products" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.products.map((product) => (
                <div
                  key={product._id || product.id}
                  className="border rounded-lg p-4"
                >
                  <h3 className="text-xl font-bold">{product.name}</h3>
                  <p className="text-lg font-semibold text-blue-600">
                    ${product.price}
                  </p>
                  <p>Type: {product.type}</p>
                  <p className="text-green-600">{product.offers}</p>
                  <p>{product.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === "calls" && (
            <div className="grid grid-cols-1 gap-4">
              {data.calls.map((call, idx) => (
                <div key={idx} className="border rounded-lg p-4">
                  <p>Customer ID: {call.customer_id}</p>
                  <p>{call.transcribed_call}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === "surveys" && (
            <div className="grid grid-cols-1 gap-4">
              {data.surveys.map((survey, idx) => (
                <div key={idx} className="border rounded-lg p-4">
                  <p>{survey.survey_info}</p>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-black text-white p-4 text-center">
        <a
          href="https://forms.office.com/r/hGJDf68aSA"
          target="_blank"
          className="bg-gradient-to-r from-[#149AFB] to-[#13EF93] text-white px-8 py-2 rounded-md hover:opacity-90 transition-opacity font-medium"
        >
          Contact Us for Phone Support
        </a>
      </footer>
    </div>
  );
}
