# Engineering Best Practices

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
