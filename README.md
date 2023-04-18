# REST API using FastAPI and JWT tokens

REST API store and manage contacts.

Contacts save in PostgreSQL database and contents from:
* Name
* Surname
* Email
* Phone number
* Birthday
* Additional info

API can do next operations:
* Create new contact
* Get list of all contacts
* Get one contact by ID
* Update existing contact
* Delete contact
* Search contacts by name, surname or email
* Get list of contacts with birthday in nearest 7 days

Authorization and authentication:
* Authentication in application
* Authorization with JWT tokens
* All operations can do only registered users
* User can do operations only with own contacts
* At registration if user with specified email already exist application return error HTTP 409 Conflict;
* Application store hashed passwords in DB
* When user successful registered app return HTTP 201 Created and user's data
* For all POST create operations app return HTTP 201 Created
* At POST operations - user authentication. App receive email and password in request body
* If bad username or password receive error HTTP 401 Unauthorized
* Authorization realized with access_token and refresh_token

