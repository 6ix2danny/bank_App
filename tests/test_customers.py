

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app import store


class TestCustomerCRUD(unittest.TestCase):

    def setUp(self):
        store.seed()
        self.client = TestClient(app)

    def test_list_customers_returns_seeded_data(self):
        response = self.client.get("/customers")
        self.assertEqual(response.status_code, 200)
        names = [c["name"] for c in response.json()]
        self.assertIn("Daniel", names)
        self.assertIn("Dan", names)
        self.assertIn("Danny", names)

    def test_get_single_customer(self):
        response = self.client.get("/customers/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Daniel")

    def test_get_nonexistent_customer_returns_404(self):
        response = self.client.get("/customers/9999")
        self.assertEqual(response.status_code, 404)

    def test_create_customer(self):
        payload = {"name": "Sarah", "username": "sarah", "password": "sarah123"}
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["name"], "Sarah")
        self.assertEqual(body["username"], "sarah")
        self.assertNotIn("password", body)

    def test_create_customer_with_duplicate_username_fails(self):
        payload = {"name": "Someone Else", "username": "daniel", "password": "x"}
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 409)

    def test_update_customer_name(self):
        response = self.client.put("/customers/2", json={"name": "Daniel Jr."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Daniel Jr.")

    def test_update_nonexistent_customer_returns_404(self):
        response = self.client.put("/customers/9999", json={"name": "Nobody"})
        self.assertEqual(response.status_code, 404)

    def test_delete_customer(self):
        response = self.client.delete("/customers/3")
        self.assertEqual(response.status_code, 204)

        follow_up = self.client.get("/customers/3")
        self.assertEqual(follow_up.status_code, 404)

    def test_delete_customer_cascades_to_their_accounts(self):
        response = self.client.delete("/customers/1")
        self.assertEqual(response.status_code, 204)

        remaining_accounts = self.client.get("/accounts").json()
        for acc in remaining_accounts:
            self.assertNotEqual(acc["customer_id"], 1)


class TestCustomerSearchSortFilter(unittest.TestCase):

    def setUp(self):
        store.seed()
        self.client = TestClient(app)

    def test_search_by_partial_name_case_insensitive(self):
        response = self.client.get("/customers", params={"search": "dan"})
        names = {c["name"] for c in response.json()}
        self.assertEqual(names, {"Daniel", "Dan", "Danny"})

    def test_search_with_no_matches_returns_empty_list(self):
        response = self.client.get("/customers", params={"search": "zzz_no_match"})
        self.assertEqual(response.json(), [])

    def test_sort_by_name_ascending(self):
        response = self.client.get("/customers", params={"sort_by": "name", "order": "asc"})
        names = [c["name"] for c in response.json()]
        self.assertEqual(names, sorted(names))

    def test_sort_by_name_descending(self):
        response = self.client.get("/customers", params={"sort_by": "name", "order": "desc"})
        names = [c["name"] for c in response.json()]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_filter_by_min_accounts(self):
        response = self.client.get("/customers", params={"min_accounts": 2})
        names = [c["name"] for c in response.json()]
        self.assertEqual(names, ["Daniel"])


if __name__ == "__main__":
    unittest.main()
