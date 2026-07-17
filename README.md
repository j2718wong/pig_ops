# SuperPig

SuperPig is a **mobile-first pig farm management platform** originally built to help manage my family's pig farm remotely. It was designed around the operational realities of small farms, where workers primarily use smartphones, internet connectivity is often unreliable, and business events such as breeding, vaccinations, inventory, and sales require strict transactional accuracy.

These constraints shaped the architecture, resulting in an offline-capable Progressive Web App (PWA), a FastAPI backend, asynchronous processing services, and a transaction-centric MySQL database.

## Live System

🧠 Production Application: https://superpig.jsysdev.com

📱 End-to-End Demo:
https://drive.google.com/file/d/1moiiK67ppN8WbLEFblpvwnY6eVgztEGi/view?usp=drive_link

⚙️ Backend & Infrastructure Walkthrough:
https://drive.google.com/file/d/1Dp_shk55O44uMWjzsAeiwKjaBKpnitRS/view?usp=drive_link

---

# Why SuperPig Exists

SuperPig was originally developed to solve a real operational problem on my family's pig farm.

The project later evolved into a reusable platform for small and medium-sized pig farms. Although it was originally intended to become a commercial SaaS product, it is now fully open source and serves as a public demonstration of my approach to backend engineering, database design, and system architecture.

---

# Engineering Constraints

Rather than choosing technologies first, the platform was designed around several operational constraints.

### Mobile-first

Farm workers primarily interact with the system using smartphones while working around the farm. Every workflow was therefore designed for mobile devices first.

### Offline-capable

Internet connectivity inside pig farms is often unreliable.

The application continues to function when connectivity is lost and synchronizes data when the connection returns.

### Data Integrity

Breeding schedules, vaccinations, inventory, financial records, and pig movements must remain accurate.

Critical business rules are therefore implemented as transactional MySQL stored procedures to ensure ACID-compliant consistency regardless of which API endpoint modifies the data.

### Operational Simplicity

The production environment intentionally favors a lean deployment model with minimal operational overhead.

---

# System Architecture

SuperPig consists of five independently maintained repositories.

| Repository | Purpose |
|------------|---------|
| pig_ops | FastAPI backend |
| pig_ops_ui_mob | Mobile-first PWA frontend |
| pig_ops_db | Database schema, migrations and stored procedures |
| pig_ops_bkops | Background processing services |
| pig_ops_admin | Administrative portal |

---

# Technology Stack

Backend

- FastAPI
- Python
- REST APIs
- Asynchronous background workers

Frontend

- Vanilla JavaScript
- Progressive Web App (PWA)
- Mobile-first SPA

Database

- MySQL
- 143 Stored Procedures
- 69 Database Migrations

Infrastructure

- Nginx
- Shell deployment scripts
- Bare-metal Linux deployment

---

# Project Scale

| Metric | Value |
|--------|------:|
| Public Repositories | 5 |
| Git Commits | 1,680 |
| Source Files | 623 |
| Lines of Code | 214,713 |
| MySQL Stored Procedures | 143 |
| Database Tables | 80+ |
| Background Worker Services | 27 |

---

# Deployment Philosophy

Rather than deploying with Kubernetes or Docker, SuperPig intentionally uses a lean bare-metal deployment.

The FastAPI backend, MySQL database, background workers, and Nginx reverse proxy execute on a single Linux host. This architecture minimizes operational complexity while remaining appropriate for the expected deployment scale.

Deployment is handled using custom shell scripts which:

- synchronize all repositories
- invalidate frontend caches
- restart application services
- maintain deployment logs

---

# Repository Layout

```text
~/projects/jsys/
├── pig_ops/
├── pig_ops_db/
├── pig_ops_ui_mob/
├── pig_ops_bkops/
└── pig_ops_admin/
```

---

# Additional Documentation

- Backend architecture walkthrough
- Database design
- Deployment scripts
- Reverse proxy configuration
- Source code