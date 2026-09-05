class Communication:
    def __init__(self, valuation):
        self.valuation = valuation
        # Ensure bank offers are always loaded (you can load them from a JSON or keep them static)
        self.bank_offers = [
            {"bank": "Standard Bank", "offer": "0% Interest for 3 months"},
            {"bank": "FNB", "offer": "R500 Cashback on Business Credit Card"},
            {"bank": "Capitec", "offer": "No monthly fees for 6 months"}
        ]

    def generate_alerts(self):
        alerts = []
        if self.valuation.current_balance < 0:
            alerts.append("Warning: Your business account is in overdraft!")
        elif self.valuation.current_balance > 0:
            alerts.append("Great news: Positive balance detected.")
        else:
            alerts.append("Alert: Balance is zero.")

        # Always append Bank Offers
        alerts.append("Your Available Bank Offers:")
        for offer in self.bank_offers:
            alerts.append(f"- {offer['bank']}: {offer['offer']}")
            
        return alerts