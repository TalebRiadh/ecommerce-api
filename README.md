## E-COMMERCE API
This is a REST API for an E-commerce service built for fun and learning with Django, DRF, PostgreSQL and Docker. 


## ROUTES TO IMPLEMENT
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/user/signup/``` | _Register new user_| _All users_|
| *POST* | ```/user/login/``` | _login user_| _All users_|
| *GET* | ```/user/``` | _Get user details_| _All users_|
| *POST* | ```/user/send-sms/{phone_number}``` | _Check if submitted phone number is a valid phone number and sent OTP._| _All users_|
| *POST* | ```/user/verify-phone/{otp}``` | _Check if submitted phone number and OTP matches and verify the user._| _All users_|
| *GET* | ```/user/address/``` | _List and Retrieve user addresses_| _All users_|
| *GET* | ```/user/address/{id}/``` | _Retrieve user address_| _All users_|
| *POST* | ```/account-confirm-email/{key}``` | _confirm email with key sent_| _All users_|
| *GET* | ```/resend-email/``` | _send key to an email_| _All users_|
| *GET* | ```/products/``` | _Get all products_|_All users_|
| *GET* | ```/products/{id}/``` | _Get a specific product_|_All users_|
| *PUT* | ```/products/{id}/``` | _update a specific product_|_All users_|
| *PATCH* | ```/products/{id}/``` | _partial update for a specific product_|_All users_|
| *DELETE* | ```/products/{id}/``` | _delete a specific product_|_All users_|
| *GET* | ```/products/categories``` | _Get all product categories_|_All users_|
| *GET* | ```/products/categories/{id}/``` | _Get all product of specific category_|_All users_|

| *GET* | ```/orders/``` | _Get all orders_|_All users_|
| *POST* | ```/orders/``` | _Place an order_|_All users_|
| *GET* | ```/order/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *PUT* | ```/orders/{order_id}/``` | _Update an order_|_All users_|
| *PATCH* | ```/orders/{order_id}/``` | _Partial update an order_|_All users_|
| *DELETE* | ```/orders/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/orders/{id}/order-items/``` | _Get all items in a specific order_|_All users_|
| *POST* | ```/orders/{id}/order-items/``` | _Add items to a specific order_|_All users_|
| *GET* | ```/orders/{id}/order-items/{id}/``` | _Get a specific item in a specific order_|_All users_|
| *PUT* | ```/orders/{id}/order-items/{id}/``` | _Update a specific item in a specific order_|_All users_|
| *PATCH* | ```/orders/{id}/order-items/{id}/``` | _Partial update a specific item in a specific order_|_All users_|
| *DELETE* | ```/orders/{id}/order-items/{id}/``` | _Remove a specific item in a specific order_|_All users_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_|
