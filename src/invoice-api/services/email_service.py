from dapr.clients import DaprClient
from models import Invoice
import os

class EmailService:

    def __init__(self):
        self.dapr_client = DaprClient()
        self.template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'invoice_email.html')

    def send_email(self, invoice:Invoice):
        metadata = {
            "emailFrom": "noreply@petclinic.ca",
            "emailTo": invoice.owner_email,
            "subject": f"Invoice for {invoice.animal_name}'s appointment"
        }        

        # Read the HTML template
        with open(self.template_path, 'r', encoding='utf-8') as file:
            html_template = file.read()

        # Replace placeholders with actual values
        html_body = html_template.replace('{{owner_name}}', invoice.owner_name)
        html_body = html_body.replace('{{animal_name}}', invoice.animal_name)
        html_body = html_body.replace('{{invoice_id}}', invoice.id)
        html_body = html_body.replace('{{issue_date}}', invoice.issue_date.strftime('%B %d, %Y'))
        html_body = html_body.replace('{{due_date}}', invoice.due_date.strftime('%B %d, %Y'))
        html_body = html_body.replace('{{subtotal}}', f'{invoice.subtotal:.2f}')
        html_body = html_body.replace('{{tax}}', f'{invoice.tax:.2f}')
        html_body = html_body.replace('{{total}}', f'{invoice.total:.2f}')

        self.dapr_client.invoke_binding("sendmail","create",html_body,metadata)