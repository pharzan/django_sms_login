# Django password less login (four digit SMS verification code)
### An API based Django dashboard login with no password

This repository is an implementation of an API used to generate a four digit which can be sent to the user via SMS 
for authentication.

The API has four endpoints:
* ```api/login/create```
* ```api/login/verify```
* ```api/login/auth```
* ```api/login/unauth```

## Usage:

### Create a four digit code:

The ```api/login/create``` receives POST request with a phone number and if the number doesn't exist in the users table,
it is inserted. 
A random four digit code is generated and stored in the database.The payload should look like:
```json 
{
   "phone_number":"09123456789"
 } 
```

### Verify the four digit code:

A POST request with the phone number and the verification code should be sent to the ```api/login/verify``` endpoint to receive
an authorization token. The payload for this endpoint looks something like:
```json
{
    "verification_code":"1081",
    "phone_number":"09123456789"
}
````
And the response includes the token:
```json
{
    "status": 200,
    "verified": true,
    "token": "1651b34546b9d9e95394b5f07dd2ef8a2e66f671dee7d7e956067a1148bcc8c2"
}
```
### Login
By navigating to the ```api/login/auth``` (making a GET request) with the token in the header the user can be logged in 
as the newly created user.
For the above example the header sholud include the token as so:
``` TOKEN:1651b34546b9d9e95394b5f07dd2ef8a2e66f671dee7d7e956067a1148bcc8c2 ``` 

### Logout
Logging out is done by navigating to the ```api/login/unauth``` endpoint.


