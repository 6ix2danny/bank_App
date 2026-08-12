
class Account:
    def __init__(self, account_id, customer_id, account_type, balance=0):
        self.id = account_id
        self.customer_id = customer_id
        self.account_type = account_type  # "checking" or "savings"
        self.balance = balance

    def add_interest(self):
        """Applies interest based on account type and returns the new
        balance. Savings earns 3%, checking earns 2% - same rule as the
        original Java version's CheckingAccount/SavingsAccount classes."""
        rate = 0.03 if self.account_type == "savings" else 0.02
        self.balance = round(self.balance * (1 + rate), 2)
        return self.balance


class Customer:
    def __init__(self, customer_id, name, username, password):
        self.id = customer_id
        self.name = name
        self.username = username
        self.password = password
