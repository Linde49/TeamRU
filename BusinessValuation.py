import math
from Transactions import Transaction

class BusinessValuation(Transaction):
    def __init__(self, json_file_path: str = "business_bank_transactions.json"):
        # Initialize the parent Transaction class
        super().__init__(json_file_path)

# ---------------------------------------------
# Calculates the Weighted SDE
# ---------------------------------------------        
    def calculate_sde_weighted(self, period_incomes: list[float], periods_per_year: int) -> float:

        # ---------------------------------------------
        # Inner function to analyze income averages and categorize periods
        # ---------------------------------------------
        def evaluate_periods(incomes: list[float]):
            num_periods = len(incomes)
            if num_periods == 0:
                return 0, 0, 0.0, 0.0
                
            average_income = sum(incomes) / num_periods
            
            good_period_count = 0
            slow_period_count = 0
            good_income_total = 0.0
            slow_income_total = 0.0
            
            for income in incomes:
                if income > average_income:
                    good_period_count += 1
                    good_income_total += income
                else:
                    slow_period_count += 1
                    slow_income_total += income
                    
            pct_good = good_period_count / num_periods
            pct_slow = slow_period_count / num_periods
            
            return good_income_total, slow_income_total, pct_good, pct_slow

        good_income, slow_income, pct_good, pct_slow = evaluate_periods(period_incomes)
        
        sde_weighted = ((good_income * pct_good) + (slow_income * pct_slow)) * periods_per_year
        return sde_weighted

# ---------------------------------------------
# Calculates the compounding factor
# ---------------------------------------------
    def calculate_compounding_factor(self, current_day_income: float, previous_day_income: float, n: int) -> float:
        if previous_day_income == 0:
            # Defaults to 0 growth (factor of 1) to avoid division by 0.
            g = 0.0 
        else:
            g = (current_day_income - previous_day_income) / previous_day_income
            
        compounding_factor = (1 + g) ** n
        return compounding_factor

# ---------------------------------------------
# Calculates the multiplier
# ---------------------------------------------

    def calculate_multiplier(self, current_balance: float, previous_balance: float) -> float:

        # ---------------------------------------------
        # Inner function to calculate the risk deduction modifier
        # ---------------------------------------------
        def riskDeduction_calculator(current: float, previous: float) -> float:
            risk_deduction = 0.0
            
            if current > previous:
                risk_deduction += 0.25
            elif current < previous:
                risk_deduction -= 0.25
                
            return risk_deduction
            
        risk_deductions = riskDeduction_calculator(current_balance, previous_balance)
        
        multiplier = 1.50 - risk_deductions
        
        return multiplier

    def calculate_future_value(self, sde_weighted: float, compounding_factor: float, multiplier: float) -> float:
        return sde_weighted * compounding_factor * multiplier