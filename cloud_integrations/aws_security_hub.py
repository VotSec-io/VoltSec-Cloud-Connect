import logging
import boto3

class AWSSecurityHub:

    def __init__(self, region_name):
        self.logger = logging.getLogger(__name__)
        self.session = boto3.Session(region_name=region_name)
        self.securityhub_client = self.session.client('securityhub')

    def get_findings(self):
        try:
            response = self.securityhub_client.list_findings()
            return response.get('Findings', [])
        except Exception as e:
            self.logger.error(e)
            return []

    def get_finding_details(self, finding_id):
        try:
            response = self.securityhub_client.get_findings(FindingIds=[finding_id])
            return response.get('Findings')[0]
        except Exception as e:
            self.logger.error(e)
            return None

if __name__ == '__main__':
    # Replace with your AWS account ID and region
    account_id = 'YOUR_ACCOUNT_ID'
    region_name = 'us-east-1'

    # Create an instance of the AWSSecurityHub class
    aws_security_hub = AWSSecurityHub(region_name)

    # Get a list of security findings
    findings = aws_security_hub.get_findings()

    # Get details for a specific finding
    finding_id = findings[0]['Id']
    finding_details = aws_security_hub.get_finding_details(finding_id)

    print(findings)
    print(finding_details)
