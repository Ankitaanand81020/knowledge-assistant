# Deployment & Release Process

**Type:** sop  
**Tags:** deployment, devops, process  
**Date:** 2024-01-20

---

Release & Deployment Workflow:

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
- test(user): Add 15 new test cases