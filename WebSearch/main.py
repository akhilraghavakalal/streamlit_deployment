import os
import streamlit as st
from dotenv import load_dotenv
import openai

# Set page title
st.set_page_config(page_title="OpenAI API Demo")

# Load environment variables
load_dotenv()

# Get the API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Create a function to get response from OpenAI
def get_openai_response(query):
    # Creating the client and configuring the key
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        response = client.responses.create(
            model="gpt-4.1",
            tools=[
                {
                    "type": "web_search_preview",
                    # location specific query
                    "user_location": {
                        "type": "approximate",
                        "country": "US",
                        "city": "Normal",
                        "region": "Chicago",
                    },
                    "search_context_size": "medium",  # handles response size and thus cost
                }
            ],
            input=query
        )
        return response.output_text
    except Exception as e:
        return f"Error: {str(e)}"

# Main app
def main():
    st.title("OpenAI Websearch Demo")
    
    # Description
    st.write("Enter your query and get a response from OpenAI websearch API")
    
    # Text input for the query
    query = st.text_area("Enter your query:", height=100)
    
    # Submit button
    if st.button("Submit"):
        if query:
            with st.spinner("Generating response..."):
                response = get_openai_response(query)
                
            # Display the response
            st.markdown("### Response:")
            st.write(response)
        else:
            st.warning("Please enter a query.")
    
    # # Display the API key status
    # if OPENAI_API_KEY:
    #     st.sidebar.success("API Key Loaded")
    # else:
    #     st.sidebar.error("API Key Not Found. Please check your .env file.")
    
    # # Add a note about the .env file
    # st.sidebar.markdown("### Note:")
    # st.sidebar.markdown("Make sure you have a .env file with your OPENAI_API_KEY.")

if __name__ == "__main__":
    main()