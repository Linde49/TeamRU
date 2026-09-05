import json

class Transaction:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

    @classmethod
    def from_json(cls, data):
         # If 'type' is in the data, rename it to 'category'
        if 'type' in data and 'category' not in data:
            data['category'] = data.pop('type')
        
        # If there are any OTHER unexpected keys, ignore them
        valid_keys = {'date', 'description', 'amount', 'category'}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        
        return cls(**filtered_data)

    def process_transaction_type(self):
        if "yoco" in self.description.lower() or "settlement" in self.description.lower():
            self.amount = abs(self.amount)  # Treat as deposit
            self.category = "Deposit"
            return "Deposit"
        elif self.amount > 0:
            self.category = "Deposit"
            return "Deposit"
        else:
            self.category = "Expenditure"
            return "Expenditure"