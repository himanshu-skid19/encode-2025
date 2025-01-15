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
    
 
    tabs = st.tabs(["Products", "Customers"])
    

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
    

    

    # with tabs[3]:
    #     st.header("Survey Results")
    #     survey_df = pd.DataFrame(list(db.survey.find({}, {'_id': 0})))
    #     if not survey_df.empty:
    #         st.metric("Total Surveys", len(survey_df))
            
           
    #         st.subheader("Survey Details")
    #         for _, survey in survey_df.iterrows():
    #             with st.expander(f"Survey {_ + 1}"):
    #                 st.write(survey['survey_info'])


    # with tabs[3]:
    #     st.header("Survey Results")
    #     survey_df = pd.DataFrame(list(db.survey.find({}, {'_id': 0})))
    #     if not survey_df.empty:
    #         st.metric("Total Surveys", len(survey_df))
            
    #         # Display average ratings
    #         st.subheader("Overall Metrics")
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             # Access nested dictionary correctly
    #             avg_satisfaction = survey_df['satisfaction_ratings'].apply(lambda x: x['overall']).mean()
    #             st.metric("Average Satisfaction", f"{avg_satisfaction:.1f}/5")
    #         with col2:
    #             recommend_count = len(survey_df[survey_df['product_feedback'].apply(lambda x: x.get('would_recommend') == 'Definitely')])
    #             recommend_percent = (recommend_count / len(survey_df)) * 100
    #             st.metric("Would Definitely Recommend", f"{recommend_percent:.1f}%")
    #         with col3:
    #             resolution_rate = len(survey_df[survey_df['resolution'].apply(lambda x: x['issue_resolved'] == 'Yes')]) / len(survey_df) * 100
    #             st.metric("Issue Resolution Rate", f"{resolution_rate:.1f}%")
            
    #         # Individual Survey Details
    #         st.subheader("Survey Details")
    #         for idx, survey in survey_df.iterrows():
    #             with st.expander(f"Survey {idx + 1} - {survey['customer_info']['name']}"):
    #                 # Customer Info
    #                 st.markdown("**Customer Information**")
    #                 st.write(f"Name: {survey['customer_info']['name']}")
    #                 st.write(f"Email: {survey['customer_info']['email']}")
    #                 st.write(f"Contact: {survey['customer_info']['contact_number']}")
                    
    #                 # Ratings
    #                 st.markdown("**Ratings**")
    #                 col1, col2 = st.columns(2)
    #                 with col1:
    #                     st.write(f"Overall Satisfaction: {survey['satisfaction_ratings']['overall']}/5")
    #                     st.write(f"Response Time: {survey['satisfaction_ratings']['response_time']}")
                    
    #                 # Resolution Status
    #                 st.markdown("**Resolution Status**")
    #                 st.write(f"Issue Resolved: {survey['resolution']['issue_resolved']}")
    #                 if survey['resolution'].get('pending_issues'):
    #                     st.write("Pending Issues:", survey['resolution']['pending_issues'])
                    
    #                 # Detailed Feedback
    #                 st.markdown("**Detailed Feedback**")
    #                 if 'detailed_feedback' in survey and survey['detailed_feedback'].get('strengths'):
    #                     st.write("Strengths:", survey['detailed_feedback']['strengths'])
    #                 if 'detailed_feedback' in survey and survey['detailed_feedback'].get('improvements'):
    #                     st.write("Areas for Improvement:", survey['detailed_feedback']['improvements'])
    #                 if 'detailed_feedback' in survey and survey['detailed_feedback'].get('additional_comments'):
    #                     st.write("Additional Comments:", survey['detailed_feedback']['additional_comments'])
    #     else:
    #         st.info("No survey responses yet.")

    # with tabs[3]:
    #     st.header("Survey Results")
        
    
    #     survey_data = list(db.survey.find({}, {'_id': 0}))
        
    #     if survey_data:
          
    #         flattened_data = []
    #         for survey in survey_data:
    #             flat_dict = {
    #                 'Customer Name': survey['customer_info']['name'],
    #                 'Email': survey['customer_info']['email'],
    #                 'Contact': survey['customer_info']['contact_number'],
    #                 'Overall Satisfaction': survey['satisfaction_ratings']['overall'],
    #                 'Response Time': survey['satisfaction_ratings']['response_time'],
    #                 'Issue Resolution': survey['resolution']['issue_resolved'],
    #                 'Pending Issues': survey['resolution'].get('pending_issues', 'None'),
    #             }
    #             flattened_data.append(flat_dict)
            
    #         # Convert to DataFrame
    #         survey_df = pd.DataFrame(flattened_data)
            
    #         # Display metrics
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             avg_satisfaction = survey_df['Overall Satisfaction'].mean()
    #             st.metric("Average Satisfaction", f"{avg_satisfaction:.1f}/5")
    #         with col2:
    #             resolved_rate = (survey_df['Issue Resolution'] == 'Yes').mean() * 100
    #             st.metric("Resolution Rate", f"{resolved_rate:.1f}%")
    #         with col3:
    #             st.metric("Total Surveys", len(survey_df))
            
         
    #         st.subheader("Survey Overview")
    #         st.dataframe(
    #             survey_df,
    #             column_config={
    #                 "Customer Name": "Customer",
    #                 "Overall Satisfaction": st.column_config.NumberColumn(
    #                     "Satisfaction",
    #                     help="Overall satisfaction rating out of 5",
    #                     format="%.1f ⭐"
    #                 ),
    #             },
    #             hide_index=True,
    #             use_container_width=True
    #         )
            
         
    #         st.subheader("Detailed Feedback")
    #         for survey in survey_data:
    #             with st.expander(f"{survey['customer_info']['name']}"):
    #                 # Create two columns for feedback
    #                 col1, col2 = st.columns(2)
                    
    #                 with col1:
    #                     st.markdown("**Customer Details**")
    #                     details_df = pd.DataFrame({
    #                         'Field': ['Name', 'Email', 'Contact'],
    #                         'Value': [
    #                             survey['customer_info']['name'],
    #                             survey['customer_info']['email'],
    #                             survey['customer_info']['contact_number']
    #                         ]
    #                     })
    #                     st.dataframe(details_df, hide_index=True)
                    
    #                 with col2:
    #                     st.markdown("**Ratings**")
    #                     ratings_df = pd.DataFrame({
    #                         'Metric': ['Overall Satisfaction', 'Response Time'],
    #                         'Rating': [
    #                             f"{survey['satisfaction_ratings']['overall']}/5",
    #                             survey['satisfaction_ratings']['response_time']
    #                         ]
    #                     })
    #                     st.dataframe(ratings_df, hide_index=True)
                    
    #                 st.markdown("**Issue Details**")
    #                 issue_df = pd.DataFrame({
    #                     'Field': ['Resolution Status', 'Pending Issues'],
    #                     'Value': [
    #                         survey['resolution']['issue_resolved'],
    #                         survey['resolution'].get('pending_issues', 'None')
    #                     ]
    #                 })
    #                 st.dataframe(issue_df, hide_index=True)
                    
    #                 if 'detailed_feedback' in survey:
    #                     st.markdown("**Feedback Comments**")
    #                     feedback_df = pd.DataFrame({
    #                         'Category': ['Strengths', 'Improvements', 'Additional Comments'],
    #                         'Comments': [
    #                             survey['detailed_feedback'].get('strengths', 'None provided'),
    #                             survey['detailed_feedback'].get('improvements', 'None provided'),
    #                             survey['detailed_feedback'].get('additional_comments', 'None provided')
    #                         ]
    #                     })
    #                     st.dataframe(feedback_df, hide_index=True)
    #     else:
    #         st.info("No survey responses yet.")

except Exception as e:
    st.error(f"Error connecting to MongoDB: {str(e)}")