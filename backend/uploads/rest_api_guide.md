# REST API Guide

Base URL: https://api.techcorp.io/v1
Authentication: Bearer token in Authorization header.

Endpoints:

GET /users
Returns a list of all active users.
Query params: page, limit, role

POST /users
Creates a new user.
Body: { "name": "string", "email": "string", "role": "string" }

GET /users/{id}
Returns a single user by ID.

PUT /users/{id}
Updates an existing user.

DELETE /users/{id}
Soft-deletes a user (sets status to inactive).

All responses are JSON. Errors return a standard format:
{ "error": "message", "code": 400 }

Rate limit: 100 requests per minute per token.
