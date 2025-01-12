
async def price_gpu(GPU : str):
    return 3000
 


FUNCTION_DEFINITIONS = [
    {
        "name": "price_gpu",
        "description": "Returns the current price of a GPU in USD.",
        "parameters": {
            "type": "object",
            "properties": {
                "GPU": {
                    "type": "string",
                    "description": "The name of the GPU for which the price is being retrieved."
                }
            },
            "required": ["GPU"]
        }
    }
]


FUNCTION_MAP = {"price_gpu": price_gpu}