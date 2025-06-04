import streamlit as st
import pandas as pd
from dateutil import parser

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("loan_data.csv", parse_dates=['Date'])

df = load_data()

# Sidebar - Report Dates and Product Filters
st.sidebar.header("📅 Available Report Dates")
unique_dates = sorted(df['Date'].dt.strftime("%Y-%m-%d").unique())
for date in unique_dates:
    st.sidebar.write(f"- {date}")

st.sidebar.header("📦 Available Products")
unique_products = df['Product Type'].unique()
for prod in unique_products:
    st.sidebar.write(f"- {prod}")

# Title
st.title("📘 Chat with Namrata")

# Input box
query = st.text_input("Ask a question (e.g., 'gold loan on 25 May 2025', '2025-05-24', 'business loan')")

# Data filtering based on query
if query:
    with st.spinner("Filtering data..."):
        query_lower = query.lower()
        filtered_df = df.copy()
        date_found = False
        product_found = False

        # Try to find a date
        try:
            parsed_date = parser.parse(query, fuzzy=True)
            if parsed_date.year >= df['Date'].dt.year.min() and parsed_date.year <= df['Date'].dt.year.max():
                filtered_df = filtered_df[filtered_df['Date'].dt.date == parsed_date.date()]
                date_found = True
        except ValueError:
            pass

        # Try to find a product
        matched_product = None
        for prod in unique_products:
            if prod.lower() in query_lower:
                matched_product = prod
                product_found = True
                break

        if product_found:
            filtered_df = filtered_df[filtered_df['Product Type'] == matched_product]

        if not filtered_df.empty:
            st.success("Showing filtered data:")
            st.dataframe(filtered_df)

            # Calculate and display the sum of amount for the filtered data
            sum_of_amount = filtered_df['Amount'].sum()
            st.subheader("Total Amount in Filtered Data:")
            st.metric("Total Amount", f"₹ {sum_of_amount:,.2f}")

            # Display a bar chart of the amount by product type in the filtered data
            st.subheader("Amount by Product Type (Filtered)")
            product_amount = filtered_df.groupby('Product Type')['Amount'].sum().reset_index()
            st.bar_chart(product_amount, x='Product Type', y='Amount')

        else:
            st.info("No data matches your query.")

else:
    st.info("Showing all data.")
    st.dataframe(df)

    # Calculate and display the sum of amount for all data
    total_amount = df['Amount'].sum()
    st.subheader("Total Amount in All Data:")
    st.metric("Total Amount", f"₹ {total_amount:,.2f}")

    # Display a bar chart of the amount by product type for all data
    st.subheader("Amount by Product Type (All Data)")
    all_product_amount = df.groupby('Product Type')['Amount'].sum().reset_index()
    st.bar_chart(all_product_amount, x='Product Type', y='Amount')