import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timezone
import pandas as pd
from sync_chroma_with_mongo import *
import threading
mongoURI = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'
def sync_mongo():
    sync_mongo_to_chroma()
def init_connection():
    return MongoClient(mongoURI)

def get_database():
    client = init_connection()
    return client.ENCODE

st.set_page_config(page_title="Data Entry", page_icon="✏️", layout="wide")
st.title("✏️ Data Entry Portal")
st.write("Add or update information in the database")

try:
    db = get_database()
    
   
    tab_selection = st.tabs(["Products", "Customers"])
    

    with tab_selection[0]:
        st.header("Add New Product")
        with st.form("product_form"):
            name = st.text_input("Product Name")
            product_id = st.number_input("Product ID", min_value=1, step=1)
            price = st.number_input("Price ($)", min_value=0.0, step=0.01)
            product_type = st.selectbox("Product Type", ["Electronics", "Accessories", "Other"])
            offers = st.text_input("Current Offers")
            warranty = st.text_input("Warranty Details")
            description = st.text_area("Product Description")
            
            submit_product = st.form_submit_button("Add Product")
            
            if submit_product:
                try:
                    product_data = {
                        "name": name,
                        "id": product_id,
                        "price": price,
                        "type": product_type,
                        "offers": offers,
                        "warranty_details": warranty,
                        "description": description
                    }
                    db.products.insert_one(product_data)
                    sync_thread = threading.Thread(target=sync_mongo)
                    sync_thread.start()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

                    st.success("Product added successfully!")
                except Exception as e:
                    st.error(f"Error adding product: {str(e)}")
    
  
    with tab_selection[1]:
        st.header("Add New Customer")
        with st.form("customer_form"):
            customer_name = st.text_input("Customer Name")
            customer_number = st.number_input("Customer Number", min_value=100, step=1)
            customer_id = st.number_input("Customer ID", min_value=1000, step=1)
            
           
            st.subheader("Product Purchases")
            num_products = st.number_input("Number of Products", min_value=1, max_value=10, value=1)
            products = []
            
            for i in range(num_products):
                st.write(f"Product {i+1}")
                col1, col2 = st.columns(2)
                with col1:
                    prod_id = st.number_input(f"Product ID #{i+1}", min_value=1, step=1, key=f"prod_id_{i}")
                with col2:
                    date_bought = st.date_input(f"Date Bought #{i+1}", key=f"date_{i}")
                
                    date_bought = datetime.combine(date_bought, datetime.min.time())
                    date_bought = date_bought.replace(tzinfo=timezone.utc)
             
                    products.append({"product_id": prod_id, "date_bought": date_bought})
            
            submit_customer = st.form_submit_button("Add Customer")
            
            if submit_customer:
                try:
                    customer_data = {
                        "customer_number": customer_number,
                        "name": customer_name,
                        "products": products,
                        "customer_id": customer_id
                    }
                    db.customers.insert_one(customer_data)
                    st.success("Customer added successfully!")
                except Exception as e:
                    st.error(f"Error adding customer: {str(e)}")
    
 
    # with tab_selection[2]:
    #     st.header("Add Call Record")
    #     with st.form("call_form"):
    #         transcription = st.text_area("Call Transcription")
    #         score = st.slider("Call Score", 0.0, 1.0, 0.5)
    #         call_customer_id = st.number_input("Customer ID", min_value=1000, step=1)
            
    #         submit_call = st.form_submit_button("Add Call Record")
            
    #         if submit_call:
    #             try:
    #                 call_data = {
    #                     "transcribed_call": transcription,
    #                     "score": score,
    #                     "customer_id": call_customer_id
    #                 }
    #                 db.calls.insert_one(call_data)
    #                 st.success("Call record added successfully!")
    #             except Exception as e:
    #                 st.error(f"Error adding call record: {str(e)}")
    

    # with tab_selection[3]:
    #     st.header("Add Survey Results")
    #     with st.form("survey_form"):
    #         survey_info = st.text_area("Survey Information")
            
    #         submit_survey = st.form_submit_button("Add Survey")
            
    #         if submit_survey:
    #             try:
    #                 survey_data = {
    #                     "survey_info": survey_info
    #                 }
    #                 db.survey.insert_one(survey_data)
    #                 st.success("Survey added successfully!")
    #             except Exception as e:
    #                 st.error(f"Error adding survey: {str(e)}")
    

    st.header("Recent Entries")
    collection = st.selectbox("Select Collection to View", 
                            ["Products", "Customers", "Calls", "Surveys"])
    
    if collection == "Products":
        df = pd.DataFrame(list(db.products.find({}, {'_id': 0}).sort([('_id', -1)]).limit(5)))
    elif collection == "Customers":
        df = pd.DataFrame(list(db.customers.find({}, {'_id': 0}).sort([('_id', -1)]).limit(5)))
    elif collection == "Calls":
        df = pd.DataFrame(list(db.calls.find({}, {'_id': 0}).sort([('_id', -1)]).limit(5)))
    else:
        df = pd.DataFrame(list(db.survey.find({}, {'_id': 0}).sort([('_id', -1)]).limit(5)))
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No entries found in this collection")

except Exception as e:
    st.error(f"Error connecting to MongoDB: {str(e)}")