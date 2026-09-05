import json, os
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'business_bank_transactions.json')

# ---- Transaction Class (Yoco Logic) ----
class Transaction:
    def __init__(self, date, description, amount, type=None, category=None):
        self.date = str(date)
        self.description = str(description)
        self.amount = float(amount)
        self.type = type if type else category
        self.process_type()

    @classmethod
    def from_json(cls, data):
        valid_keys = {'date', 'description', 'amount', 'type', 'category'}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    def process_type(self):
        if "yoco" in self.description.lower() or "settlement" in self.description.lower():
            self.amount = abs(self.amount)
            self.type = "Deposit"
        elif self.amount > 0:
            self.type = "Deposit"
        else:
            self.type = "Expense"
        self.frontend_type = 'income' if self.type == 'Deposit' else 'expense'

# ---- Valuation Class ----
class BusinessValuation:
    def __init__(self, transactions):
        self.transactions = transactions
        self.current_balance = sum(t.amount for t in transactions if t.frontend_type == 'income') - sum(abs(t.amount) for t in transactions if t.frontend_type == 'expense')
    def calculate_sde_weighted(self, period_incomes, periods_per_year=12):
        if not period_incomes: return 0
        avg = sum(period_incomes) / len(period_incomes)
        good = sum(i for i in period_incomes if i > avg)
        slow = sum(i for i in period_incomes if i <= avg)
        pct_good = sum(1 for i in period_incomes if i > avg) / len(period_incomes)
        pct_slow = 1 - pct_good
        return ((good * pct_good) + (slow * pct_slow)) * periods_per_year
    def calculate_compounding_factor(self, c, p, n=12):
        return (1 + (0 if p == 0 else (c - p) / p)) ** n
    def calculate_multiplier(self, c, p):
        return 1.50 - (0.25 if c > p else -0.25 if c < p else 0)
    def calculate_future_value(self, sde, comp, mult):
        return sde * comp * mult

# ---- Load Data ----
def load_transactions():
    import os
    if not os.path.exists(DATA_FILE): 
        print(f"Error: File {DATA_FILE} not found")
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            raw_data = json.load(f)
        if isinstance(raw_data, dict):
            for key in ['transactions', 'data', 'items', 'results', 'records']:
                if key in raw_data and isinstance(raw_data[key], list):
                    raw_data = raw_data[key]
                    break
        if not isinstance(raw_data, list): return []
        return [Transaction.from_json(item) for item in raw_data]
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

# ---- API ROUTES (Required for your GUI's JavaScript) ----
@app.route('/api/dashboard')
def api_dashboard():
    transactions = load_transactions()
    total_income = sum(t.amount for t in transactions if t.frontend_type == 'income')
    total_expenses = sum(abs(t.amount) for t in transactions if t.frontend_type == 'expense')
    net_profit = total_income - total_expenses

    today = datetime.now()
    chart_data = []
    for i in range(5, -1, -1):
        month = (today - timedelta(days=30 * i)).strftime('%Y-%m')
        m_income = sum(t.amount for t in transactions if t.frontend_type == 'income' and t.date.startswith(month))
        m_expense = sum(abs(t.amount) for t in transactions if t.frontend_type == 'expense' and t.date.startswith(month))
        chart_data.append({"month": month, "income": m_income, "expense": m_expense})

    recent_tx = [{"date": t.date, "description": t.description, "category": t.type, "type": t.frontend_type, "amount": abs(t.amount)} for t in transactions[-5:]]

    score = 60 if net_profit > 0 else 30
    score = min(100, score + 10 if total_income > 10000 else score)

    return jsonify({
        "stats": {"revenue": total_income, "expenses": total_expenses, "profit": net_profit, "cash": net_profit},
        "chart": chart_data,
        "recent": recent_tx,
        "loan": {"score": score, "checks": ["Bank statement tracked", "Transactions categorised", "Positive profitability" if net_profit > 0 else "Negative profitability"]}
    })

@app.route('/api/transactions')
def api_transactions():
    transactions = load_transactions()
    return jsonify([{"date": t.date, "description": t.description, "category": t.type, "type": t.frontend_type, "amount": abs(t.amount)} for t in transactions])

@app.route('/api/business', methods=['GET', 'POST'])
def api_business():
    transactions = load_transactions()
    total_income = sum(t.amount for t in transactions if t.frontend_type == 'income')
    return jsonify({
        "business": "Karabo's Spaza", "owner": "Karabo", "industry": "Retail / Spaza shop",
        "yearsTrading": 2, "employees": 1, "typicalMonthlyRevenue": total_income, "notes": "Calculated from JSON."
    })

@app.route('/api/loan')
def api_loan():
    transactions = load_transactions()
    incomes = [t.amount for t in transactions if t.frontend_type == 'income']
    valuation = BusinessValuation(transactions)
    sde = valuation.calculate_sde_weighted(incomes)
    comp = valuation.calculate_compounding_factor(sum(incomes), sum(incomes)*0.9)
    mult = valuation.calculate_multiplier(valuation.current_balance, valuation.current_balance - 1000)
    cfv = valuation.calculate_future_value(sde, comp, mult)
    offers = [{"bank": "Standard Bank", "decision": "OFFERED", "amount": 50000, "rate": 0.125}, {"bank": "FNB", "decision": "OFFERED", "amount": 75000, "rate": 0.115}]
    score = min(100, 50 + (20 if cfv > 50000 else 0) + (20 if valuation.current_balance > 0 else 0))
    return jsonify({"cfv": cfv, "sde_weighted": sde, "compounding_factor": comp, "multiplier": mult, "score": score, "offers": offers, "checks": ["All transactions tracked", "Loan readiness calculated", "Offers available"]})

@app.route('/api/transaction', methods=['POST'])
def api_add_transaction():
    data = request.get_json()
    amount = float(data.get('amount'))
    if data.get('type') == 'expense': amount = -abs(amount)
    new_tx = {"date": data.get('date'), "description": data.get('description'), "amount": amount, "type": "Deposit" if data.get('type') == 'income' else "Expense", "category": data.get('category')}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f: transactions = json.load(f)
    else:
        transactions = []
    transactions.append(new_tx)
    with open(DATA_FILE, 'w') as f: json.dump(transactions, f, indent=4)
    return jsonify({"message": "Transaction saved"})

# ---- Main Route ----
@app.route('/')
def index():
    return render_template('finanace_app_GUI.html')

if __name__ == '__main__':
    app.run(debug=True)