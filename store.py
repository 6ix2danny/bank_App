

from app.entities import Customer, Account

customers = {}
accounts = {}

_customer_id_counter = 1
_account_id_counter = 1


def _next_customer_id():
    global _customer_id_counter
    cid = _customer_id_counter
    _customer_id_counter += 1
    return cid


def _next_account_id():
    global _account_id_counter
    aid = _account_id_counter
    _account_id_counter += 1
    return aid


def seed():
    """Resets and populates starting data - same Daniel/Dan/Danny theme
    as the Java version, so there's something to query immediately."""
    global customers, accounts, _customer_id_counter, _account_id_counter
    customers = {}
    accounts = {}
    _customer_id_counter = 1
    _account_id_counter = 1

    daniel = create_customer("Daniel", "daniel", "daniel123")
    dan = create_customer("Dan", "dan", "dan123")
    danny = create_customer("Danny", "danny", "danny123")

    create_account(daniel.id, "checking", 1000)
    create_account(daniel.id, "savings", 5000)
    create_account(dan.id, "checking", 250)
    create_account(danny.id, "savings", 12000)


def create_customer(name, username, password):
    customer = Customer(_next_customer_id(), name, username, password)
    customers[customer.id] = customer
    return customer


def get_customer(customer_id):
    return customers.get(customer_id)


def get_all_customers():
    return list(customers.values())


def update_customer(customer_id, name=None, username=None, password=None):
    customer = customers.get(customer_id)
    if customer is None:
        return None
    if name is not None:
        customer.name = name
    if username is not None:
        customer.username = username
    if password is not None:
        customer.password = password
    return customer


def delete_customer(customer_id):
    if customer_id not in customers:
        return False
    del customers[customer_id]
    # Cascade delete: remove accounts that belonged to this customer so
    # we don't leave orphaned accounts pointing at a deleted customer.
    orphaned_ids = [aid for aid, acc in accounts.items() if acc.customer_id == customer_id]
    for aid in orphaned_ids:
        del accounts[aid]
    return True


def create_account(customer_id, account_type, balance=0):
    account = Account(_next_account_id(), customer_id, account_type, balance)
    accounts[account.id] = account
    return account


def get_account(account_id):
    return accounts.get(account_id)


def get_all_accounts():
    return list(accounts.values())


def get_accounts_for_customer(customer_id):
    return [a for a in accounts.values() if a.customer_id == customer_id]


def update_account(account_id, account_type=None, balance=None):
    account = accounts.get(account_id)
    if account is None:
        return None
    if account_type is not None:
        account.account_type = account_type
    if balance is not None:
        account.balance = balance
    return account


def delete_account(account_id):
    if account_id not in accounts:
        return False
    del accounts[account_id]
    return True
