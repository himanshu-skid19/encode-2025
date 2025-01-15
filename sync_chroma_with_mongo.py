import google.generativeai as genai
import chromadb
import os
from chromadb.utils import embedding_functions
from pymongo import MongoClient
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()


os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Configure genai with the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Gemini API Key successfully loaded.")


def concatenate_product_details(product):
    """Concatenate all product details into a single string"""
    return f"Product: {product.get('name', '')}. " \
           f"Type: {product.get('type', '')}. " \
           f"Price: ${product.get('price', '')}. " \
           f"Offers: {product.get('offers', '')}. " \
           f"Warranty: {product.get('warranty_details', '')}. " \
           f"Description: {product.get('description', '')}."

class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __call__(self, texts):
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text
            )
            embeddings.append(result['embedding'])
        return embeddings

def sync_mongo_to_chroma():
    # MongoDB connection
    mongoURI = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'
    mongo_client = MongoClient(mongoURI)
    db = mongo_client.ENCODE
    products_collection = db.products

    # ChromaDB setup
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    gemini_ef = GeminiEmbeddingFunction()

    # Get or create collection
    try:
        collection = chroma_client.get_collection(
            name="products_collection",
            embedding_function=gemini_ef
        )
        print("Found existing ChromaDB collection")
    except:
        collection = chroma_client.create_collection(
            name="products_collection",
            embedding_function=gemini_ef
        )
        print("Created new ChromaDB collection")

    # Get existing product IDs in ChromaDB
    existing_ids = set()
    try:
        existing_ids = set(collection.get()['ids'])
    except:
        pass

    # Get all products from MongoDB
    mongo_products = list(products_collection.find())
    
    # Filter out products that are already in ChromaDB
    # Convert MongoDB ObjectId to string for comparison
    new_products = [p for p in mongo_products if str(p['_id']) not in existing_ids]
    
    if not new_products:
        print("No new products to add")
        return collection

    # Prepare data for ChromaDB
    documents = [concatenate_product_details(p) for p in new_products]
    ids = [str(p['_id']) for p in new_products]  # Convert ObjectId to string
    metadata = [{"name": p['name'], 
                "type": p.get('type', 'Unknown'),
                "mongo_id": str(p['_id'])} for p in new_products]

    # Add new products to ChromaDB
    if documents:
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadata
        )
        print(f"Added {len(documents)} new products to ChromaDB")

    return None





