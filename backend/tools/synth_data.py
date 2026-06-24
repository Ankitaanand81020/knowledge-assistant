"""
Synthetic data generation script for company knowledge base.
Creates realistic sample documents across multiple themes.
"""

from pathlib import Path
import json
from datetime import datetime

raw = Path("data/raw")
raw.mkdir(parents=True, exist_ok=True)

# Comprehensive synthetic company knowledge base
docs = [
    # HR & Company Policies
    {
        "title": "Leave Policy & Guidelines",
        "content": """Our company provides comprehensive leave benefits:
- Annual Leave: 24 paid days per year
- Sick Leave: 10 days per year (paid)
- Casual Leave: 5 flexible days
- Maternity Leave: 4 months
- Paternity Leave: 2 weeks
- Bereavement Leave: 3 days
- Leaves are non-transferable and must be taken in the fiscal year.
- Request leave through the HR portal at least 5 days in advance.
- Emergency leave requires manager approval and HR notification.""",
        "tags": ["hr", "policy", "benefits"],
        "type": "policy",
        "date": "2024-01-15"
    },
    {
        "title": "Remote Work & Flexible Hours Policy",
        "content": """Flexible work arrangements are encouraged:
- Full-time remote work available on case-by-case basis
- Hybrid model: 3 days office, 2 days remote (default)
- Core hours: 10 AM - 4 PM local time
- Must attend quarterly in-person team meetings
- Home office setup subsidy: $500 one-time
- Internet reimbursement: up to $50/month
- Communication tools: Slack, Teams, Zoom
- Time tracking: Honor system based on trust""",
        "tags": ["hr", "policy", "remote"],
        "type": "policy",
        "date": "2024-03-20"
    },
    {
        "title": "Onboarding Checklist & First 30 Days",
        "content": """Day 1 (Monday):
- HR welcome meeting at 9 AM
- Laptop & equipment setup
- Building access card setup
- IT security briefing

Day 1-2:
- Meet direct manager
- Tour office facilities
- System access provisioning
- Email & calendar setup

Day 3-5:
- Team introduction meetings
- Codebase walkthrough
- Development environment setup
- First task assignment

Week 2-4:
- Pair programming sessions
- Customer/product introduction
- Architecture overview
- First code review & merge

Day 30 Review:
- 1:1 with manager
- Self-assessment
- Feedback collection
- Goal-setting for next quarter""",
        "tags": ["onboarding", "new-hire"],
        "type": "sop",
        "date": "2024-02-01"
    },
    # Technical Documentation
    {
        "title": "Authentication & API Security",
        "content": """API Security Standards:

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

Example: curl -H 'Authorization: Bearer YOUR_TOKEN' https://api.company.com/v1/data""",
        "tags": ["api", "security", "technical"],
        "type": "technical",
        "date": "2024-01-10"
    },
    {
        "title": "Development Environment Setup",
        "content": """Setting up your development environment:

Prerequisites:
- Git (v2.40+)
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker (for local testing)
- PostgreSQL 15

Steps:
1. Clone repo: git clone https://github.com/company/project.git
2. Backend setup:
   - cd backend
   - python -m venv venv
   - source venv/bin/activate
   - pip install -r requirements.txt
   - cp .env.example .env
   - Edit .env with your values
3. Database:
   - createdb company_dev
   - python manage.py migrate
4. Frontend setup:
   - cd ../frontend
   - npm install
   - npm run dev
5. Start backend:
   - cd ../backend
   - python manage.py runserver
6. Access at http://localhost:3000

Troubleshooting:
- Port conflicts: Change PORT in .env
- Database errors: Ensure PostgreSQL is running
- Dependencies: Run pip install --upgrade -r requirements.txt""",
        "tags": ["setup", "development", "tutorial"],
        "type": "tutorial",
        "date": "2024-02-15"
    },
    {
        "title": "Deployment & Release Process",
        "content": """Release & Deployment Workflow:

1. Code Review:
   - Create feature branch: git checkout -b feature/name
   - Create pull request
   - Require 2 approvals
   - Pass CI/CD checks

2. Testing:
   - Unit tests: npm run test (frontend) / pytest (backend)
   - Integration tests: npm run test:integration
   - E2E tests: npm run test:e2e (staging only)
   - Coverage target: 80%+

3. Staging Deployment:
   - Tag: git tag v1.2.3
   - Push: git push origin v1.2.3
   - Auto-deploys to staging
   - Run smoke tests

4. Production Deployment:
   - Merge to main branch
   - Create release notes
   - Deploy during maintenance window (Sundays 2-4 AM UTC)
   - Monitor logs & metrics for 1 hour

5. Rollback:
   - If critical error: git revert & push
   - Message on #deployments channel
   - Post-mortem within 24 hours

Commit message format:
- feat(auth): Add OAuth login
- fix(api): Handle null responses
- docs(readme): Update setup steps
- test(user): Add 15 new test cases""",
        "tags": ["deployment", "devops", "process"],
        "type": "sop",
        "date": "2024-01-20"
    },
    # FAQ & Troubleshooting
    {
        "title": "Common Questions & Troubleshooting",
        "content": """Q: How do I reset my password?
A: Visit https://dashboard.company.com/reset-password or contact IT support.

Q: I can't connect to the VPN.
A: Ensure Cisco AnyConnect is installed. Try: cisco-anyconnect vpn.company.com. Contact IT if issue persists.

Q: How do I report a bug?
A: File an issue on Jira (jira.company.com) with 'BUG' label and priority.

Q: Can I access production logs?
A: Only ops team has direct access. Submit request via #prod-support in Slack.

Q: How often are backups taken?
A: Daily at 2 AM UTC. Retention: 30 days. Recovery time: ~1 hour.

Q: What's the incident response procedure?
A: Critical: Page on-call via Pagerduty. Non-critical: File ticket on Jira.

Q: How do I request a new tool/license?
A: Submit to ops@company.com with business justification. Approval within 5 business days.

Q: Where's the company culture handbook?
A: See company.sharepoint.com/culture (access via SSO)""",
        "tags": ["faq", "troubleshooting", "support"],
        "type": "faq",
        "date": "2024-03-10"
    },
    {
        "title": "Architecture Overview & System Design",
        "content": """High-level Architecture:

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
- GET /api/data?limit=10&offset=0""",
        "tags": ["architecture", "system-design", "technical"],
        "type": "technical",
        "date": "2024-02-20"
    },
    # Team & Contact Info
    {
        "title": "Team Directory & Contact Info",
        "content": """Engineering Team:
- Alice Johnson (CTO): alice.johnson@company.com | Slack: @alice
- Bob Smith (Backend Lead): bob.smith@company.com | Ext: 2341
- Carol White (Frontend Lead): carol.white@company.com | Slack: @carol
- David Lee (DevOps): david.lee@company.com | On-call Sat-Sun

Product & Design:
- Emma Davis (Product Manager): emma.davis@company.com
- Frank Zhang (UX Designer): frank.zhang@company.com

Support:
- General: support@company.com
- HR: hr@company.com
- IT: it@company.com
- Finance: finance@company.com

Chats & Groups:
- #engineering: Main channel
- #deployments: Release updates
- #random: Off-topic discussions
- @devops-oncall: Incident response

Office Hours:
- Engineering standup: 9 AM daily (Teams meeting)
- Product sync: 3 PM Wed
- All-hands: 4 PM Fri

Departments:
- Engineering: 15 people
- Product: 3 people
- Design: 2 people
- Operations: 4 people""",
        "tags": ["team", "contact", "directory"],
        "type": "reference",
        "date": "2024-03-01"
    },
]

# Write documents to files
for i, doc in enumerate(docs):
    # Markdown format
    md_path = raw / f"doc_{i}.md"
    md_content = f"""# {doc['title']}

**Type:** {doc['type']}  
**Tags:** {', '.join(doc['tags'])}  
**Date:** {doc['date']}

---

{doc['content']}"""
    md_path.write_text(md_content, encoding="utf-8")
    
    # JSON format (metadata)
    json_path = raw / f"doc_{i}.json"
    json_content = {
        "title": doc["title"],
        "content": doc["content"],
        "tags": doc["tags"],
        "type": doc["type"],
        "date": doc["date"]
    }
    json_path.write_text(json.dumps(json_content, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✅ Created {len(docs)} synthetic documents in data/raw/")
print(f"   - {len(docs)} Markdown files (.md)")
print(f"   - {len(docs)} JSON metadata files (.json)")
print(f"\nSample topics covered:")
for doc in docs:
    print(f"   - {doc['title']}")
print(f"\nNext step: Run backend reindex to build embeddings")