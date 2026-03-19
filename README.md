# AI-Powered SQL Query Builder

An **AI-powered SQL Query Builder** built with **Streamlit** and **Mistral AI API**.  

Convert natural language queries into SQL statements and execute them on a local SQLite database instantly.

---

## Features

- Convert English text into SQL queries using Mistral AI  
- Execute SQL queries safely on a local SQLite database  
- Display query results in an interactive table  
- Download query results as CSV  
- Simple, intuitive Streamlit web interface  

---

## Database Schema

**Table:** `customers`

| Column           | Type    |
|-----------------|---------|
| id              | INTEGER PRIMARY KEY |
| name            | TEXT    |
| orders          | INTEGER |
| last_order_date | TEXT    |

Sample data is automatically inserted when running the app for the first time.

---

## How to Run

1. **Clone the repo:**

```bash
git clone https://github.com/aarushij978/sqlquerybuilder.git
cd sqlquerybuilder
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set your Mistral API key (optional for AI part):**
Option 1: Use environment variable:
```bash
export MISTRAL_API_KEY="your_api_key_here"
```
Option 2: Create a .env file in the project root:
```bash
MISTRAL_API_KEY=your_api_key_here
```

5. **Run the app:**
```bash
streamlit run sqlbuilder.py
```

6. **Open in browser:**
```bash
http://localhost:8501
```
---

## Demo Screenshots

Place your screenshots in the demo_screenshots/ folder and update the filenames if needed.

1. Show all customers

2. Customers with more than 3 orders

## Notes

- Only SELECT queries are allowed for safety.
- SQLite is used for simplicity — no external database installation required.
- our API key is optional; the app will still run with the sample DB.

## Tech Stack

- Python 3
- Streamlit — Web app framework
- SQLite — Local database
- Pandas — For displaying query results
- Mistral AI API — Converts natural language → SQL



## Folder Structure (Recommended)
sqlquerybuilder/
├─ sqlbuilder.py             # Main Streamlit app
├─ requirements.txt          # Dependencies
├─ README.md                 # Project README
├─ demo_screenshots/   
│   ├─ SQL_Query_Builder_Page.png
│   ├─ all_customers.png
│   └─ customers_gt_3_orders.png
├─ sample.db (optional)      # Auto-generated SQLite DB
├─ .env (not committed)      # API key (optional)
└─ .gitignore                # Ignore venv, __pycache__, .env, etc.
