import logging
import os
from subprocess import Popen

class RemediationEngine:

    def __init__(self, remediation_scripts_path):
        self.logger = logging.getLogger(__name__)
        self.remediation_scripts_path = remediation_scripts_path

    def remediate_incident(self, incident):
        try:
            # Retrieve the remediation script path based on user input or incident type and severity
            if self.remediation_scripts_path:
                remediation_script_path = self.remediation_scripts_path
            else:
                script_path = input("Enter the path to the remediation script: ")
                remediation_script_path = os.path.join(script_path, f"{incident.type}-{incident.severity}.sh")

            # Execute the remediation script if it exists
            if os.path.isfile(remediation_script_path):
                Popen(["sh", remediation_script_path])
                self.logger.info('Remediation script executed successfully.')
            else:
                self.logger.info('No remediation script found at the specified path.')
        except Exception as e:
            self.logger.error('Failed to remediate incident:', e)

if __name__ == '__main__':
    # Allow user to input the remediation scripts path
    remediation_scripts_path = input("Enter the path to the remediation scripts directory (optional): ")

    # Create an instance of the RemediationEngine class
    remediation_engine = RemediationEngine(remediation_scripts_path)

    # Create a mock incident object
    incident = Incident('ID-12345', 'High', 'Malware infection')

    # Remediate the mock incident
    remediation_engine.remediate_incident(incident)
