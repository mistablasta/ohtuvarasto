import unittest
from app import app, varastot, id_counter


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        varastot.clear()
        id_counter[0] = 0

    def test_index_empty(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Varastot", response.data)

    def test_create_get(self):
        response = self.client.get("/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Luo uusi varasto", response.data)

    def test_create_post(self):
        response = self.client.post("/create", data={
            "nimi": "Mehuvarasto",
            "tilavuus": "100",
            "alku_saldo": "50"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mehuvarasto", response.data)
        self.assertEqual(len(varastot), 1)

    def test_edit_get(self):
        self.client.post("/create", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Testi", response.data)

    def test_edit_add(self):
        self.client.post("/create", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        self.client.post("/edit/1", data={
            "action": "lisaa",
            "maara": "50"
        })
        self.assertAlmostEqual(varastot[1]["varasto"].saldo, 50)

    def test_edit_take(self):
        self.client.post("/create", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        self.client.post("/edit/1", data={
            "action": "ota",
            "maara": "20"
        })
        self.assertAlmostEqual(varastot[1]["varasto"].saldo, 30)

    def test_delete(self):
        self.client.post("/create", data={
            "nimi": "Testi",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        self.assertEqual(len(varastot), 1)
        response = self.client.post("/delete/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(varastot), 0)

    def test_edit_nonexistent_redirects(self):
        response = self.client.get("/edit/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent(self):
        response = self.client.post("/delete/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
