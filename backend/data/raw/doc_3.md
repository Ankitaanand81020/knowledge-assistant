# Authentication & API Security

**Type:** technical  
**Tags:** api, security, technical  
**Date:** 2024-01-10

---

API Security Standards:

1. Authentication:
   - Use JWT tokens for API access
   - Token generation endpoint: POST /auth/token
   - Include token in Authorization header: Bearer {token}
   - Tokens expire after 24 hours

2. API Keys:
   - Generate from dashboard at dashboard.company.com/keys
   - Use X-API-Key header for service-to-service auth
   - Rotate keys quarterly
   - Never commit keys to git (use .env)

3. Rate Limiting:
   - 100 requests/minute per token
   - 10,000 requests/day per API key
   - Burst limit: 500 requests/minute

4. HTTPS:
   - All endpoints require HTTPS (TLS 1.3+)
   - Self-signed certs not allowed in production

5. IP Whitelisting:
   - Available for enterprise customers
   - Configure in Settings > Security

Example: curl -H 'Authorization: Bearer YOUR_TOKEN' https://api.company.com/v1/data