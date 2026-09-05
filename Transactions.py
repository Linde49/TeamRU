import json
import os

class Transaction:
    def __init__(self, json_file_path: str = "business_bank_transactions.json"):
        self.__file_path = json_file_path
        self.__data = self.__load_json()

    def __load_json(self) -> dict:
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r") as file:
                return json.load(file)
        return {"business": "", "currency": "ZAR", "transactions": []}

    def get_business_name(self) -> str:
        return self.__data.get("business", "")

    def get_currency(self) -> str:
        return self.__data.get("currency", "ZAR")

    # Native query for Yoco deposits
    def query_yoco_deposits(self) -> list[float]:
        return [
            t["amount"] for t in self.__data.get("transactions", [])
            if t.get("provider") == "Yoco" and t.get("type") == "Deposit"
        ]

    # Native query for expenditures
    def query_expenditures(self) -> list[float]:
        return [
            t["amount"] for t in self.__data.get("transactions", [])
            if t.get("type") == "Expenditure"
        ]

    # Native query for latest balance
    def query_latest_balance(self) -> float:
        txns = self.__data.get("transactions", [])
        return txns[-1]["balance"] if txns else 0.0

    def query_all_transactions(self) -> list[dict]:
        return self.__data.get("transactions", [])