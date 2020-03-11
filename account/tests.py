import json
from account.models import User
from django.test import TestCase
from django.test import Client


# email , first_name , last_name , password
class SignUp(TestCase):
    def setUp(self):
        User.objects.create(
            first_name = "asdfasdf",
            last_name = "asdfasdf",
            email =  "jakdu123@gmail.com",
            password = "123123123",
        )

    def Signup_success(self):
        client = Client()

        author = {
            "first_name" : "asdfasdf",
            "last_name" : "asdfasdf",
            "email" : "jakdu123@gmail.com" ,
            "password" :"123123123"
        }

        response = client.post('/account/signup' , json.dumps(author) , content_type='application/json')
        self.assertEqual(response.status_code , 200)

    def Signup_duplicated_email(self):
        client = Client()

        author = {
            "first_name" : "asdfasdf",
            "last_name" : "asdfasdf",
            "email" : "jakdu123@gmail.com",
            "password":"123123123"
        }

        response = client.post('/account/signup' , json.dumps(author) , content_type='application/json')
        self.assertEqual(response.status_code ,400)
        self.assertEqual(response.json(),
                         {
                             "message":"INVALID_EMAIL"
                         }
                        )
    def Signup_post_invalid_keys(self):
        client = Client()

        author = {
            "name" : "jakdu",
            "email":"jakdu123@gmail.com",
        }

        response = client.post('/account/signup' ,json.dumps(author) , content_type='application/json')
        self.assertEqual(response.status_code , 400)
        self.assertEqual(response.json() , {
            "message" : "INVALID_KEYS",
            }
        )

class SignIn(TestCase):
    def setUp(self):
        User.objects.create(
            first_name = "asdfasdf",
            last_name = "asdfasdf",
            email =  "jakdu123@gmail.com",
            password = "$2b$12$JVSrJT3pPYPk7lxNvUF0oO/Ju9fjsWIukNbL5UbGjR33JR72mgPei",
        )

    def SignIn_Success(self):
        client = Client()

        author = {
            "email" :"jakdu123@gmail.com",
            "password" :"$2b$12$JVSrJT3pPYPk7lxNvUF0oO/Ju9fjsWIukNbL5UbGjR33JR72mgPei"
        }

        response = client.post('/account/signin' , json.dumps(author) , content_type='application/json')
        self.assertEqual(response.status_code , 200)

    def SignIn_keyerror(self):
        client = Client()

        author = {
            "name" : "1231",
            "password" : "$2b$12$JVSrJT3pPYPk7lxNvUF0oO/Ju9fjsWIukNbL5UbGjR33JR72mgPei"
        }

        response = client.post('/account/signin' , json.dumps(author) , content_type='application/json')
        self.assertEqual(response.status_code , 400)

