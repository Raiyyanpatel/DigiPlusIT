# Authentication, SSO & MFA (KB-AUTH-01)

## Overview
Troubleshooting guide for Okta SSO, Active Directory, and Duo Security MFA.

## Common Issues & Resolutions

### 1. User Locked Out of Okta
- **Cause**: Too many failed password attempts (more than 5).
- **Resolution**:
  1. Verify user identity via video call or manager approval.
  2. Unlock account in Okta Admin console.
  3. Send password reset link to personal backup email or manager.

### 2. Duo Push Not Arriving
- **Cause**: Poor cell reception, disabled notifications, or new phone without transfer.
- **Resolution**:
  1. Instruct user to open the Duo app manually and pull down to refresh.
  2. If they have a new phone, send a bypass code and trigger the Duo reactivation workflow.
  3. Fallback to SMS passcode if push fails entirely.

### 3. Application Missing from Okta Dashboard
- **Cause**: Missing group assignment or incorrect licensing.
- **Resolution**:
  1. Check the user's AD groups.
  2. Verify the application requires specific role-based access.
  3. If approved, add user to the appropriate provisioning group.
