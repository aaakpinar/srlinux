# SRLinux System Hardening Best Practices

This document provides SR Linux-specific best practices for system hardening, including configuration examples.

## 1. Password Complexity
To enhance security, enforce password complexity rules for SR Linux local users.

**Configuration Example:**
```bash
/system aaa authentication password complexity-rules {
    minimum-length 8
    maximum-length 1024
    minimum-lowercase 1
    minimum-uppercase 1
    minimum-numeric 1
    minimum-special-character 1
    allow-username false
}
```

## 2. User Lockouts
Define user lockout policies to prevent brute-force attacks by limiting failed login attempts.

**Configuration Example:**
```bash
/system aaa authentication password lockout-policy {
    attempts 3
    time 1        # Time period (in minutes) within which failed attempts are counted
    lockout 15    # Duration (in minutes) the user is locked out after reaching the limit
}
```

## 3. Password Aging
Implement password aging to enforce periodic changes by defining an expiration period.

**Configuration Example:**
```bash
/system aaa authentication password {
    aging 90      # Password expiry period in days
}
```

## 4. Password History
Restrict password reuse by maintaining a history of past passwords.

**Configuration Example:**
```bash
/system aaa authentication password {
    history 4     # Prevents reuse of the last 4 passwords
}
```

## 5. First Login Enforcement
Require new users to change their password on their first login.

**Configuration Example:**
```bash
/system aaa authentication password {
    change-on-first-login true
}
```

## 6. Bash Access Management
Control access to the Bash shell, limiting it to specific users or scenarios for advanced operations.

**Configuration Example:**
```bash
/system aaa authentication linuxadmin-user {
    password "your_password_here"   # Configure password for the linuxadmin user
}
```

## 7. User Role Management
Define roles with access to specific services, such as CLI, gNMI, and JSON-RPC, to enforce permissions for local and remote users.

**Configuration Example:**
```bash
/aaa authorization role local-user {
    services [
        cli
        gnmi
        json-rpc
    ]
}
```

## 8. JSON & gNMI Impact
Ensure that SR Linux management interfaces, such as CLI, gNMI, and JSON-RPC, reflect uniform hardening settings.

**Configuration Example:**
```bash
/aaa authorization role remote-user {
    services [
        cli
        gnmi
        json-rpc
    ]
    tacacs {
        priv-lvl 11
    }
}
```
