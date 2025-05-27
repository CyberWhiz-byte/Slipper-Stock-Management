import streamlit as st
import pandas as pd
import os

# File path for stock CSV
stock_file = "Enhanced_Stocks(Available Stocks Only).csv"

# Load stock data
def load_stock():
    if os.path.exists(stock_file):
        return pd.read_csv(stock_file)
    else:
        return pd.DataFrame(columns=["Model Number", "Stock Set"])

# Save stock data
def save_stock(df):
    df.to_csv(stock_file, index=False)

st.title("Slipper Stock Management")

# Load stock data
stock_df = load_stock()

# Show current stock
st.subheader("Current Stock")
st.dataframe(stock_df)

# Transaction form
st.subheader("Update Stock")
model_number = st.selectbox("Model Number", stock_df["Model Number"].unique())
quantity = st.number_input("Quantity", min_value=1, step=1)
action = st.radio("Action", ["Sale", "Restock"])

if st.button("Apply Transaction"):
    if action == "Sale":
        stock_df.loc[stock_df["Model Number"] == model_number, "Stock Set"] -= quantity
    elif action == "Restock":
        stock_df.loc[stock_df["Model Number"] == model_number, "Stock Set"] += quantity

    save_stock(stock_df)
    st.success(f"{action} of {quantity} applied to {model_number}.")

    # Reload and show updated stock
    stock_df = load_stock()
    st.dataframe(stock_df)

# Option to add a new model
st.subheader("Add New Model")
new_model = st.text_input("New Model Number")
new_stock = st.number_input("Initial Stock", min_value=0, step=1, key="new")

if st.button("Add Model"):
    if new_model and new_model not in stock_df["Model Number"].values:
        stock_df = stock_df.append({"Model Number": new_model, "Stock Set": new_stock}, ignore_index=True)
        save_stock(stock_df)
        st.success(f"Model {new_model} added with {new_stock} units.")
        st.dataframe(stock_df)
    else:
        st.error("Model already exists or name is empty.")
