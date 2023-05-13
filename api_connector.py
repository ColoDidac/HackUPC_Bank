import json
import furl
import requests
from datetime import datetime, timezone

from exceptions import UnauthorizedError, NotFoundError, InternalServerError
from domain import Transaction


class Client:
    BASE_URL = 'https://int.strandscloud.com/fs-api/'

    def __init__(self, api_key, user):
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-api-key': api_key,
            'Authorization': 'Bearer ' + user})
        self.url = furl.furl(self.BASE_URL)

    API_OK = 200
    API_ERRORS_MAPPING = {
        403: UnauthorizedError,
        401: UnauthorizedError,
        400: NotFoundError,
        500: InternalServerError,
    }

    def request(self, endpoint):
        response = self.session.get(self.BASE_URL + endpoint)
        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, Exception)
            raise exception
        return json.loads(response.text)

    def transactions(self):
        endpoint = 'transactions'
        data = self.client.request(endpoint)
        return [Transaction(t) for t in data['transactions']]

    def transaction(self, id):
        endpoint = f'transactions/{id}'
        return Transaction(self.client.request(endpoint))


class BankUser(Client):
    def __init__(self, api_key, user):
        self.client = Client(api_key, user)
        self.transactions = []
        self.current_amount = 0
        self.debt = 0
        self.upcoming_transactions = []

    def process_transaction(self, transaction):
        transaction = Transaction(transaction)
        self.current_amount += transaction.amount.amount
        return transaction

    def process_upcoming_transaction(self, transaction):
        transaction = Transaction(transaction)
        given_date = datetime.strptime(transaction.due_date, '%Y-%m-%dT%H:%M%z')
        today_date = datetime.now(timezone.utc)
        self.debt += (transaction.amount.amount if
                      given_date > today_date else self.debt)
        return transaction

    def get_transactions(self):
        endpoint = 'transactions'
        data = self.client.request(endpoint)
        self.transactions = [
                self.process_transaction(t) for t in data['transactions']]
        return self.transactions

    def get_transaction(self, id):
        # Todo: If transactions is already filled search in transactions first
        endpoint = f'transactions/{id}'
        return Transaction(self.client.request(endpoint))

    def get_upcoming_transactions(self):
        endpoint = 'upcoming-transactions'
        data = self.client.request(endpoint)
        self.upcoming_transactions = [
                self.process_upcoming_transaction(t) for t in data[
                    'upcomingTransactions']]
        return self.upcoming_transactions

    def calculate_alert(self):
        raise NotImplementedError

    def calculate_avg(self):
        current_month = datetime.now().month
        month_amount = 0
        ##########
        # MODE 1 #
        #########
        for transaction in self.transactions:
            if int(transaction.date[5:7]
                   ) == current_month and transaction.amount.amount < 0:
                month_amount += transaction.amount.amount
        return month_amount / datetime.now().day

        #################################
        #   MODE 2                     #
        #   DESDE DE QUE ES COBRA (CAT:80-81)    #
        ##############################
        """
        data_inicio_periodo=""
        for transaction in self.transactions:
            if transaction["category"] == 81:
                data_inicio_periodo=transaction["date"]
        """
