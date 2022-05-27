# Authentication Service TK LAW B7

Link service: https://law-b7-auth.herokuapp.com/

API Docs: https://app.apiary.io/authservicetklawb7api/

```api/user/``` (GET): Verify token + get user info (token di header)

```api/token/``` (POST): Login user (params: email, password)

```api/token/refresh/``` (POST): Refresh token (params: refresh)

```api/user/register/``` (POST): Register user baru (params: email, user_name, password, first_name, last_name, phone_number)

```api/user/logout/blacklist/``` (POST): Logout user (params: refresh_token)
