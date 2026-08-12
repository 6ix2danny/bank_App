

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app import store


class TestAccountCRUD(unittest.TestCase):

    def setUp(self):
        store.seed()
        self.client = TestClient(app)

    def test_list_accounts_returns_seeded_data(self):
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)  # 2 + 1 + 1 seeded above

    def test_get_single_account(self):
        response = self.client.get("/accounts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["account_type"], "checking")

    def test_get_nonexistent_account_returns_404(self):
        response = self.client.get("/accounts/9999")
        self.assertEqual(response.status_code, 404)

    def test_create_account_for_existing_customer(self):
        payload = {"customer_id": 1, "account_type": "savings", "balance": 300}
        response = self.client.post("/accounts", json=payload)
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["customer_id"], 1)
        self.assertEqual(body["balance"], 300)

    def test_create_account_for_nonexistent_customer_fails(self):
        payload = {"customer_id": 9999, "account_type": "savings", "balance": 100}
        response = self.client.post("/accounts", json=payload)
        self.assertEqual(response.status_code, 404)

    def test_create_account_rejects_invalid_type(self):
        payload = {"customer_id": 1, "account_type": "crypto", "balance": 100}
        response = self.client.post("/accounts", json=payload)
        # Pydantic's pattern validation should reject this before it
        # ever reaches our own code (FastAPI returns 422 for bad input)
        self.assertEqual(response.status_code, 422)

    def test_update_account_balance(self):
        response = self.client.put("/accounts/1", json={"balance": 9999})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["balance"], 9999)

    def test_delete_account(self):
        response = self.client.delete("/accounts/1")
        self.assertEqual(response.status_code, 204)
        follow_up = self.client.get("/accounts/1")
        self.assertEqual(follow_up.status_code, 404)


class TestAccountInterest(unittest.TestCase):

    def setUp(self):
        store.seed()
        self.client = TestClient(app)

    def test_savings_account_gets_3_percent_interest(self):
        # Account 2 is Daniel's savings account, seeded with balance 5000
        response = self.client.post("/accounts/2/add-interest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["balance"], 5150.0)  # 5000 * 1.03

    def test_checking_account_gets_2_percent_interest(self):
        # Account 1 is Daniel's checking account, seeded with balance 1000
        response = self.client.post("/accounts/1/add-interest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["balance"], 1020.0)  # 1000 * 1.02


class TestAccountSearchSortFilter(unittest.TestCase):

    def setUp(self):
        store.seed()
        self.client = TestClient(app)

    def test_filter_by_account_type(self):
        response = self.client.get("/accounts", params={"account_type": "savings"})
        types = {a["account_type"] for a in response.json()}
        self.assertEqual(types, {"savings"})

    def test_filter_by_min_balance(self):
        response = self.client.get("/accounts", params={"min_balance": 1000})
        for acc in response.json():
            self.assertGreaterEqual(acc["balance"], 1000)

    def test_filter_by_max_balance(self):
        response = self.client.get("/accounts", params={"max_balance": 1000})
        for acc in response.json():
            self.assertLessEqual(acc["balance"], 1000)

    def test_filter_by_customer_id(self):
        response = self.client.get("/accounts", params={"customer_id": 1})
        for acc in response.json():
            self.assertEqual(acc["customer_id"], 1)
        self.assertEqual(len(response.json()), 2)  # Daniel has 2 seeded accounts

    def test_sort_by_balance_descending(self):
        response = self.client.get("/accounts", params={"sort_by": "balance", "order": "desc"})
        balances = [a["balance"] for a in response.json()]
        self.assertEqual(balances, sorted(balances, reverse=True))

    def test_combined_filter_and_sort(self):
        response = self.client.get(
            "/accounts",
            params={"account_type": "savings", "sort_by": "balance", "order": "asc"},
        )
        results = response.json()
        balances = [a["balance"] for a in results]
        self.assertEqual(balances, sorted(balances))
        for acc in results:
            self.assertEqual(acc["account_type"], "savings")


if __name__ == "__main__":
    unittest.main()
