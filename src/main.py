import logging
from flask import Flask, request
from user_api_manager import UserAPIManager
from access_control import AccessControlManager
from user_authentication import UserAuthenticationManager

# Create application instance
app = Flask(__name__)

# Create repositories and managers
user_repository = UserRepository()
user_role_repository = UserRoleRepository()
permission_repository = PermissionRepository()
access_control_manager = AccessControlManager(user_role_repository, permission_repository)
user_authentication_manager = UserAuthenticationManager(user_repository)

# Create API manager and start the user API server
user_api_manager = UserAPIManager(user_repository)
user_api_manager.run()

if __name__ == '__main__':
    # Configure application logging
    logging.basicConfig(level=logging.INFO)

    # Define a protected route that requires authentication and authorization
    @app.route('/protected_resource', methods=['GET'])
    @access_control_manager.has_permission('user', 'protected_resource', 'read')
    def protected_resource():
        if user_authentication_manager.validate_session_token(request.headers.get('Authorization')):
            return jsonify({'message': 'You are authorized to access this resource.'}), 200
        else:
            return jsonify({'error': 'Invalid or expired session token.'}), 401

    # Run the Flask application in production mode
    app.run(host='0.0.0.0', port=5000, debug=False)
