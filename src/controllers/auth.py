from src.services.auth import FirebaseService
from fastapi import APIRouter, HTTPException

firebase_service = FirebaseService('./secretKey.json', '')
auth_router = APIRouter()

@auth_router.post('/create_user')
def create_user(email: str, password: str, display_name: str = None, phone_number: str = None, photo_url: str = None, disabled: bool = False, email_verified: bool = False):
    try:
        uid = firebase_service.create_user(email, password, display_name, phone_number, photo_url, disabled, email_verified)
        return {'uid': uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.put('/update_user')
def update_user(uid: str, update_data: dict):
    try:
        firebase_service.update_user(uid, update_data)
        return {'message': 'User updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.delete('/delete_user')
def delete_user(uid: str):
    try:
        firebase_service.delete_user(uid)
        return {'message': 'User deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get('/get_user')
def get_user(uid: str):
    try:
        user = firebase_service.get_user(uid)
        return {'user': vars(user)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get('/get_user_by_email')
def get_user_by_email(email: str):
    try:
        user = firebase_service.get_user_by_email(email)
        return {'user': vars(user)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get('/get_user_by_phone_number')
def get_user_by_phone_number(phone_number: str):
    try:
        user = firebase_service.get_user_by_phone_number(phone_number)
        return {'user': vars(user)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get('/get_users')
def get_users(max_results):
    try:
        users = firebase_service.list_users(int(max_results))
        users_dict = [vars(user) for user in users]
        return {'users': users_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/set_custom_user_claims')
def set_custom_user_claims(uid: str, custom_claims: dict):
    try:
        firebase_service.set_custom_user_claims(uid, custom_claims)
        return {'message': 'Custom claims setsuccessfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/revoke_refresh_tokens')
def revoke_refresh_tokens(uid: str):
    try:
        firebase_service.revoke_refresh_tokens(uid)
        return {'message': 'Refresh tokens revoked successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/verify_id_token')
def verify_id_token(id_token: str, check_revoked: bool = False):
    try:
        claims = firebase_service.verify_id_token(id_token, check_revoked)
        return {'claims': claims}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/create_custom_token')
def create_custom_token(uid: str, additional_claims: dict = None):
    try:
        custom_token = firebase_service.create_custom_token(uid, additional_claims)
        return {'custom_token': custom_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/send_verification_email')
def send_verification_email(id_token: str):
    try:
        firebase_service.send_verification_email(id_token)
        return {'message': 'Verification email sent successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/send_password_reset_email')
def send_password_reset_email(email: str):
    try:
        firebase_service.send_password_reset_email(email)
        return {'message': 'Password reset email sent successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/sign_in_user')
def sign_in_user(email: str, password: str):
    try:
        tokens = firebase_service.sign_in_user(email, password)
        return {'tokens': tokens}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

