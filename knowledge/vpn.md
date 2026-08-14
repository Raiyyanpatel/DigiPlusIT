# VPN Connectivity Troubleshooting (KB-VPN-01)

## Overview
This document outlines standard troubleshooting steps for the enterprise GlobalProtect VPN client.

## Common Issues & Resolutions

### 1. "Authentication Failed" error
- **Cause**: Outdated cached credentials or password expiration.
- **Resolution**: 
  1. Clear the VPN client cache.
  2. Verify SSO status via Okta.
  3. Reset Okta password if expired.

### 2. Frequent Disconnections (Every 5-10 mins)
- **Cause**: Outdated VPN client version or MTU mismatch.
- **Resolution**:
  1. Verify client version is at least v6.1.2.
  2. If outdated, instruct user to update via the Self Service Portal.
  3. Check home router MTU settings if issue persists.

### 3. "Cannot connect to portal" error
- **Cause**: ISP blocking IPsec (UDP 500/4500) or portal outage.
- **Resolution**:
  1. Force SSL VPN mode in client settings.
  2. If SSL fails, check status.digiplus.it for known portal outages.
  3. Create an engineering ticket if portal is unresponsive.
