CUSTOMERS = {
    "cus_1001": {
        "customer_id": "cus_1001",
        "name": "Alex Rivera",
        "email": "alex.rivera@example.com",
        "plan": "Business",
        "account_status": "active",
        "mrr": 249,
        "open_invoices": 1,
    },
    "cus_1002": {
        "customer_id": "cus_1002",
        "name": "Maya Chen",
        "email": "maya.chen@example.com",
        "plan": "Enterprise",
        "account_status": "under_review",
        "mrr": 2100,
        "open_invoices": 0,
    },
}


class AccountService:
    def get_account(self, customer_id: str) -> dict:
        return CUSTOMERS.get(
            customer_id,
            {
                "customer_id": customer_id,
                "name": "Unknown Customer",
                "email": "unknown@example.com",
                "plan": "Unknown",
                "account_status": "unknown",
                "mrr": 0,
                "open_invoices": 0,
            },
        )
