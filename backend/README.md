# Snapgram Backend

This is the backend of the Snapgram social media application, built with FastAPI. It handles user authentication, data processing, and API requests.

## Project Structure

```
backend/
├── app/
│ ├── api/        # Api routes and authentication
│ ├── core/       # Config file to load environemnt variables from .env
│ ├── models/     # Classes and database integration
│ ├── utils/      # Authentication and mail sender functions
│ └── tests/      # Api endpoints testes
├── .env         
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB

### Installation

1. Navigate to the backend directory
  
  ```bash
  cd backend
  ```
  
2. Create a virtual environment:
  
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```
  
3. Install the required dependencies:
  
  ```bash
  pip install -r requirements.txt
  ```
  
4. Set up the environment variables:
  
  ```bash
  vim .env
  
  # example of '.env' file
  
  MONGODB_URL=mongodb://localhost:27017
  HOST=127.0.0.1
  PORT=8000
  DB_NAME=you_db_name
  
  JWT_SECRET_KEY=YOUR_SECRET_KEY__IT_MUST_BE_UPDATED
  JWT_REFRESH_SECRET_KEY=YOU_REFRESH_SECRET_KEY__IT_MUST_BE_UPDATED
  
  MAIL_SERVER="smtp.gmail.com" # if you want to send email from gmail
  MAIL_USERNAME="your_email@gmail.com"
  MAIL_APP_PASSWORD="******" # if gmail is used you must use app password instead of your password
  MAIL_FROM="from_ you"
  ```
  
5. Run the application:
  
  ```bash
  uvicorn app.api.app:app
  ```
  

### API Documentation:

after running the uvicorn server (after the previous step) you can **view** and **test** the api endpoints, you can also view the **requests** and **responses** schemas with examples using [FastAPI - Swagger UI](http://127.0.0.1:8000/docs)

### Testing

Run the tests using pytest:

```bash
pytest
```

### API Endpoints

#### Authentication

- `/auth/register`: Registering a new user
  
- `/auth/login`: Login the user to the application
  
- `/auth/me`: get the current authenticated user
  
- `/auth/logout`: Logging out the user
  
- `/auth/forgot-password`: send an email to the user with a url to reset his password
  
- `/auth/reset-password/{token}`: updating the user password
  
- `/auth/refresh-token`: Refreshing the user access token using the refresh token
  

#### Users

- `/users/{user_id}`: Get, Deleter, Update a user
  
- `/users/follow/{friend_id}`: Follow friend, by adding the friend user to the list of following to the current user
  
- `/users/unfollow/{friend_id}`: Unfollow friend, by removing friend user from current user following list
  
- `/users/{user_id}/following`: Get the list of all users the current user following
  
- `/users/{user_id}/followers`: Get the list of all users following the current user
  

#### Posts

- `/posts/`: Create a new Post, the post will be created by a user
  
- `/posts/{post_id}`: Get, Update and Delete a post, when getting a post it will be returned with all its comments and likes
  
- `/posts/user/{user_id}`: Get all posts of a user
  

#### Comments:

- `/comments/`: Create a new comment
  
- `/comments/{comment_id}`: Get, Update and Delete a comment
  
- `/comments/post/{post_id}`: Get all comments of a post
  

#### Likes

- `/likes/`: Create a like object; "a user can like a post"
  
- `/likes/{like_id}`: Delete a like object; "a user can unlike a post he liked before"
  
- `likes/post/{post_id}`: Get all like objects of a post
