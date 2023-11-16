import logging
import json
import os
from flask import Flask, request, jsonify

class UserAPIManager:

    def __init__(self, user_repository):
        self.logger = logging.getLogger(__name__)
        self.user_repository = user_repository

        # Create a Flask app instance for handling API requests
        self.app = Flask(__name__)

        # Define routes and request handlers for user management operations
        @self.app.route('/users', methods=['GET'])
        def get_users():
            try:
                users = self.user_repository.get_all_users()
                return jsonify(users), 200
            except Exception as e:
                self.logger.error('Failed to retrieve users:', e)
                return jsonify({'error': 'Failed to retrieve users'}), 500

        @self.app.route('/users/<user_id>', methods=['GET'])
        def get_user_by_id(user_id):
            try:
                user = self.user_repository.get_user_by_id(user_id)
                if user is None:
                    return jsonify({'error': 'User not found'}), 404
                else:
                    return jsonify(user), 200
            except Exception as e:
                self.logger.error(f'Failed to retrieve user {user_id}:', e)
                return jsonify({'error': 'Failed to retrieve user'}), 500

        @self.app.route('/users', methods=['POST'])
        def create_user():
            try:
                user_data = json.loads(request.data)
                new_user = self.user_repository.create_user(user_data)
                return jsonify(new_user), 201
            except Exception as e:
                self.logger.error('Failed to create user:', e)
                return jsonify({'error': 'Failed to create user'}), 500

        @self.app.route('/users/<user_id>', methods=['PUT'])
        def update_user(user_id):
            try:
                user_data = json.loads(request.data)
                updated_user = self.user_repository.update_user(user_id, user_data)
                return jsonify(updated_user), 200
            except Exception as e:
                self.logger.error(f'Failed to update user {user_id}:', e)
                return jsonify({'error': 'Failed to update user'}), 500

        @self.app.route('/users/<user_id>', methods=['DELETE'])
        def delete_user(user_id):
            try:
                self.user_repository.delete_user(user_id)
                return jsonify({'message': 'User deleted successfully'}), 200
            except Exception as e:
                self.logger.error(f'Failed to delete user {user_id}:', e)
                return jsonify({'error': 'Failed to delete user'}), 500

    def run(self):
        # Run the Flask app in production mode
        self.app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    # Replace with actual user repository implementation
    user_repository = UserRepository()

    # Create an instance of the UserAPIManager class
    user_api_manager = UserAPIManager(user_repository)

    # Start the user API server
    user_api_manager.run()
