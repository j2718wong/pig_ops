# SuperPig Engineering Case Study

## Building a Database-Centric Transaction Processing System

## Overview

SuperPig is a mobile-first pig farm management platform originally developed to manage my family's pig farm remotely.

The project later evolved into a reusable platform for small and medium-sized pig farms.

Unlike many modern web applications, SuperPig was designed **database-first**, where business workflows were implemented and validated before any user interface was developed.

This document explains the engineering decisions behind the project.

---

# Development Philosophy

Most web applications evolve like this:

```text
UI
 ↓
REST API
 ↓
Business Logic
 ↓
Database
```

SuperPig evolved differently:

```text
Database Schema
        ↓
Stored Procedures
        ↓
SQL Testing
        ↓
FastAPI
        ↓
Text Reports
        ↓
Progressive Web App
```

For several months, the system was exercised entirely through SQL by executing stored procedures directly.

Only after the business rules stabilized was the web interface developed.

---

# Why Business Logic Lives Inside MySQL

A single business event, such as recording an insemination, affects many business entities:

- Production History
- Sow Status
- Boar Status
- Pig Operations
- Farm Statistics
- Account Statistics
- Notes
- Cache Synchronization
- Supplier Information

These updates must succeed or fail as one transaction.

Instead of executing dozens of SQL statements from FastAPI, the application performs:

```sql
CALL pig_prod_add(...);
```

The database becomes responsible for maintaining transactional consistency.

## Benefits

- ACID-compliant transactions
- One database round trip
- Shared business rules
- No duplicated logic
- Easier database-first testing

## Tradeoffs

- Larger stored procedures
- More SQL-centric architecture
- Higher learning curve for web developers

This was a deliberate architectural decision rather than a technical limitation.
