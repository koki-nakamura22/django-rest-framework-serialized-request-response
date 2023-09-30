from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class TestTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.resource_url = '/api/tests'
        
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_get_ok(self):
        response = self.client.get(
            self.resource_url,
            data={
                'id': 1,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ng(self):
        response = self.client.get(
            self.resource_url,
            data={
                'idaaa': 1,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


    def test_post_ok(self):
        response = self.client.post(
            self.resource_url,
            data={
                'name': 'Koki',
                'age': 20,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_ng(self):
        response = self.client.post(
            self.resource_url,
            data={
                'name': 'Koki',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
