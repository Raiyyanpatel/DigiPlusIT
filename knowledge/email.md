# Email Delivery & Configuration (KB-EMAIL-01)

## Overview
Troubleshooting guide for Google Workspace (Gmail) and SMTP relay services.

## Common Issues & Resolutions

### 1. Emails Going to Spam (External Recipients)
- **Cause**: Missing or misconfigured SPF, DKIM, or DMARC records for a new subdomain.
- **Resolution**:
  1. Check domain health using MXToolbox.
  2. If it's a new marketing subdomain, escalate to the IT Infrastructure team to update DNS records.
  3. Create an Asana task for DNS changes.

### 2. Cannot Access Shared Mailbox
- **Cause**: Incorrect delegated access permissions or sync delay.
- **Resolution**:
  1. Verify the user is in the correct Google Group granting access.
  2. Instruct user to access the mailbox via "Open another mailbox" in Gmail web UI, rather than Outlook.
  3. Wait up to 24 hours for Google Workspace delegation to fully propagate if newly added.

### 3. Application Failing to Send Automated Emails
- **Cause**: Expired SendGrid API key or blocked by bounce limits.
- **Resolution**:
  1. Check the SendGrid activity feed for the specific application.
  2. If the IP is blacklisted, submit a delisting request.
  3. If API key is revoked, generate a new one and create a GitHub issue for the dev team to update their secrets.
