from enum import Enum, auto
from datetime import datetime, timezone
from typing import List, Dict, Any
from Transactions import Transaction

class LoanOffer:
    class Decision(Enum):
        OFFERED = auto()
        DECLINED = auto()

    def __init__(self, bank_name: str, decision: Decision, amount: float, interest_rate: float):
        self._bank_name = bank_name
        self._decision = decision
        self._amount = amount
        self._interest_rate = interest_rate
        self._received_at = datetime.now(timezone.utc)

    @property
    def bank_name(self) -> str: return self._bank_name
    @property
    def decision(self) -> Decision: return self._decision
    @property
    def amount(self) -> float: return self._amount
    @property
    def interest_rate(self) -> float: return self._interest_rate
    @property
    def received_at(self) -> datetime: return self._received_at


class Communications:
    class ConnectionStatus(Enum):
        DISCONNECTED = auto()
        CONNECTED = auto()
        ERROR = auto()

    def __init__(self, business_id: str, BAP: str, ACR : str, MVT: float):
        self._bank_api_endpoint = BAP
        self._api_credentials_ref = ACR
        self._pending_offers: List[LoanOffer] = []
        self._connection_status = self.ConnectionStatus.DISCONNECTED
        self._business_id = business_id
        self._MVT = MVT

    def send_projection_to_bank(self, txn: Transaction, stats: Dict[str, float]) -> bool:
        self._business_id = txn.get_business_name()
        total_txns = len(txn.query_all_transactions())
        latest_balance = txn.query_latest_balance()
        cfv = stats.get("cfv", 0.0)

        print(f"\n{'='*50}")
        print(f"📊 STATISTICAL ANALYSIS: {self._business_id.upper()}")
        print(f"{'='*50}")
        print(f" Weighted SDE:         R {stats.get('sde_weighted', 0):,.2f}")
        print(f" Compounding Factor:   {stats.get('compounding_factor', 0):.4f}")
        print(f" Risk Multiplier:      {stats.get('multiplier', 0):.2f}x")
        print(f"--------------------------------------------------")
        print(f" CALCULATED FUTURE VALUE (CFV): R {cfv:,.2f}")
        print(f"{'='*50}\n")
        
        if cfv < self._MVT:
            print(f"[LOG] Valuation of R{cfv:,.2f} is below the R{self._MVT:,.2f} threshold. Abort.")
            return False

        application_payload = {
            "business_description": self._business_id,
            "financial_health": {
                "latest_balance": latest_balance,
                "transaction_count": total_txns,
                "currency": txn.get_currency()
            },
            "statistical_analysis": stats
        }

        print(f"[LOG] Simulating API call to: {self._bank_api_endpoint}")
        print(f"[LOG] Publishing full application payload for evaluation...")
        
        self._connection_status = self.ConnectionStatus.CONNECTED
        return True

    def poll_for_bank_response(self, cfv: float) -> List[LoanOffer]:
        print("[LOG] Simulating polling for bank responses...")
        
        calculated_loan_amount = round(cfv * 0.01, 2)
        
        dynamic_offer = LoanOffer(
            bank_name = "ABSA FinTech API",
            decision = LoanOffer.Decision.OFFERED,
            amount = calculated_loan_amount,
            interest_rate = 0.11
        )
        
        self.receive_loan_offer(dynamic_offer)
        return self._pending_offers

    def receive_loan_offer(self, offer: LoanOffer) -> None:
        self._pending_offers.append(offer)
        self.notify_owner(f"New loan offer received from {offer.bank_name}")

    def notify_owner(self, message: str) -> None:
        print(f"[PUSH NOTIFICATION to {self._business_id}]: {message}")

    @property
    def business_id(self) -> str: return self._business_id
    @property
    def connection_status(self) -> ConnectionStatus: return self._connection_status
    @property
    def pending_offers(self) -> List[LoanOffer]: return self._pending_offers