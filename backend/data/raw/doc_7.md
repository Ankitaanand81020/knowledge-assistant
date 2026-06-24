# Architecture Overview & System Design

**Type:** technical  
**Tags:** architecture, system-design, technical  
**Date:** 2024-02-20

---

High-level Architecture:

Frontend (React + Next.js):
- Static site generation (SSG) for public pages
- Client-side rendering for dashboard
- API calls via axios
- State management: Redux
- Hosted on Vercel CDN

Backend (Python FastAPI):
- REST API with OpenAPI docs
- Async task processing with Celery
- Database: PostgreSQL + Redis cache
- Authentication: JWT + OAuth2
- Hosted on AWS EC2 (auto-scaling group)

Data Pipeline:
- Ingestion: S3 → Lambda → PostgreSQL
- Processing: Celery workers (3x standard)
- Export: PostgreSQL → S3 (daily)

Monitoring & Logging:
- Application logs: CloudWatch
- APM: New Relic
- Metrics: Prometheus + Grafana
- Alerts: PagerDuty
- Uptime monitoring: StatusPage

Database Schema:
- users: id, email, name, role
- sessions: id, user_id, token, created_at, expires_at
- data: id, user_id, content, created_at

API Endpoints (sample):
- POST /api/auth/login
- GET /api/users/{id}
- POST /api/data
- GET /api/data?limit=10&offset=0