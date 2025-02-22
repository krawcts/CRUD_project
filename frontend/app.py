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

# Add Product
with st.expander("Add a New Product"):
    with st.form("new_product"):
        name = st.text_input("Product Name")
        description = st.text_area("Product Description")
        price = st.number_input("Price", min_value=0.01, format="%f")
        category = st.selectbox(
            "Category",
            ["Electronics", "Appliances", "Furniture", "Clothing", "Shoes"],
        )
        supplier_email = st.text_input("Supplier Email")
        submit_button = st.form_submit_button("Add Product")

        if submit_button:
            response = requests.post(
                "http://backend:8000/products/",
                json={
                    "name": name,
                    "description": description,
                    "price": price,
                    "category": category,
                    "supplier_email": supplier_email,
                },
            )
            show_response_message(response)
          
# View Products
with st.expander("View Products"):
    if st.button("Show All Products"):
        response = requests.get("http://backend:8000/products/")
        if response.status_code == 200:
            products = response.json()
            df = pd.DataFrame(products)

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "category",
                    "supplier_email",
                    "created_at",
                ]
            ]

            # Display the DataFrame without the index
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Get Product Details
with st.expander("Get Product Details"):
    get_id = st.number_input("Product ID", min_value=1, format="%d")
    if st.button("Fetch Product"):
        response = requests.get(f"http://backend:8000/products/{get_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "category",
                    "supplier_email",
                    "created_at",
                ]
            ]

            # Display the DataFrame without the index
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Delete Product
with st.expander("Delete Product"):
    delete_id = st.number_input("Product ID to Delete", min_value=1, format="%d")
    if st.button("Delete Product"):
        response = requests.delete(f"http://backend:8000/products/{delete_id}")
        show_response_message(response)

# Update Product
with st.expander("Update Product"):
    with st.form("update_product"):
        update_id = st.number_input("Product ID", min_value=1, format="%d")
        new_name = st.text_input("New Product Name")
        new_description = st.text_area("New Product Description")
        new_price = st.number_input(
            "New Price",
            min_value=0.01,
            format="%f",
        )
        new_category = st.selectbox(
            "New Category",
            ["Electronics", "Appliances", "Furniture", "Clothing", "Shoes"],
        )
        new_email = st.text_input("New Supplier Email")

        update_button = st.form_submit_button("Update Product")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_price > 0:
                update_data["price"] = new_price
            if new_email:
                update_data["supplier_email"] = new_email
            if new_category:
                update_data["category"] = new_category

            if update_data:
                response = requests.put(
                    f"http://backend:8000/products/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("No information provided for update")