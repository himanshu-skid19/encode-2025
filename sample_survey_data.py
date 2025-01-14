import datetime
from pymongo import MongoClient
# Connect to MongoDB
mongoURI = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'
client = MongoClient(mongoURI)

db = client.ENCODE
# Code to insert sample survey data
def insert_sample_surveys():
    sample_surveys = [
        {
            "customer_info": {
                "name": "John Doe",
                "email": "john@example.com",
                "contact_number": "123-456-7890"
            },
            "satisfaction_ratings": {
                "overall": 4,
                "response_time": "Fast"
            },
            "resolution": {
                "issue_resolved": "Yes",
                "pending_issues": None
            },
            "product_feedback": {
                "satisfaction": "Satisfied",
                "would_recommend": "Definitely"
            },
            "detailed_feedback": {
                "strengths": "Quick response and professional service",
                "improvements": "None at this time",
                "additional_comments": "Great experience overall"
            },
            "submission_date": datetime.datetime.now()
        },
        {
            "customer_info": {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "contact_number": "987-654-3210"
            },
            "satisfaction_ratings": {
                "overall": 3,
                "response_time": "Average"
            },
            "resolution": {
                "issue_resolved": "Partially",
                "pending_issues": "Still waiting for refund processing"
            },
            
            "product_feedback": {
                "satisfaction": "Neutral",
                "would_recommend": "Maybe"
            },
            "detailed_feedback": {
                "strengths": "Staff was friendly",
                "improvements": "Faster refund processing",
                "additional_comments": "Please follow up on pending refund"
            },
            "submission_date": datetime.datetime.now()
        },
        {
            "customer_info": {
                "name": "Robert Wilson",
                "email": "robert@example.com",
                "contact_number": "555-123-4567"
            },
            
            "satisfaction_ratings": {
                "overall": 5,
                "response_time": "Very Fast"
            },
            "resolution": {
                "issue_resolved": "Yes",
                "pending_issues": None
            },
            
            "product_feedback": {
                "satisfaction": "Very Satisfied",
                "would_recommend": "Definitely"
            },
            "detailed_feedback": {
                "strengths": "Excellent product knowledge and support",
                "improvements": "Everything was perfect",
                "additional_comments": "Will definitely recommend to others"
            },
            "submission_date": datetime.datetime.now()
        }
    ]

    try:
        # Insert the sample data
        result = db.survey.insert_many(sample_surveys)
      #  st.success(f"Successfully inserted {len(result.inserted_ids)} sample surveys")
    except Exception as e:
        print(f"Error inserting sample data: {str(e)}")
        #st.error(f"Error inserting sample data: {str(e)}")

# Add a button to insert sample data
# if st.button("Insert Sample Survey Data"):
#     insert_sample_surveys()

if __name__ == "__main__":
    insert_sample_surveys()