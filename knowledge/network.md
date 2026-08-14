# Office Network Infrastructure (KB-NET-01)

## Overview
Troubleshooting guide for office Wi-Fi, switching, and routing (Meraki/Cisco).

## Common Issues & Resolutions

### 1. "Corp-WiFi" Not Connecting
- **Cause**: Expired RADIUS certificate on client device or incorrect EAP-TLS profile.
- **Resolution**:
  1. Instruct user to "Forget" the network.
  2. Re-enroll the device via the internal MDM portal (Jamf/Intune).
  3. Verify the device is compliant in the MDM dashboard.

### 2. Slow Network Speeds in Office
- **Cause**: Access Point saturation or interference.
- **Resolution**:
  1. Check the Meraki Dashboard for high channel utilization on the specific AP.
  2. Ask user to move to a different zone if one AP is overwhelmed.
  3. Reboot the AP if it shows anomalous memory usage.

### 3. Cannot Access Internal Staging Servers
- **Cause**: Missing office IP whitelist in AWS Security Groups.
- **Resolution**:
  1. Verify the user is connected to the office network, not guest.
  2. Check if the staging environment was recently rebuilt (which might reset SG rules).
  3. Create a GitHub issue for DevOps to update the Terraform configuration with the current office egress IPs.
