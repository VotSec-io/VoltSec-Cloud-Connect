import os
import json
import logging
from cryptography.fernet import Fernet

class CredentialsManager:

    def __init__(self, credentials_file_path):
        self.logger = logging.getLogger(__name__)
        self.credentials_file_path = credentials_file_path
        self.fernet = Fernet(os.environ.get('CREDENTIALS_ENCRYPTION_KEY'))

    def store_credentials(self, credentials):
        try:
            encrypted_credentials = self.fernet.encrypt(json.dumps(credentials).encode('utf-8'))
            with open(self.credentials_file_path, 'wb') as credentials_file:
                credentials_file.write(encrypted_credentials)
            self.logger.info('Credentials stored successfully.')
        except Exception as e:
            self.logger.error('Failed to store credentials:', e)

    def retrieve_credentials(self):
        try:
            with open(self.credentials_file_path, 'rb') as credentials_file:
                encrypted_credentials = credentials_file.read()
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
    credentials = {
        'aws_account_id': 'YOUR_AWS_ACCOUNT_ID',
        'aws_access_key_id': 'YOUR_AWS_ACCESS_KEY_ID',
        'aws_secret_access_key': 'YOUR_AWS_SECRET_ACCESS_KEY'
    }
    credentials_manager.store_credentials(credentials)

    # Example usage: Retrieve credentials
    retrieved_credentials = credentials_manager.retrieve_credentials()
    print('Retrieved credentials:', retrieved_credentials)
