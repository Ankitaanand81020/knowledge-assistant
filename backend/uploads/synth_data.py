import json
import os
from datetime import datetime

documents = [
    {
        "title": "Company Overview",
        "type": "company",
        "tags": ["company", "overview", "internal"],
        "content": """# Company Overview

TechCorp was founded in 2018 with a mission to simplify internal knowledge management.
We have 3 offices: New York, London, and Bangalore.
Our core teams are Engineering, Product, HR, and Finance.
The CEO is Sarah Mitchell. CTO is Raj Patel.
We operate Monday to Friday, 9am to 6pm local time.
"""
    },
    {
        "title": "Leave Policy",
        "type": "policy",
        "tags": ["hr", "policy", "leave"],
        "content": """# Leave Policy

All full-time employees are entitled to 20 days of paid annual leave per year.
Leave must be applied at least 3 days in advance via the HR portal.
Sick leave is separate: up to 10 days per year with a medical certificate.
Maternity leave is 26 weeks fully paid. Paternity leave is 2 weeks.
Unused leave cannot be carried forward beyond 5 days into the next year.
Leave during probation (first 6 months) is limited to 5 days.
"""
    },
    {
        "title": "Payroll FAQ",
        "type": "faq",
        "tags": ["hr", "payroll", "faq"],
        "content": """# Payroll FAQ

Q: When is payday?
A: Salaries are credited on the last working day of every month.

Q: How do I access my payslip?
A: Log in to the HR portal at hr.techcorp.internal and go to Payslips.

Q: Who do I contact for salary issues?
A: Email payroll@techcorp.internal or raise a ticket in the HR portal.

Q: Is there a performance bonus?
A: Yes, annual bonuses are paid in March based on yearly appraisal scores.

Q: How do I update my bank account details?
A: Submit a request via the HR portal under Profile > Bank Details.
"""
    },
    {
        "title": "Onboarding Checklist",
        "type": "sop",
        "tags": ["onboarding", "sop", "new-hire"],
        "content": """# Onboarding Checklist

Day 1:
- Collect your laptop from IT desk (Floor 2)
- Set up your email and Slack account
- Meet your manager and team
- Complete the security awareness training (link sent to email)

Day 2:
- Get access to GitHub, Jira, and Confluence
- Read the engineering handbook
- Attend the onboarding session at 10am (Google Meet link in calendar)

Week 1:
- Complete payroll setup in HR portal
- Submit ID documents to HR
- Shadow a senior engineer for 2 days
- Set up local dev environment using the setup guide

Week 2:
- Pick your first ticket from the backlog
- Daily standups at 9:30am on Slack Huddle
"""
    },
    {
        "title": "REST API Guide",
        "type": "tutorial",
        "tags": ["engineering", "api", "tutorial"],
        "content": """# REST API Guide

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
"""
    },
    {
        "title": "Engineering Best Practices",
        "type": "sop",
        "tags": ["engineering", "standards", "sop"],
        "content": """# Engineering Best Practices

Code Reviews:
- All PRs must have at least 1 approval before merging
- Review within 24 hours of request
- Use GitHub comments for feedback, not Slack

Branching Strategy:
- main: production only
- develop: integration branch
- feature/your-name/ticket-id: your work branch

Commit Messages:
- Use conventional commits: feat:, fix:, docs:, chore:
- Example: feat: add login endpoint for user auth

Testing:
- Minimum 70% unit test coverage for new code
- Integration tests required for all API endpoints
- Run tests locally before pushing: npm test

Deployments:
- Deployments happen every Tuesday and Thursday at 2pm
- Hotfixes can be deployed any time with CTO approval
"""
    },
    {
        "title": "IT Support Guide",
        "type": "faq",
        "tags": ["it", "support", "faq"],
        "content": """# IT Support Guide

Q: How do I reset my password?
A: Go to accounts.techcorp.internal and click Forgot Password.

Q: My laptop is slow. What should I do?
A: Restart it first. If still slow, raise a ticket at it.techcorp.internal.

Q: How do I connect to the VPN?
A: Download Cisco AnyConnect from the IT portal. Use vpn.techcorp.io as the server.
Credentials are your company email and password.

Q: Can I install software on my laptop?
A: Only IT-approved software. Submit a request via the IT portal.

Q: I lost my laptop. What do I do?
A: Call IT immediately at +1-800-TECHCORP. They will remotely wipe the device.

Q: How do I get a second monitor?
A: Submit a hardware request in the IT portal. Delivery takes 3-5 business days.
"""
    },
]

def generate_documents():
    os.makedirs("data/raw", exist_ok=True)

    for doc in documents:
        slug = doc["title"].lower().replace(" ", "_").replace(":", "").replace("/", "_")

        # Write the markdown content file
        md_path = f"data/raw/{slug}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(doc["content"])

        # Write the metadata JSON file
        meta = {
            "title": doc["title"],
            "type": doc["type"],
            "tags": doc["tags"],
            "date": datetime.now().isoformat(),
            "source": f"{slug}.md"
        }
        json_path = f"data/raw/{slug}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        print(f"Created: {slug}.md + {slug}.json")

    print(f"\nDone. {len(documents)} documents created in data/raw/")

if __name__ == "__main__":
    generate_documents()