import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
from datetime import datetime


mongoURI = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'

def init_connection():
    return MongoClient(mongoURI)

def get_data():
    client = init_connection()
    db = client.ENCODE
    return db

st.set_page_config(page_title="MongoDB Dashboard", page_icon="📊", layout="wide")


st.title("📊 MongoDB Database Dashboard")
st.write("View and analyze data from all collections in the database")

try:
    db = get_data()
    
 
    tabs = st.tabs(["Products", "Customers", "Calls", "Survey Results"])
    

    with tabs[0]:
        st.header("Products Overview")
        products_df = pd.DataFrame(list(db.products.find({}, {'_id': 0})))
        if not products_df.empty:
      
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Products", len(products_df))
            with col2:
                st.metric("Average Price", f"${products_df['price'].mean():.2f}")
            with col3:
                st.metric("Product Types", len(products_df['type'].unique()))
            
         
            st.subheader("Product Details")
            st.dataframe(products_df, use_container_width=True)
            
            if len(products_df) > 0:
                
                st.subheader("Price Distribution by Product Type")
                fig = px.bar(products_df, x='name', y='price', color='type',
                            title="Product Prices by Category")
                st.plotly_chart(fig, use_container_width=True)
    

    with tabs[1]:
        st.header("Customer Information")
        customers_df = pd.DataFrame(list(db.customers.find({}, {'_id': 0})))
        if not customers_df.empty:
          
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Customers", len(customers_df))
            with col2:
                total_products = sum([len(p) for p in customers_df['products']])
                st.metric("Total Products Sold", total_products)
            
         
            st.subheader("Customer Purchase History")
            for _, customer in customers_df.iterrows():
                with st.expander(f"Customer: {customer['name']}"):
                    products_bought = pd.DataFrame(customer['products'])
                    st.dataframe(products_bought)
    

    with tabs[2]:
        st.header("Call Analytics")
        calls_df = pd.DataFrame(list(db.calls.find({}, {'_id': 0})))
        if not calls_df.empty:
           
            st.metric("Total Calls", len(calls_df))
            
           
            st.subheader("Call Score Distribution")
            fig = px.histogram(calls_df, x='score',
                             title="Distribution of Call Scores",
                             nbins=10)
            st.plotly_chart(fig, use_container_width=True)
            
        
            st.subheader("Call Transcripts")
            for _, call in calls_df.iterrows():
                with st.expander(f"Call for Customer {call['customer_id']} (Score: {call['score']})"):
                    st.write(call['transcribed_call'])
    

    with tabs[3]:
        st.header("Survey Results")
        survey_df = pd.DataFrame(list(db.survey.find({}, {'_id': 0})))
        if not survey_df.empty:
            st.metric("Total Surveys", len(survey_df))
            
           
            st.subheader("Survey Details")
            for _, survey in survey_df.iterrows():
                with st.expander(f"Survey {_ + 1}"):
                    st.write(survey['survey_info'])

except Exception as e:
    st.error(f"Error connecting to MongoDB: {str(e)}")