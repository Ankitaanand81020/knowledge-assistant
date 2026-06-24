# Development Environment Setup

**Type:** tutorial  
**Tags:** setup, development, tutorial  
**Date:** 2024-02-15

---

Setting up your development environment:

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
- Dependencies: Run pip install --upgrade -r requirements.txt