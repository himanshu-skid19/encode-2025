from pymongo import MongoClient, uri_parser
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

mongoURL = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'
def get_customer_data():
    # MongoDB connection string
    
    # Parse the connection string to extract the database name
    #parsed_uri = uri_parser.parse_uri(mongoURL)
    #db_name = parsed_uri.get("database")  # Extract the database name
    db_name = "ENCODE"

    if not db_name:
        raise ValueError("Database name is not specified in the connection string.")

    # Connect to MongoDB
    client = MongoClient(mongoURL)
    db = client[db_name]  # Use the extracted database name
    collection = db["customers"]  # Replace with your collection name

    # Retrieve all customer data
    customer_data = list(collection.find({}))  # You can add filters if needed
    print("Customer Data: ", customer_data)
    return customer_data

def get_customer_details(customer_id):
    client = MongoClient(mongoURL)
    db = client.ENCODE

    customers_collection = db.customers
    x = customers_collection.find_one({"customer_id": int(customer_id)})
    print("njn2qjneiqn2ei ", x)
    return x

def get_product_data():
    # MongoDB connection string

    # Parse the connection string to extract the database name
    #parsed_uri = uri_parser.parse_uri(mongoURL)
    #db_name = parsed_uri.get("database")  # Extract the database name
    db_name = "ENCODE"
    if not db_name:
        raise ValueError("Database name is not specified in the connection string.")

    # Connect to MongoDB
    client = MongoClient(mongoURL)
    db = client[db_name]  # Use the extracted database name
    collection = db["products"]  # Replace with your collection name

    # Retrieve all customer data
    product_data = list(collection.find({}))  # You can add filters if needed
    return product_data

def get_call_data():
    # MongoDB connection string

    # Parse the connection string to extract the database name
    #parsed_uri = uri_parser.parse_uri(mongoURL)
    db_name = "ENCODE"

    if not db_name:
        raise ValueError("Database name is not specified in the connection string.")

    # Connect to MongoDB
    client = MongoClient(mongoURL)
    db = client[db_name]  # Use the extracted database name
    collection = db["calls"]  # Replace with your collection name

    # Retrieve all customer data
    call_data = list(collection.find({}))  # You can add filters if needed
    return call_data


def filter_customers_by_score(customers_data, products_data, calls_data, THRESHOLD=75):
    filtered_customers = []
    for customer in customers_data:
        customer_score = 0
        for product in customer["products"]:
            product_id = product["product_id"]
            product_info = next((p for p in products_data if p["id"] == product_id), None)
            if product_info:
                #print("1: ",customer["customer_id"])
                customer_score += product_info["price"] / 100
        for call in calls_data:
            if call["customer_id"] == customer["customer_id"]:
                #print("2: ",customer["customer_id"])
                customer_score += call["score"]
        customer["customer_score"] = customer_score

        if customer_score > THRESHOLD:
            #print("3: ",customer["customer_id"])
            filtered_customers.append(customer)
    #print("Filtered Customers: ", filtered_customers)
    return filtered_customers


def initiate_calls(customers):
    print("Initiating calls to customers...")
    # Twilio credentials (replace with your actual credentials)
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    for customer in customers:
        print("Customer: ", customer)
        phone_number = customer.get("customer_number")
        survey_analysis = customer.get("survey_analysis", "No analysis available.")
        print(f"Initiating call to {phone_number}...")
        if phone_number:
             # Generate TwiML with TTS
            response = VoiceResponse()
            response.say(survey_analysis, voice='alice', language='en-US')  # Use 'alice' for a natural voice
            call = client.calls.create(
               # url = "http://demo.twilio.com/docs/voice.xml",
                to="+91 79828 39139",
                from_=os.getenv("TWILIO_PHONE_NUMBER"),  # Replace with your Twilio number
                twiml=str(response)
            )
            print(f"Call initiated to {phone_number}, Call SID: {call.sid}")
def main():
    print("Starting the voice call agent...")
    # Step 1: Retrieve data from MongoDB
    customers = get_customer_data()
    products = get_product_data()
    calls = get_call_data()


    # Step 2: Filter customers based on score
    min_score = 0.5  # Example threshold score
    filtered_customers = filter_customers_by_score(customers, products, calls, min_score)

    # Step 3: Pass filtered customers to voice call agent
    initiate_calls(filtered_customers)

if __name__ == "__main__":
    main()

