import json
from pymongo import MongoClient

class ChatContext:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.messages_col = self.db["messages"]

    def get_user_history(self, user_id):
        history = list(self.messages_col.find({"user_id": user_id}, {"_id": 0, "role": 1, "message": 1}))
        return history

    def build_context(self, user_id):
        history = self.get_user_history(user_id)
        context = ""
        for msg in history[-5:]:  # Last 5 messages
            prefix = "Kullanıcı:" if msg["role"] == "user" else "Bot:"
            context += f"{prefix} {msg['message']}\n"
        # Ek: önemli olaylar
        from mock_apis import getBillingInfo, getUserInfo
        try:
            billing = getBillingInfo(user_id, "current")
            unpaid = 0
            last_due = "-"
            if billing.get("success"):
                unpaid = billing["data"].get("unpaid_amount", 0)
                bills = billing["data"].get("bills", [])
                if bills:
                    last_due = bills[-1]["month"]
            customer = getUserInfo(user_id)
            contract_end = customer["data"].get("contract_end_date", "-") if customer.get("success") else "-"
        except Exception:
            unpaid = 0
            last_due = "-"
            contract_end = "-"
        context += f"Önemli Bilgiler: Son Fatura Dönemi: {last_due}, Toplam Ödenmemiş: {unpaid} TL, Sözleşme Bitiş: {contract_end}\n"
        return context.strip()  # Remove trailing newline

    def save_message(self, user_id, role, message):
        self.messages_col.insert_one({"user_id": user_id, "role": role, "message": message})
