import firebase_admin
from firebase_admin import auth, credentials
import requests

class FirebaseService:
    """
    A class that provides methods for interacting with Firebase Authentication API.
    """

    def __init__(self, service_account_key_path, api_key):
        """
        Initializes a new instance of the FirebaseUserActions class.

        :param service_account_key_path: The path to the Firebase service account key file.
        :param api_key: The Firebase API key.
        """
        cred = credentials.Certificate(service_account_key_path)
        firebase_admin.initialize_app(cred)
        self.api_key = api_key

    def create_user(self, email, password, display_name=None, phone_number=None, photo_url=None, disabled=None, email_verified=None):
        """
        Creates a new user account with the specified email and password.

        :param email: The email address of the user to create.
        :param password: The password for the new user account.
        :param display_name: The display name for the new user account.
        :param phone_number: The phone number for the new user account.
        :param photo_url: The photo URL for the new user account.
        :param disabled: Whether the new user account is disabled.
        :param email_verified: Whether the new user account's email address has been verified.
        :return: The UID of the newly created user.
        """
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
            phone_number=phone_number,
            photo_url=photo_url,
            disabled=disabled,
            email_verified=email_verified
        )
        return user.uid

    def update_user(self, uid, data):
        """
        Updates the specified user account with the specified data.

        :param uid: The UID of the user to update.
        :param data: A dictionary containing the data to update.
        """
        auth.update_user(uid, **data)

    def delete_user(self, uid):
        """
        Deletes the specified user account.

        :param uid: The UID of the user to delete.
        """
        auth.delete_user(uid)

    def get_user(self, uid):
        """
        Retrieves the user account with the specified UID.

        :param uid: The UID of the user to retrieve.
        :return: A UserRecord object representing the retrieved user account.
        """
        return auth.get_user(uid)

    def get_user_by_email(self, email):
        """
        Retrieves the user account with the specified email address.

        :param email: The email address of the user to retrieve.
        :return: A UserRecord object representing the retrieved user account.
        """
        return auth.get_user_by_email(email)

    def get_user_by_phone_number(self, phone_number):
        """
        Retrieves the user account with the specified phone number.

        :param phone_number: The phone number of the user to retrieve.
        :return: A UserRecord object representing the retrieved user account.
        """
        return auth.get_user_by_phone_number(phone_number)

    def list_users(self, max_results):
        """
        Retrieves a list of all user accounts.

        :param max_results: The maximum number of results to return.
        :return: A list of UserRecord objects representing the retrieved user accounts.
        """
        return [user for user in auth.list_users(max_results=max_results).iterate_all()]

    def set_custom_user_claims(self, uid, custom_claims):
        """
        Sets custom claims for the specified user account.

        :param uid: The UID of the user to set custom claims for.
        :param custom_claims: A dictionary containing the custom claims to set.
        """
        auth.set_custom_user_claims(uid, custom_claims)

    def revoke_refresh_tokens(self, uid):
        """
        Revokes all refresh tokens for the specified user account.

        :param uid: The UID of the user to revoke refresh tokens for.
        """
        auth.revoke_refresh_tokens(uid)

    def verify_id_token(self, id_token, check_revoked=False):
        """
        Verifies the specified ID token.

        :param id_token: The ID token to verify.
        :param check_revoked: Whether to check if the token has been revoked.
        :return: A dictionary containing the decoded token claims.
        """
        return auth.verify_id_token(id_token, check_revoked=check_revoked)

    def create_custom_token(self, uid, additional_claims=None):
        """
        Creates a custom token for the specified user account.

        :param uid: The UID of the user to create a custom token for.
        :param additional_claims: A dictionary containing additional claims to include in the custom token.
        :return: The custom token.
        """
        return auth.create_custom_token(uid, additional_claims=additional_claims)

    def send_verification_email(self, id_token):
        """
        Sends a verification email to the user with the specified ID token.

        :param id_token: The ID token of the user to send the verification email to.
        """
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={self.api_key}"
        data = {
            "requestType": "VERIFY_EMAIL",
            "idToken": id_token,
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Log the error or return an error message to the user
            raise e

    def send_password_reset_email(self, email):
        """
        Sends a password reset email to the user with the specified email address.

        :param email: The email address of the user to send the password reset email to.
        """
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={self.api_key}"
        data = {
            "requestType": "PASSWORD_RESET",
            "email": email,
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Log the error or return an error message to the user
            raise e

    def sign_in_user(self, email, password):
        """
        Signs in the user with the specified email and password.

        :param email: The email address of the user to sign in.
        :param password: The password of the user to sign in.
        :return: A dictionary containing the user's ID token and refresh token.
        """
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error or return an error message to the user
            raise e
