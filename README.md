# law-b7-auth

```api/user/``` (GET): Verify token + get user info (token di header)

```api/token/``` (POST): Login user (params: email, password)

```api/token/refresh/``` (POST): Refresh token (params: refresh)

```api/user/register/``` (POST): Register user baru (params: email, user_name, password, first_name, last_name, phone_number)

```api/user/logout/blacklist/``` (POST): Logout user (params: refresh_token)
