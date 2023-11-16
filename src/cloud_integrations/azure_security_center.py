import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.security import SecurityCenterClient

class AzureSecurityCenter:

    def __init__(self, subscription_id):
        self.logger = logging.getLogger(__name__)
        credential = DefaultAzureCredential()
        self.client = SecurityCenterClient(credential, subscription_id=subscription_id)

    def get_alerts(self):
        try:
            return self.client.alerts.list()
        except Exception as e:
            self.logger.error(e)
            return []

    def get_alert_details(self, alert_id):
        try:
            return self.client.alerts.get(alert_id)
        except Exception as e:
            self.logger.error(e)
            return None

if __name__ == '__main__':
    # Replace with your Azure subscription ID
    subscription_id = 'YOUR_SUBSCRIPTION_ID'

    # Create an instance of the AzureSecurityCenter class
    azure_security_center = AzureSecurityCenter(subscription_id)

    # Get a list of security alerts
    alerts = azure_security_center.get_alerts()

    # Get details for a specific alert
    alert_id = alerts[0]['id']
    alert_details = azure_security_center.get_alert_details(alert_id)

    print(alerts)
    print(alert_details)
