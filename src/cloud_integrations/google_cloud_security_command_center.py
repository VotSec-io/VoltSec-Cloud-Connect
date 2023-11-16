import logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class GoogleCloudSecurityCommandCenter:

    def __init__(self, project_id):
        self.logger = logging.getLogger(__name__)
        credentials, project = Credentials.from_service_account_file('service_account.json').with_project(project_id)
        self.service = build('securitycommandcenter', 'v1', credentials=credentials)

    def get_findings(self):
        try:
            response = self.service.projects().securityCenter().findings().list().execute()
            return response.get('findings', [])
        except Exception as e:
            self.logger.error(e)
            return []

    def get_finding_details(self, finding_name):
        try:
            response = self.service.projects().securityCenter().findings().get(name=finding_name).execute()
            return response
        except Exception as e:
            self.logger.error(e)
            return None

if __name__ == '__main__':
    # Replace with your Google Cloud project ID
    project_id = 'YOUR_PROJECT_ID'

    # Create an instance of the GoogleCloudSecurityCommandCenter class
    gcsc_client = GoogleCloudSecurityCommandCenter(project_id)

    # Get a list of security findings
    findings = gcsc_client.get_findings()

    # Get details for a specific finding
    finding_name = findings[0]['name']
    finding_details = gcsc_client.get_finding_details(finding_name)

    print(findings)
    print(finding_details)
