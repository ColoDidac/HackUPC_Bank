import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


class BankUser:
    def __init__(self, num_client):
        load_dotenv()
        self.client_id = num_client
        self.token = os.getenv(f'USER{num_client}_TOKEN')
        self.transactions = []
        self.current_amount = 0
        self.debt = 0
        self.upcoming_transactions = []

    def get_transactions(self):
        url = "https://int.strandscloud.com/fs-api/transactions?recoverHeatLevel=false&page=0&size=50&sort=DATE_DESC&applyToSplits=false"
        headers = {
            "accept": "application/json",
            "x-api-key": "5brZ6as5Qj3AhS2rzeedm8VGxUBTlMSD8YQsyxz3",
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhMQVRvOWM2T3VQci1jWEdqMEc3UiJ9.eyJpc3MiOiJodHRwczovL3N0cmFuZHMtZGVtby1iYW5rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHx1c2VyUEZNMTYiLCJhdWQiOiJodHRwOi8vc2FuZGJveC5zdHJhbmRzY2xvdWQuY29tLyIsImlhdCI6MTY4Mzc5Njc5NiwiZXhwIjoxNjg0MjI4Nzk2LCJhenAiOiJtRG5YajB0TDNZWEVOVldtQ2NOQ2xKUG5lV2loenlIbCIsImd0eSI6InBhc3N3b3JkIn0.IDlxIHJiYsXHsMWdqasdXSTtVm7MjvbJiitVzyGFuTU6arsorLzK8giJnUXhaPHCo1SlXeHlKzb58cLnSJlaohvXaBFjECZ9sSMxfRYMM16SNW8oq51ZUyhUJogrgzvY5AdQhQ6YBKF_nXJrRGOqICzePl1Dq3zUeeFZbZ4nJzgJi_sy2mXNFdtZZU-2U0T6T59ba8GmTz2u3itseIhzRI8R8WdwQaCN-HG8bl5lH2nUsfRIcpJskgIOHIizPCCJu4_K-06nFItbYQy8hvsB6ml5_BlkUb1hcfczn2b05yM6n9xFLOOrRLk3NZ_u9FZBGsxXZvmveG_vZnx0F1BuXg"
        }
        response = requests.get(url, headers=headers)
        for element in response.json()["transactions"]:
            self.current_amount += element["amount"]["amount"]
            self.transactions.append({"id": element["id"],
                                      "amount": element["amount"]})
        print(self.client_id)
        print(self.transactions)
        print(self.current_amount)

    def get_upcoming_transactions(self):
        url = "https://int.strandscloud.com/fs-api/upcoming-transactions?recoverHeatLevel=false&page=0&size=50&sort=DUE_DATE_DESC"
        headers = {
            "accept": "application/json",
            "x-api-key": "5brZ6as5Qj3AhS2rzeedm8VGxUBTlMSD8YQsyxz3",
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhMQVRvOWM2T3VQci1jWEdqMEc3UiJ9.eyJpc3MiOiJodHRwczovL3N0cmFuZHMtZGVtby1iYW5rLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHx1c2VyUEZNMTkiLCJhdWQiOiJodHRwOi8vc2FuZGJveC5zdHJhbmRzY2xvdWQuY29tLyIsImlhdCI6MTY4Mzc5Njc5NywiZXhwIjoxNjg0MjI4Nzk3LCJhenAiOiJtRG5YajB0TDNZWEVOVldtQ2NOQ2xKUG5lV2loenlIbCIsImd0eSI6InBhc3N3b3JkIn0.h4rWdi3Smy3cHLLD0pjWsIfXloiUaLwqxX93NrE2XUqcK5Q4N4uwliQHvn6Mus8GIjWeGhSPAevELFZPbniTcfjxmcKHk_Mg7bCW3nKa5CEuVgUPjjSCOpBezWTm0--QiSjz5TZerGn6sl7UbgUxwwR719CkjDkklslRnT1O5squSI8A4z032n1cisrFOSMCdpXzeaGWCdidePtFS1VY4sy9T6Fh9PzNsi0ubwWvfrsu20eRB_6JGxEl5BRTZ8Xer5P3ifwRJRR19iEB3kPiZrNQ7IzXZHY9TjV3Q4SZ-mQrlBGtc5D8FdTiJr_qkWv3zjgCz-U3VanCk6DJK4RZaA"
        }
        response = requests.get(url, headers=headers)
        for transaction in response.json()["upcomingTransactions"]:
            self.upcoming_transactions.append({
                "transaction": transaction["name"],
                "amount": transaction["amount"],
                "dueDate": transaction["dueDate"]
            })
            given_date = datetime.strptime(transaction["dueDate"], '%Y-%m-%dT%H:%M%z')
            today_date = datetime.now(timezone.utc)
            self.debt += transaction["amount"]["amount"] if given_date > today_date else self.debt
        print(self.upcoming_transactions)
        print(self.debt)

    # def calculate_alert(self):


if __name__ == '__main__':
    for client in range(5):
        client_bank = BankUser(client)
        client_bank.get_transactions()
        #client_bank.get_upcoming_transactions()
        # client_bank.calculate_alert()
