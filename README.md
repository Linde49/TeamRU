# TeamRU
# Nexus - Business Finance Dashboard

FinTrack is a lightweight Flask-based web application designed for SMMEs (like Spaza shops) to visualize their financial health, automatically process Yoco card settlements as deposits, calculate future business valuations, and assess loan readiness. The UI features a modern, deep-green professional theme.

## Features

- **Interactive Dashboard**: Displays real-time revenue, expenses, net profit, cash available, and a 6-month income vs. expense bar chart.
- **Yoco Settlement Logic**: Automatically detects transactions containing "yoco" or "settlement" in the description, converts them to positive amounts, and categorizes them as **Deposits** (Income).
- **Advanced Business Valuation**: Calculates Weighted SDE (Seller's Discretionary Earnings), Compounding Factors, Risk Multipliers, and Future Valuation directly from your transaction data.
- **Loan Readiness & Bank Offers**: Generates a loan readiness score and displays a list of bank offers from major South African banks.
- **Transaction Management**: View, categorize, and add new transactions directly through the GUI.
- **No External Database**: Uses a simple, easy-to-edit JSON file for data storage.

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3 (Custom Green Theme), Vanilla JavaScript (Fetch API)
- **Data Storage**: `business_bank_transactions.json`

## Project Structure
 
-Hackathon:
    -_pycache_
    - templates
        -finanace_app_GUI.html
    - app.py
    - BusinessValuation.py
    - Communications.py
    - transactions.py
    - README.md

> **IMPORTANT NOTE ON FILE NAME**: The template file in project is named `finanace_app_GUI.html`. Please ensure you do not rename this unless you also update `render_template('finanace_app_GUI.html')` in `app.py`.

## Prerequisites

- Python 3.7+ installed on your system.
- Flask installed (`pip install flask`).

## Setup and Installation

1. **Clone or download** the project files into a folder.
2. **Navigate to the folder** in your terminal/command prompt:
   ```bash
   cd path/to/your-project-folder
3. install flask: pip install flask

**Running the application**:
1. Start flask development server: python/ py app.py
2. Open web browswer and go to : http://127.0.0.1:5000


**Data Format (business_bank_transactions.json)**
The backend is strict about parsing this file. It must start with a square bracket [ (a list), OR be wrapped in a dictionary with a key like transactions, data, items, results, or records.

Example of a valid JSON list:

[
    {"date": "2026-09-01", "description": "Yoco Settlement", "amount": 1500.00, "type": "Deposit"},
    {"date": "2026-09-02", "description": "Groceries", "amount": -50.00, "type": "Expense"}
]


**Business Valuation Logic**

The BusinessValuation class in app.py uses the following formulas based on your transaction data:

Weighted SDE: Averages income periods, weights good/slow periods, and multiplies by annual periods.

Compounding Factor: Uses day-over-day income growth to project future growth.

Risk Multiplier: Adjusts based on whether current balance is higher or lower than the previous balance.

Future Value: SDE Weighted * Compounding Factor * Risk Multiplier

**Known Limitations / Customizations**

Business Profile: By design, the "Business data" form does NOT store data to a backend file. It purely uses the "Karabo's Spaza" hardcoded profile and dynamically calculates revenue from your JSON file.

Storing New Transactions: Clicking "Save Transaction" on the Transactions tab will append the new entry directly to your business_bank_transactions.json file.

Color Palette: The entire UI uses a custom deep-green palette (based on #DAF1DE, #235347, #0B2B26). The Expense and Income badges use white backgrounds with red and green borders respectively, purely for high visual contrast.

**API Endpoints**
The frontend uses these internal API routes for its dynamic data:

GET /api/dashboard - Fetches stats, chart data, recent transactions, and loan score.

GET /api/transactions - Fetches the full transaction history.

GET /api/loan - Fetches valuation metrics and bank offers.

GET/POST /api/business - Retrieves hardcoded business data (GET) or ignores POST data.

POST /api/transaction - Adds a new transaction to the JSON file.

**Troubleshooting**
GUI is empty: Ensure your JSON file has data inside it, starts with [, and that your template file is named exactly finanace_app_GUI.html.

TemplateNotFound error: Check the spelling of the HTML file in your templates folder and ensure it matches the string in app.py.

Transactions showing as Expenses: Ensure Yoco settlements contain the word "yoco" or "settlement" in their description for automatic deposit logic to trigger.