import requests

from requests.auth import HTTPBasicAuth

from python_mbills.base import MBillsBase
from python_mbills import constants
from python_mbills.exceptions import SignatureValidationException


class MBillsAPI(object):
    def __init__(self,
                 api_key,
                 shared_secret,
                 mbills_rsa_pub_key,
                 nonce_length=15,
                 api_endpoint="https://private-90f7d-mbills.apiary-mock.com",
                 currency='EUR'):
        """
        Initialize the MBills API and Base class.
        :param api_key: 
        :param shared_secret: 
        :param mbills_rsa_pub_key: 
        :param nonce_length: (default set to 15)
        :param api_endpoint: (default set to Apiary mock api)
        """
        self.api_endpoint = api_endpoint
        self.currency = currency
        self.base = MBillsBase(api_key, shared_secret, mbills_rsa_pub_key, nonce_length)

    def test_api_parameters_and_signature_verification(self):
        """
        Test if your configuration works correctly. 
        :return: 
        """
        url = "%s%s" % (self.api_endpoint, constants.TEST_ENDPOINT)

        username = self.base.get_username()
        password = self.base.get_password(username=username, request_url=url)

        response = requests.get(url, auth=HTTPBasicAuth(username=username, password=password))

        if not self.base.verify_response(response.json()):
            raise SignatureValidationException('Server signature verification has failed')

        return True

    def test_webhook(self):
        url = "%s%s" % (self.api_endpoint, constants.TEST_WEBHOOK)

        username = self.base.get_username()
        password = self.base.get_password(username=username, request_url=url)

        response = requests.get(url, auth=HTTPBasicAuth(username=username, password=password))

        if not self.base.verify_response(response.json()):
            raise SignatureValidationException('Server signature verification has failed')

        return True

    def create_new_sale(self, amount, purpose, payment_reference=None, order_id=None, channel_id=None, capture=True):
        """
        Create new sale.
        :param amount: 
        :param purpose: 
        :param payment_reference: 
        :param order_id: 
        :param channel_id: 
        :param capture: 
        :return: tuple (transaction_id, payment_token_number, status)
        """
        request_data = {
            "amount": amount,
            "currency": self.currency,
            "purpose": purpose,
            "capture": capture
        }

        if payment_reference:
            request_data['paymentreference'] = payment_reference

        if order_id:
            request_data['orderid'] = order_id

        if channel_id:
            request_data['channelid'] = channel_id

        url = "%s%s" % (self.api_endpoint, constants.NEW_SALE_ENDPOINT)

        username = self.base.get_username()
        password = self.base.get_password(username=username, request_url=url)

        response = requests.post(url, data=request_data, auth=HTTPBasicAuth(username=username, password=password))

        if not self.base.verify_response(response.json()):
            raise SignatureValidationException('Server signature verification has failed')

        response_json = response.json()

        return response_json.get('transactionid'), response_json.get('paymenttokennumber'), response_json.get('status')

    def fetch_transaction_status(self, transaction_id):
        """
        Get the transaction current status. 

        :param transaction_id: 
        :return: 
        """
        url = "%s%s%s/status" % (self.api_endpoint, constants.TRANSACTION_STATUS_ENDPOINT, transaction_id)

        username = self.base.get_username()
        password = self.base.get_password(username=username, request_url=url)

        response = requests.get(url, auth=HTTPBasicAuth(username=username, password=password))

        if not self.base.verify_response(response.json()):
            raise SignatureValidationException('Server signature verification has failed')

        return response.json()
