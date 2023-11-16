import os
import json
import logging
from cryptography.fernet import Fernet
from getpass import getpass

class CredentialsManager:

    def __init__(self, credentials_file_path):
        self.logger = logging.getLogger(__name__)
        self.credentials_file_path = credentials_file_path
        self.fernet = Fernet(os.environ.get('CREDENTIALS_ENCRYPTION_KEY'))

    def store_credentials(self):
        try:
            # Prompt user for AWS account ID
            aws_account_id = input("Enter your AWS account ID: ")

            # Prompt user for AWS access key ID
            aws_access_key_id = input("Enter your AWS access key ID: ")

            # Prompt user for AWS secret access key
            aws_secret_access_key = getpass("Enter your AWS secret access key: ")

            # Prompt user for Azure subscription ID
            azure_subscription_id = input("Enter your Azure subscription ID: ")

            # Prompt user for Google Cloud project ID
            google_cloud_project_id = input("Enter your Google Cloud project ID: ")

            # Create a dictionary of credentials
            credentials = {
                'aws_account_id': aws_account_id,
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key,
                'azure_subscription_id': azure_subscription_id,
                'google_cloud_project_id': google_cloud_project_id
            }

            # Encrypt and store credentials to the file
            encrypted_credentials = self.fernet.encrypt(json.dumps(credentials).encode('utf-8'))
            with open(self.credentials_file_path, 'wb') as credentials_file:
                credentials_file.write(encrypted_credentials)
            self.logger.info('Credentials stored successfully.')
        except Exception as e:
            self.logger.error('Failed to store credentials:', e)

    def retrieve_credentials(self):
        try:
            # Read encrypted credentials from the file
            with open(self.credentials_file_path, 'rb') as credentials_file:
                encrypted_credentials = credentials_file.read()

            # Decrypt and return credentials
            credentials = json.loads(self.fernet.decrypt(encrypted_credentials).decode('utf-8'))
            self.logger.info('Credentials retrieved successfully.')
            return credentials
        except Exception as e:
            self.logger.error('Failed to retrieve credentials:', e)
            return None

if __name__ == '__main__':
    # Replace with your actual credentials_file_path
    credentials_file_path = 'credentials.json'

    # Create an instance of the CredentialsManager class
    credentials_manager = CredentialsManager(credentials_file_path)

    # Example usage: Store credentials
    credentials_manager.store_credentials()

    # Example usage: Retrieve credentials
    retrieved_credentials = credentials_manager.retrieve_credentials()
    print('Retrieved credentials:', retrieved_credentials)
