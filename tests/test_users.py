import unittest
from flask import json
from app import app
from app.datastructure.ds_methods import DSMethods


class TestUsers(unittest.TestCase):
    """
    This tests the User endpoints
    """
    def setUp(self):
        self.app = app.test_client()
        self.datastructure = DSMethods()


    def tearDown(self):
        self.datastructure.clear_data()
    
    def test_create_user_returns_error_if_request_missing_fields(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "fistName": "eric",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com"
        }))
        self.assertEqual(response.status_code, 400);

    def test_sign_up_with_too_many_fields(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "fistName": "eric",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule",
            "other": "my field"
        }))
        self.assertIn("Too many arguments", str(response.data))
    
    def test_if_user_tries_to_signup_providing_non_json_data(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application", data=json.dumps([]))
        self.assertIn("Your request must be in json format", str(response.data))

    def test_if_user_tries_to_signup_with_field_typos(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "fistname": "eric",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        self.assertIn("firstName, lastName, email or password is missing", str(response.data))

    def test_if_user_tries_to_signup_providing_improper_data(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "e",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        self.assertEqual(response.status_code, 417);
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eric",
            "lastName": "Mashauri",
            "email": "eubulegmail.com",
            "password": "eubule"
        }))
        self.assertIn("Email must be of format john123@gmail.com", str(response.data));
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eric",
            "lastName": 1,
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        self.assertIn("Name should be a string of characters", str(response.data));
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eri/",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        self.assertIn("Name must not contain a special character", str(response.data));
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eric",
            "lastName": "",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        self.assertIn("Name cannot be empty", str(response.data));
    
    def test_if_user_tries_to_signup_with_invalid_password(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eric",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "e"
        }))
        self.assertIn("Password must be at least 3 characters long", str(response.data))
    
    def test_if_user_can_successfuly_signup(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eric",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        self.assertEqual(response.status_code, 201)

    def test_if_user_tries_to_login_when_they_have_no_account(self):
        response = self.app.post("/api/v1/auth/login", content_type="application/json", data=json.dumps({
            "email": "eric@gmail.com",
            "password": "malaba"
        }))
        self.assertIn("User with email eric@gmail.com does not exist", str(response.data))
    
    def test_if_user_tries_to_login_with_password_incorrect(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "eric",
            "lastName": "Mashauri",
            "email": "eubule@gmail.com",
            "password": "eubule"
        }))
        response = self.app.post("/api/v1/auth/login", content_type="application/json", data=json.dumps({
            "email": "eubule@gmail.com",
            "password": "malaba"
        }))
        self.assertIn("Your password is incorrect. Please try again", str(response.data))
    
    def test_if_user_tries_to_login_with_improper_data(self):
        response = self.app.post("/api/v1/auth/login", content_type="application/json", data=json.dumps({
            "email": "eubule@gmail.com",
            "passwort": "eubule"
        }))
        self.assertEqual(response.status_code, 400)
        response = self.app.post("/api/v1/auth/login", content_type="application/json", data=json.dumps({
            "email": "eubule@gmail.com"
        }))
        self.assertEqual(response.status_code, 400)
        response = self.app.post("/api/v1/auth/login", content_type="application/json", data=json.dumps({
            "email": "eubule@gmail.com",
            "passwort": "eubule",
            "other": "something"
        }))
        self.assertEqual(response.status_code, 414)
        response = self.app.post("/api/v1/auth/login", content_type="application", data=json.dumps([]))
        self.assertIn("Your request must be in json format", str(response.data))
    
    def test_if_user_can_successfuly_login(self):
        response = self.app.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({
            "firstName": "mala",
            "lastName": "Mashauri",
            "email": "malaba@gmail.com",
            "password": "malaba"
        }))
        response = self.app.post("/api/v1/auth/login", content_type="application/json", data=json.dumps({
            "email": "malaba@gmail.com",
            "password": "malaba"
        }))
        self.assertEqual(response.status_code, 200)        
