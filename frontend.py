import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import backend as db

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Finance: Revenue & Expense Tracker")

st.title("💰 Finance: Revenue & Expense Tracker")

# --- Business Insights Section ---
st.header("Business Insights")
col1, col2, col3, col4 = st.columns(4)

total_transactions = db.get_transaction_counts()
total_revenue = db.get_total_revenue()
total_expense = db.get_total_expense()
net_income = total_revenue - total_expense

col1.metric("Total Transactions", total_transactions)
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Total Expenses", f"${total_expense:,.2f}")
col4.metric("Net Income", f"${net_income:,.2f}", delta=f"{net_income - 0:,.2f}", delta_color="normal")

st.write("---")

# --- Transaction Management Section (CRUD) ---
st.header("Transaction Management")
operation = st.selectbox("Select an operation:", ["Create", "Update", "Delete"])

if operation == "Create":
    st.subheader("Create a New Transaction")
    with st.form("create_form"):
        transaction_date = st.date_input("Transaction Date", datetime.now())
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        transaction_type = st.selectbox("Type", ["Revenue", "Expense"])
        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            transaction_id = str(uuid.uuid4())
            result = db.create_transaction(transaction_id, transaction_date, description, amount, transaction_type)
            st.success(result)

elif operation == "Update":
    st.subheader("Update an Existing Transaction")
    transactions = db.read_transactions()
    transaction_ids = [t[0] for t in transactions]
    selected_id = st.selectbox("Select Transaction ID to Update:", transaction_ids)
    
    if selected_id:
        current_data = next((t for t in transactions if t[0] == selected_id), None)
        if current_data:
            current_description = current_data[2]
            current_amount = current_data[3]
            
            with st.form("update_form"):
                new_description = st.text_input("New Description", value=current_description)
                new_amount = st.number_input("New Amount", value=float(current_amount), min_value=0.01, format="%.2f")
                submitted = st.form_submit_button("Update Transaction")
                if submitted:
                    result = db.update_transaction(selected_id, new_description, new_amount)
                    st.success(result)

elif operation == "Delete":
    st.subheader("Delete a Transaction")
    transactions = db.read_transactions()
    transaction_ids = [t[0] for t in transactions]
    selected_id = st.selectbox("Select Transaction ID to Delete:", transaction_ids)
    
    if selected_id:
        if st.button("Confirm Delete"):
            result = db.delete_transaction(selected_id)
            st.warning(result)

st.write("---")

# --- Read & Filter Transactions Section ---
st.header("All Transactions")
col5, col6 = st.columns(2)
transaction_type_filter = col5.selectbox("Filter by Type", ["All", "Revenue", "Expense"])
sort_by_option = col6.selectbox("Sort by", ["None", "Amount", "Date"])

transactions_data = db.read_transactions(transaction_type=transaction_type_filter, sort_by=sort_by_option)

if transactions_data:
    df = pd.DataFrame(transactions_data, columns=["Transaction ID", "Date", "Description", "Amount", "Type"])
    st.dataframe(df)
else:
    st.info("No transactions to display.")