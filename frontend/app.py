import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.image("logo.png", width=200)

st.title("Product Management")

# Helper function to display detailed error messages
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operation completed successfully!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # If the error is a list, extract the messages from each error
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Error: {errors}")
                else:
                    # Otherwise, show the error message directly
                    st.error(f"Error: {data['detail']}")
        except ValueError:
            st.error("Unknown error. Failed to decode the response.")