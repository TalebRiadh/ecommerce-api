
from ..models import User
from allauth.account.models import EmailAddress
import json
from .test_setup import TestSetUp



class TestViews(TestSetUp):
    def test_register_user(self):
        response=self.client.post(self.register_url,self.user_data,format='json')
        import pdb 
        pdb.set_trace()
        self.assertEqual(response.status_code,201)

    def test_login_user(self):
        self.client.post(self.register_url,self.user_data)
        user=User.objects.filter(email=self.user_data["email"]).first()
        email = EmailAddress.objects.filter(email=self.user_data["email"]).first()
        email.verified = True
        email.save()
        user.save()
        response= self.client.post(self.login_url, json.dumps({"email": self.user_data["email"], "password": self.password}),content_type='application/json')

        self.assertEqual(response.status_code,200)

    