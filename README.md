# SuperPig: Bare-Metal Production Infrastructure & Systems Engineering

🧠 **Production Application:** [https://superpig.jsysdev.com](https://superpig.jsysdev.com)  
📱 **End-to-End System Demo:** [Watch the Video Walkthrough](https://drive.google.com/file/d/1moiiK67ppN8WbLEFblpvwnY6eVgztEGi/view?usp=drive_link)  
⚙️ **Backend & Database Infrastructure Tour:** [Watch the Engineering Breakdown](https://drive.google.com/file/d/1Dp_shk55O44uMWjzsAeiwKjaBKpnitRS/view?usp=drive_link)


## 📊 Codebase Metrics & Git Repository Breakdown

Below is the definitive performance and composition audit across the 5 decoupled repositories comprising the SuperPig ecosystem.

```text
========================================================================
📂 REPOSITORY TOPOGRAPHY & COMMIT VOLUME
========================================================================
  📦 pig_ops         │ 729 Commits  │ Core FastAPI Backend Engine
  📦 pig_ops_ui_mob  │ 626 Commits  │ Zero-Dependency PWA Frontend
  📦 pig_ops_db      │ 269 Commits  │ Transactional Schemas & Migrations
  📦 pig_ops_bkops   │  51 Commits  │ Asynchronous Background Workers
  📦 pig_ops_admin   │   5 Commits  │ Payment Settlement Gateway
  ───────────────────┴──────────────┴────────────────────────────────────
  📈 GRAND TOTAL     │ 1,680 Commits │ Continuous Lifespan: September 2025 to April 2026
```

### 🛠️ Language & Structural Composition

| Component / Layer | File Type | Files | Total Lines | Avg Lines/File | Structural Purpose |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Database Transactional Layer** | MySQL Stored Procedures | 143 | **30,030** | 210 | Core business logic execution & ACID safety |
| **Schema State Control** | DB Migrations | 69 | **3,702** | 53 | Immutable database version tracking |
| **Core Asynchronous Backend** | Python (FastAPI) | 135 | **52,907** | 391 | High-throughput API endpoint architecture |
| **Distributed Task Processing** | Python (Background Ops) | 27 | **5,070** | 187 | Decoupled cron workflows & data processing |
| **Framework-Agnostic UI** | JavaScript (Vanilla SPA) | 195 | **101,324** | 519 | Lightweight, zero-runtime frontend layout |
| **System Interface Templates** | HTML / JSON / CSS | 25 | **15,092** | 603 | Presentation layer & caching configurations |
| **Infrastructure Controls** | Shell Scripts | 19 | **3,012** | 158 | Bare-metal deployment & lifecycle automation |
| **🧮 SYSTEM AGGREGATE** | **All Modules Combined** | **623** | **214,713** | **344** | **Production-grade scalable architecture** |



---

This document details the production environment for SuperPig. Architected as a **lean, bare-metal monolith**, the entire ecosystem executes directly on a single host. By consolidating the asynchronous Python backend, optimized MySQL relational database, and background processing systems onto a unified server, network latency is dropped to absolute zero, maximizing data processing speed while drastically lowering resource overhead.

---

### 🧠 Architectural Paradigm: The Pragmatic Monolith

While modern trends default to heavy container orchestration, SuperPig deliberately implements a **zero-overhead, containerless deployment pattern**. 
* **Zero Latency:** Shared memory space and Unix socket loops provide instantaneous backend-to-database execution.
* **Atomic Velocity:** Code changes are verified and promoted via a highly optimized, custom shell engine. 
* **Predictable Security:** Nginx acts as an uncompromised reverse-proxy handling SSL termination, static file caching, and custom edge failovers.

---

### 📂 Multi-Repository Production Topography

The system runs out of a unified, decoupled project tree (`~/projects/jsys`), breaking down into 5 functional, atomic repositories:

```text
~/projects/jsys/
├── app.pid              # Active Process ID of the asynchronous FastAPI runtime
├── deploy_logs/         # Automated logs for code updates
├── deploy.sh*           # High-velocity deployment engine
├── restart_logs/        # High-availability runtime logging
├── restart.sh*          # Process lifecycle automation controller
├── version.txt          # Active production immutable build tag
│
├── pig_ops/             # Core Backend (FastAPI, business logic routes)
├── pig_ops_db/          # Database Layer (143 Stored Procedures, schema migrations)
├── pig_ops_ui_mob/      # Mobile Frontend (101k lines of modular Vanilla JS SPA)
├── pig_ops_bkops/       # Background Ops (Asynchronous background processing workers)
└── pig_ops_admin/       # Administrative Gateway (Manual payment handling & ledger settlement)
```

---

### 🚀 Zero-Downtime Deployment Automation (`deploy.sh`)

To eliminate the bloat of external third-party CI/CD runners, production releases are controlled by a custom shell orchestration engine. Running `./deploy.sh` initiates an automated multi-step update pipeline:

1. **State Isolation:** Tracks and captures the live FastAPI runtime process via `app.pid`.
2. **Atomic Synchronization:** Pulls structural revisions across the decoupled repositories cleanly.
3. **Cache Invalidation:** Updates the `version.txt` tag to forcefully bust static assets at the user edge.
4. **Graceful Reloading:** Invokes `./restart.sh` to safely flush process buffers and cycle the server instance.

---

### 🌐 Reverse Proxy & Edge Infrastructure (Nginx Topology)

Nginx handles edge traffic, enforcing HTTP/2 protocol optimizations, caching policies, and an automated upstream fallback mechanism.

#### 1. Static Asset Caching Layer
To bypass backend compute cycles, Nginx maps directly to the decoupled mobile frontend repository (`pig_ops_ui_mob`), serving raw Single Page Application assets directly from the filesystem with optimized HTTP cache control headers:

```nginx
location /static/ {
    alias /root/projects/jsys/pig_ops_ui_mob/static/;
    expires 30d;
    add_header Cache-Control "public, no-transform";
}

location /static_m/ {
    alias /root/projects/jsys/pig_ops_ui_mob/src/static/;
    expires 30d;
    add_header Cache-Control "public, no-transform";
}
```

#### 2. High-Availability Maintenance Injection
If the upstream FastAPI program resets during updates, Nginx intercepts the `502/503/504` errors at the edge, instantaneously serving an isolated maintenance layout without crashing the client's progressive web app:

```nginx
error_page 502 503 504 /maintenance.html;
location = /maintenance.html {
    root /root/projects/jsys/pig_ops/webroot/templates;
    internal;
}
```

#### 3. Core Upstream Routing
All root application traffic is proxied directly into the local loopback interface (`127.0.0.1:8080`), passing clean client telemetry up to FastAPI:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade \$http_upgrade;
    proxy_set_header Connection "upgrade";
}
```
