import firebase_admin
from firebase_admin import credentials, auth

class FirebaseUserManager:
    def __init__(self, service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)

    def create_user(self, email, password, display_name=None):
        # Create a new user account with the specified email and password
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return user.uid

    def get_user_by_uid(self, uid):
        # Get a user by their user ID
        user = auth.get_user(uid)
        return user

    def get_user_by_email(self, email):
        # Get a user by their email address
        user = auth.get_user_by_email(email)
        return user

    def update_user(self, uid, display_name=None, password=None):
        # Update a user's profile or password
        user = auth.update_user(
            uid=uid,
            display_name=display_name,
            password=password
        )
        return user.uid

    def delete_user(self, uid):
        # Delete a user account by their user ID
        auth.delete_user(uid)

    def list_users(self, max_results=1000):
        # List up to `max_results` users inthe Firebase project
        page = auth.list_users(max_results=max_results)
        users = []
        while page:
            for user in page.users:
                users.append(user)
            page = page.get_next_page()
        return users