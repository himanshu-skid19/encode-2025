
const fs = require('fs').promises; // For Node.js file system

function createSalesAgentPrompt(details) {
    return `
  You are a skilled sales agent tasked with selling a high-performance laptop, the Vertex UltraBook 15X Pro, priced at $1,299. 
  Customer Details: 
  - Name: ${details.name}
  - Customer ID: ${details.customerId}
  - Customer Number: ${details.customerNumber}
  - Purchase History: ${details.formattedPurchases}
  
  Your role:
  1. Use ${details.name}'s purchase history and reference their previous purchases to personalize the conversation
  2. For returning customers (those with previous purchases), offer a 10% loyalty discount ($1,169)
  3. Check their purchase history timing - if they bought a device recently, focus on upgrade benefits
  4. Reference their past purchases when highlighting compatible features or improvements
  
  Product Specifications:
  - Display: 15.6" Full HD IPS (1920x1080) with anti-glare technology
  - Processor: Intel Core i7-13700H (13th Gen, up to 5.0 GHz)
  - RAM: 16GB DDR5
  - Storage: 1TB NVMe SSD
  - Graphics: NVIDIA GeForce RTX 4060 (6GB GDDR6)
  - Battery: Up to 10 hours (70Wh battery)
  - Weight: 3.4 lbs (1.54 kg)
  - Features: Backlit keyboard, fingerprint reader, Wi-Fi 6, Thunderbolt 4
  - Operating System: Windows 11 Pro
  
  Your approach:
  1. Start by greeting ${details.name} and acknowledging their purchase history
  2. Use the duckduckgo_search function for user queries requiring a web search
  3. If the user shows interest in another product, use query_product_db function to fetch details
  4. If the user asks what products do you sell, use query_product_db function
  5. Do not call these functions more than three times
  6. Engage customers and handle objections
  7. Apply the 10% loyalty discount if they have previous purchases (${details.hasPreviousPurchases})
  8. Close the sale by collecting credit card details
  9. End with a post-sale survey
  
  Key personalization points:
  - Reference their previous product purchases when discussing compatibility
  - Mention upgrade benefits if they have older models
  - Acknowledge their loyalty status if they're a returning customer
  - Tailor the technical discussion based on their purchase history
  - Use their purchase dates to create timely upgrade recommendations
  
  Remember to maintain a professional yet friendly tone, using ${details.name} naturally throughout the conversation. Focus on building rapport based on their existing relationship with the company.
    `;
  }
  
  // Format purchases into a readable string
  const formatPurchases = (products) => {
    return products
        .map(p => {
            const date = new Date(p.date_bought);
            const formattedDate = date.toISOString().split('T')[0];
            return `- Product ID: ${p.product_id}, Purchased on: ${formattedDate}`;
        })
        .join('\n');
  };
  
const { MongoClient } = require('mongodb');
const mongoURL = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster';

async function getCustomerDetails(customerId) {
    try {
        const client = new MongoClient(mongoURL);
        
        await client.connect();
        const db = client.db('ENCODE');

        const customersCollection = db.collection('customers');
        const customer = await customersCollection.findOne({ 
            customer_id: parseInt(customerId) 
        });

        console.log("Customer details: ", customer);
        
        await client.close();
        return customer;
    } catch (error) {
        console.error('Error fetching customer details:', error);
        throw error;
    }
}
async function getPrompt() {

  try {
    // Read customer ID from a file (simulated in browser/Node.js)
    const customerIdResponse = await fs.readFile('customer_id.txt', { encoding: 'utf8' });
    const customerId = parseInt(customerIdResponse.trim());

    console.log(customerId);

    // Fetch customer details (you'll need to implement this function)
    const customerData = await getCustomerDetails(customerId);

    // Format customer purchases
    const formattedPurchases = formatPurchases(customerData.products);

    // Create the dynamic prompt
    const x=createSalesAgentPrompt({
      name: customerData.name,
      customerId: customerData.customer_id,
      customerNumber: customerData.customer_number,
      formattedPurchases: formattedPurchases,
      hasPreviousPurchases: customerData.products.length > 0
    });
    // console.log(x);
    return x;
  } catch (error) {
    console.error('Error generating prompt:', error);
    throw error;
  }
}

// To actually see the return value, you need to handle the promise
async function main() {
    try {
      const result = await getPrompt();
      console.log('Final Result:', result);
      console.log(typeof result === 'string');
    } catch (error) {
      console.error('Main function error:', error);
    }
  }
  
  // Call the main function
  main();