# Project API Documentation

## Activity 5: User Authentication

### Features
- User Registration
- User Login with JWT authentication
- Access to protected routes only for authenticated users
- Password hashing using Django's built-in password hasher
- Proper error handling for invalid credentials and unauthorized access

### API Endpoints

| Method | Endpoint            | Description                     | Request Body / Headers                            | Sample Response                                              |
|--------|---------------------|---------------------------------|-------------------------------------------------|--------------------------------------------------------------|
| POST   | `/api/register/`    | Register a new user             | JSON: `{ "username": "", "email": "", "password": "" }` | `{ "id": 1, "username": "user1", "email": "user1@example.com" }` |
| POST   | `/api/token/`       | Obtain JWT token (login)        | JSON: `{ "username": "", "password": "" }`      | `{ "access": "token", "refresh": "refresh_token" }`          |
| POST   | `/api/token/refresh/` | Refresh JWT access token       | JSON: `{ "refresh": "refresh_token" }`           | `{ "access": "new_access_token" }`                           |
| GET    | `/api/me/`          | Get current authenticated user | Header: `Authorization: Bearer <access_token>`  | `{ "id": 1, "username": "user1", "email": "user1@example.com" }` |

---

## Activity 6: CRUD Operations

### Features
- CRUD endpoints for three models: BlogPost, Goal, and Comment
- All requests require JWT authentication
- Each model supports creating, reading, updating, and deleting resources
- Data access is scoped to the authenticated user (users can only manage their own data)
- Proper error handling for unauthorized or invalid operations

### API Endpoints

#### BlogPost

| Method | Endpoint           | Description                    | Request Body                    | Sample Response         |
|--------|--------------------|-------------------------------|--------------------------------|-------------------------|
| GET    | `/api/posts/`      | List all blog posts (user only) | Header: `Authorization: Bearer <token>` | List of posts JSON       |
| POST   | `/api/posts/`      | Create a new blog post         | `{ "title": "", "content": "" }` | Created post JSON        |
| GET    | `/api/posts/{id}/` | Retrieve a single blog post    | Header: `Authorization: Bearer <token>` | Post detail JSON         |
| PUT    | `/api/posts/{id}/` | Update a blog post             | `{ "title": "", "content": "" }` | Updated post JSON        |
| DELETE | `/api/posts/{id}/` | Delete a blog post             | Header: `Authorization: Bearer <token>` | 204 No Content           |

#### Goal

| Method | Endpoint          | Description                | Request Body                    | Sample Response         |
|--------|-------------------|----------------------------|--------------------------------|-------------------------|
| GET    | `/api/goals/`     | List user goals            | Header: `Authorization: Bearer <token>` | List of goals JSON       |
| POST   | `/api/goals/`     | Create a new goal          | `{ "title": "", "description": "" }` | Created goal JSON        |
| GET    | `/api/goals/{id}/` | Retrieve a single goal     | Header: `Authorization: Bearer <token>` | Goal detail JSON         |
| PUT    | `/api/goals/{id}/` | Update a goal              | `{ "title": "", "description": "" }` | Updated goal JSON        |
| DELETE | `/api/goals/{id}/` | Delete a goal              | Header: `Authorization: Bearer <token>` | 204 No Content           |

#### Comment

| Method | Endpoint             | Description               | Request Body                    | Sample Response         |
|--------|----------------------|---------------------------|--------------------------------|-------------------------|
| GET    | `/api/comments/`     | List user comments        | Header: `Authorization: Bearer <token>` | List of comments JSON    |
| POST   | `/api/comments/`     | Create a new comment      | `{ "post": post_id, "content": "" }` | Created comment JSON     |
| GET    | `/api/comments/{id}/` | Retrieve a single comment | Header: `Authorization: Bearer <token>` | Comment detail JSON      |
| PUT    | `/api/comments/{id}/` | Update a comment          | `{ "content": "" }`             | Updated comment JSON     |
| DELETE | `/api/comments/{id}/` | Delete a comment          | Header: `Authorization: Bearer <token>` | 204 No Content           |

## Activity 7: Rate Limiting

### Features
- Custom rate limiting decorator to limit incoming requests per client (user or IP).
- Limits requests to 5 per 60 seconds by default (configurable).
- Returns HTTP 429 Too Many Requests when limit exceeded.
- Includes informative JSON error message.
- Supports both authenticated users and anonymous clients (by IP address).

### API Endpoints with Rate Limiting

| Method | Endpoint                           | Description                                    | Request Headers                                   | Sample Response                                      |
|--------|----------------------------------|------------------------------------------------|--------------------------------------------------|------------------------------------------------------|
| GET    | `http://127.0.0.1:8000/api/me/` | Retrieve authenticated user's profile (rate limited) | `Authorization: Bearer <access_token>`            | **Success (200):**<br>```json {"id":1,"username":"user1","email":"user1@example.com"}```<br><br>**Rate Limit Exceeded (429):**<br>```json {"detail": "Rate limit exceeded. Try again later."}``` |

### Rate Limit Policy
- Maximum of 5 requests per 60 seconds per user or IP address.
- When exceeded, API returns status code 429 and blocks further requests until the window resets.
