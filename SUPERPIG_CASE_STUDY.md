# SuperPig Engineering Case Study

## Building a Database-Centric Transaction Processing System

### Overview

SuperPig is a mobile-first pig farm management platform originally developed to manage my family's pig farm remotely. While it eventually evolved into a complete Progressive Web Application (PWA) with a FastAPI backend and asynchronous processing services, the project began from a very different perspective than most modern web applications.

Rather than designing user interfaces first, I designed the business engine first.

The primary objective was never to build a website—it was to build a system capable of accurately representing the operational state of a pig farm while guaranteeing transactional consistency across hundreds of interconnected business rules.

This document explains the engineering decisions behind that architecture.

---

# Development Philosophy

Most web applications begin with the user interface.

```
UI
 ↓
REST API
 ↓
Business Logic
 ↓
Database
```

SuperPig evolved in almost the opposite direction.

```
Database Schema
        ↓
Stored Procedures
        ↓
SQL Testing & Text Reports
        ↓
FastAPI
        ↓
Progressive Web App
```

For several months, the system had no production user interface.

Every feature was developed by executing stored procedures directly inside MySQL, validating the resulting data, and generating reports directly from SQL.

Only after the business workflows stabilized was the mobile interface developed.

This allowed the core business engine to mature independently from presentation concerns.

---

# Why Database-Centric Business Logic?

One production event inside a pig farm rarely affects a single table.

For example, recording an insemination updates multiple business entities simultaneously:

* Production history
* Sow status
* Boar status
* Farm statistics
* Account statistics
* Pig operations
* Notes
* Cache synchronization versions
* Relationship tables
* Supplier information

These updates must either all succeed or all fail.

Rather than orchestrating dozens of individual database calls from the application layer, each business event is encapsulated inside a transactional stored procedure.

```
Client

      ↓

FastAPI

      ↓

CALL pig_prod_add(...)

      ↓

MySQL Transaction

      ↓

Update multiple business entities

      ↓

Commit
```

This architecture provides:

* ACID-compliant consistency
* Single transactional boundary
* Reduced database round trips
* Centralized business rules
* Shared logic across every API endpoint

The objective was correctness before convenience.

---

# Thin API Layer by Design

The FastAPI backend intentionally contains very little business logic.

Its responsibilities are limited to:

* Authentication
* Authorization
* Request validation
* Input normalization
* HTTP transport
* Response formatting
* File uploads

After validation, the API delegates transactional work to the database.

This often makes the Python code appear deceptively simple.

That simplicity is intentional.

The complexity resides where transactional consistency matters most: inside the database.

---

# Why Stored Procedures Instead of an ORM?

Modern Python applications commonly place business logic inside service classes backed by an ORM.

I intentionally chose a different approach.

The project originated from my background in enterprise database engineering, where complex transactional workflows were routinely implemented inside Oracle PL/SQL and PostgreSQL/MySQL stored procedures.

For SuperPig, the database is not merely persistent storage.

It is the business engine.

Advantages of this approach include:

* Centralized transactional rules
* Reduced application/database network traffic
* Elimination of duplicated business logic
* Deterministic execution of complex workflows
* Ability to test business functionality independently from the UI

Tradeoffs include:

* Larger stored procedures
* Greater emphasis on SQL expertise
* Less familiar architecture for developers accustomed to ORM-centric applications

This was a conscious architectural decision rather than a technical limitation.

---

# Database-First Development

One unexpected advantage of this architecture was development speed.

Because every business workflow existed as a stored procedure, the application could be exercised entirely through SQL.

For example:

```
CALL pig_prod_add(...)

↓

Inspect resulting database state

↓

Verify reports

↓

Adjust business rules

↓

Repeat
```

No frontend development was required to validate new functionality.

This allowed business workflows to mature before investing time in user interface development.

---

# Offline-First Mobile Architecture

The intended users of SuperPig are farm workers.

Typical working conditions include:

* Poor network connectivity
* Outdoor environments
* Smartphone-only usage
* Shared devices
* Intermittent internet access

These operational realities influenced every architectural decision.

The frontend was therefore implemented as a Progressive Web Application capable of offline operation with later synchronization.

The objective was to adapt the software to the farm rather than forcing the farm to adapt to the software.

---

# Evolution of My Architecture

The overall architectural philosophy remained consistent throughout my career.

| System               | Database           | Business Layer           | Application Layer |
| -------------------- | ------------------ | ------------------------ | ----------------- |
| ERG Transit Systems  | Oracle             | PL/SQL Stored Procedures | pyWeb2            |
| Liricco Technologies | PostgreSQL / MySQL | Stored Procedures        | Flask             |
| SuperPig             | MySQL              | Stored Procedures        | FastAPI           |

Although the frameworks evolved, the underlying design philosophy remained consistent:

* model business events
* preserve transactional integrity
* minimize unnecessary database traffic
* separate transport concerns from business rules

---

# Engineering Tradeoffs

Every architecture involves tradeoffs.

SuperPig intentionally prioritizes:

* Transactional consistency over ORM convenience
* Business correctness over framework trends
* Database execution over repeated network communication
* Stable business rules before user interface development
* Operational simplicity over infrastructure complexity

For the expected deployment scale, this resulted in a simpler production environment while maintaining strong data integrity.

---

# Lessons Learned

If rebuilding SuperPig today, I would retain the database-centric transactional model while improving several areas:

* automated integration testing around stored procedures
* richer architectural documentation
* stronger CI/CD automation
* improved API observability
* optional event-driven integration for external systems

I would not fundamentally change the decision to centralize complex transactional workflows inside the database.

That decision remains appropriate for a system whose primary complexity lies in maintaining consistency across many interconnected business entities.

---

# Conclusion

SuperPig was never intended to demonstrate proficiency with a particular framework.

Instead, it demonstrates an engineering philosophy.

The project reflects my experience building enterprise transaction-processing systems where data integrity, deterministic behavior, and maintainable business workflows were more important than following a specific architectural trend.

FastAPI, MySQL, and Progressive Web Apps were implementation choices.

The core objective has always been the same:

Design software around business events, preserve transactional integrity, and build systems whose correctness does not depend on the user interface.
