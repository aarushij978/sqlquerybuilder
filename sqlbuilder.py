import streamlit as st
import requests
import sqlite3
import pandas as pd

# Create/connect to local database
conn = sqlite3.connect("sample.db", check_same_thread=False)

# Create table (only runs if not exists)
conn.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    orders INTEGER,
    last_order_date TEXT
)
""")

# Insert sample data (only if table is empty)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM customers")
count = cursor.fetchone()[0]

if count == 0:
    conn.execute("INSERT INTO customers (name, orders, last_order_date) VALUES ('Aarushi', 5, '2025-02-10')")
    conn.execute("INSERT INTO customers (name, orders, last_order_date) VALUES ('Rohan', 2, '2025-02-15')")
    conn.execute("INSERT INTO customers (name, orders, last_order_date) VALUES ('Sneha', 7, '2025-01-20')")
    conn.commit()



# API configuration
API_KEY = "CS2iq3kE5NTmtA97BjhkmprNEya6EuQH"
API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

# Static instruction prompt for SQL query generation
static_context = """
You are an expert SQL assistant.

Database schema:
Table: customers(id, name, orders, last_order_date)

Convert the following natural language question into SQL.
Only return SQL. No explanation.
"""

def call_mistral_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "open-mixtral-8x22b",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [])[0].get("message", {}).get("content", "")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except (IndexError, KeyError) as e:
        return f"Unexpected response format: {e}"

def main():
    st.markdown(
        """
        <h1 style='text-align: center;'>SQL Query Builder</h1>
        <h3 style='text-align: center; font-weight: normal;'>Describe your query in English and get a working SQL statement!</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("Enter your query description in English")

    query_description = st.text_area(
        "Describe what you want to do with the database:",
        placeholder="e.g., Get the names of all customers who placed more than 3 orders last month."
    )

    if st.button("Generate SQL Query"):
        if not query_description.strip():
            st.error("Please enter a query description.")
            return

        prompt = f"{static_context}\n\nNatural Language Input:\n{query_description}"
        sql_result = call_mistral_api(prompt)

        st.markdown("### Generated SQL Query")
        st.code(sql_result, language='sql')

        # ✅ Execute SQL query safely (FIXED INDENTATION)
        try:
            if any(word in sql_result.lower() for word in ["delete", "drop", "update", "insert"]):
                st.error("Only SELECT queries are allowed.")
            else:
                df = pd.read_sql_query(sql_result, conn)
                st.markdown("### Query Results")
                st.dataframe(df)

                st.download_button(
                    "Download Results as CSV",
                    df.to_csv(index=False),
                    "results.csv"
                )

        except Exception as e:
            st.error(f"Error executing query: {e}")

if __name__ == "__main__":
    main()
