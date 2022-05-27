# law-b7-auth

GET ```api/user/``` : Verify token + get user info (token di header)

POST ```api/token/``` : Login user (params: email, password)

POST ```api/token/refresh/```: Refresh token (params: refresh)

POST ```api/user/register/```: Register user baru (params: email, user_name, password, first_name, last_name, phone_number)

POST ```api/user/logout/blacklist/```: Logout user (params: refresh_token)
