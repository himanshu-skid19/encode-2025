from pymongo import MongoClient
import chromadb
from chromadb.utils import embedding_functions
import openai
import hashlib
import json
from typing import List, Dict
import os

class ProductSearchSystem:
    def __init__(self, mongo_uri: str, openai_api_key: str, cache_dir: str = "./cache"):
        """
        Initialize the search system with MongoDB connection and ChromaDB setup.
        
        Args:
            mongo_uri (str): MongoDB connection string
            openai_api_key (str): OpenAI API key for embeddings
            cache_dir (str): Directory to store ChromaDB persistent client
        """
    
        self.client = MongoClient(mongo_uri)
        self.db = self.client.ENCODE
        self.products_collection = self.db.products
        
 
        openai.api_key = openai_api_key
        
    
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-ada-002"
        )
        
     
        self.chroma_client = chromadb.PersistentClient(path=cache_dir)
        
  
        self.collection = self.chroma_client.get_or_create_collection(
            name="products",
            embedding_function=self.embedding_function
        )
        
    def _generate_document_hash(self, document: Dict) -> str:
        """Generate a unique hash for a document to track changes."""
        return hashlib.md5(json.dumps(document, sort_keys=True).encode()).hexdigest()
    
    def update_chroma_db(self):
        """Update ChromaDB with products from MongoDB."""
   
        products = list(self.products_collection.find({}))
    
        self.collection.delete(where={})
        
     
        ids = []
        documents = []
        metadatas = []
        
        for product in products:
            product_id = str(product['id'])
            description = product['description']

            metadata = {
                'name': product['name'],
                'price': product['price'],
                'type': product['type'],
                'offers': product['offers'],
                'warranty_details': product['warranty_details']
            }
            
            ids.append(product_id)
            documents.append(description)
            metadatas.append(metadata)
        
     
        if documents:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
        return len(documents)
    
    def search_products(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Search for products similar to the query.
        
        Args:
            query (str): Search query
            n_results (int): Number of results to return
            
        Returns:
            List[Dict]: List of similar products with their metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=['metadatas', 'documents', 'distances']
        )
        
  
        formatted_results = []
        for i in range(len(results['ids'][0])):
            result = {
                'id': results['ids'][0][i],
                'description': results['documents'][0][i],
                'similarity_score': 1 - results['distances'][0][i],  
                **results['metadatas'][0][i]  
            }
            formatted_results.append(result)
            
        return formatted_results


if __name__ == "__main__":
   
    search_system = ProductSearchSystem(
        mongo_uri='mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster',
        openai_api_key='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',
        cache_dir='./chroma_cache'
    )
    

    num_products = search_system.update_chroma_db()
    print(f"Updated ChromaDB with {num_products} products")
    

    query = "high performance computing device"
    results = search_system.search_products(query, n_results=2)
    

    for result in results:
        print(f"\nProduct: {result['name']}")
        print(f"Similarity Score: {result['similarity_score']:.2f}")
        print(f"Description: {result['description']}")
        print(f"Price: ${result['price']}")



