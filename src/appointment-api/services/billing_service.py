from dapr.clients import DaprClient
from models import BillingInformation
import json

class BillingService:

    def __init__(self):
        self.dapr_client = DaprClient()

    def send_billing(self,billing_information:BillingInformation):
        self.dapr_client.publish_event(
            pubsub_name="pubsub",
            topic_name="invoice",
            data=billing_information.model_dump_json()
        )