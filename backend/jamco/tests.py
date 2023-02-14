from django.test import RequestFactory
from jamco.views import index

from django.test import TestCase


class FooTest(TestCase):

    def test_index_view(self):
        # Create an instance of the request factory
        request_factory = RequestFactory()
        request = request_factory.get(index)

        # Use the request in the view
        response = index(request)

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)
