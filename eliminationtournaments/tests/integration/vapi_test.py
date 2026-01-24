from rest_framework.test import APITestCase

from unittest.mock import patch
from tournament_api.vapi import VapiCall
class VapiIntegrationTest(APITestCase):
    def test_report_exception_returns_vapi_start(self):
        try:
            2 + this_should_fail
        except NameError as e:
            vapi = VapiCall()
            vapi.reportException(e)
    


