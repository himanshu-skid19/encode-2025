

async def duckduckgo_search(query, max_results=5):
    from duckduckgo_search import DDGS

    results = []
    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)
            for r in search_results:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""), 
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return [{"title": "Error occurred", "url": "", "snippet": str(e)}]
    
    if not results:
        return [{"title": "No results found", "url": "", "snippet": ""}]
    
    return results



async def success():
    print("******************************************")
    from twilio.rest import Client
    


    account_sid = 'AC38db8f90e828f32babcbae0052c0b019'
    auth_token = '45e01b1a38edc7265d0eb2b1c39b7867'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    to='whatsapp:+919031910788',
    body='Thank You for purchasing the product with us. We would appreciate if you could take a moment to fill out the survey form. https://forms.gle/6FV1hmDun6rB9SpQ6'
    )

    print(message.sid)
    print("SUCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")



async def query_product_db(query_text, n_results=3):
    import chromadb
    from chromadb.utils import embedding_functions
    import google.generativeai as genai
    import os

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

    try:
       
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
     
        os.environ["GEMINI_API_KEY"] = 'AIzaSyDO_9k4-rG2UoeRW5AQirXBvx6_XRVZpBo'
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        

        gemini_ef = GeminiEmbeddingFunction()
        
     
        collection = chroma_client.get_collection(
            name="products_collection",
            embedding_function=gemini_ef
        )

        query_results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        formatted_results = []
        for doc, metadata in zip(query_results['documents'][0], query_results['metadatas'][0]):
            formatted_results.append({
                'name': metadata['name'],
                'type': metadata['type'],
                'details': doc,
                'mongo_id': metadata['mongo_id'],
                'relevance_score': None if not query_results['distances'] else query_results['distances'][0][len(formatted_results)]
            })
        print(formatted_results)
        return {
            'success': True,
            'results': formatted_results,
            'error': None
        }

    except Exception as e:
        return {
            'success': False,
            'results': [],
            'error': str(e)
        }











FUNCTION_DEFINITIONS = [
    {
        "name": "duckduckgo_search",
        "description": "Perform a web search using the DuckDuckGo search engine and return a list of results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string to look up on DuckDuckGo."
                },
                "max_results": {
                    "type": "integer",
                    "description": "The maximum number of search results to retrieve.",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "query_product_db",
        "description": "Query the existing company database which has all the products that the company sells. Returns info about products related to the query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query_text": {
                    "type": "string",
                    "description": "The search query text."
                },
                "n_results": {
                    "type": "integer",
                    "description": "Number of results to return.",
                    "default": 3
                }
            },
            "required": ["query_text"]
        }
    }, 
    {
        "name": "success",
        "description": "A  function that should be called when the user agrees to buy a product",
        "parameters": {}
    }



]


FUNCTION_MAP = {"duckduckgo_search": duckduckgo_search, "query_product_db": query_product_db, "success": success}