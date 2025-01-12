

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
    }
]


FUNCTION_MAP = {"duckduckgo_search": duckduckgo_search}