### README.md
```markdown
# Sales Demo API

A RESTful API built with Flask and a Vue.js frontend for managing sales data, deployed on AWS Elastic Beanstalk with a PostgreSQL RDS backend.

## Overview
This project implements a simple sales management system where users can:
- Authenticate via JWT.
- Perform CRUD operations on sales records (create, read, update, delete).
- Visualize sales data in a dashboard with a chart.

## Setup Instructions

### Prerequisites
- Python 3.9
- Node.js and npm
- AWS CLI (`aws configure` with credentials)
- Elastic Beanstalk CLI (`eb` installed via `pip install awsebcli`)
- PostgreSQL client (e.g., `pgAdmin`) for RDS access

### Backend Setup (Flask)
1. **Clone Repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-dir>
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   - Key packages: `Flask`, `Flask-SQLAlchemy`, `psycopg2-binary`, `PyJWT`, `python-dotenv`.
3. **Local Environment (Optional):**
   - Create `.env`:
     ```
     DATABASE_URL=postgresql://admin:<your-password>@localhost:5432/salesdb
     SECRET_KEY=your-secret-key
     ```
   - Run: `python app.py` (serves at `http://localhost:5000`).

### Frontend Setup (Vue)
1. **Navigate to Frontend:**
   ```bash
   cd frontend  # Adjust if folder name differs
   ```
2. **Install Dependencies:**
   ```bash
   npm install
   ```
3. **Run Locally:**
   ```bash
   npm run serve
   ```
   - Serves at `http://localhost:8080`, hardcoded to `http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com`.

### Database Setup
- **RDS Instance:** `salesdb1-instance.cbkw6ke2kh9f.ap-southeast-2.rds.amazonaws.com`.
- **Schema:**
  ```sql
  CREATE TABLE sales (
      id SERIAL PRIMARY KEY,
      date DATE NOT NULL,
      amount FLOAT NOT NULL
  );
  ```
- **Connect Locally (Test):**
  - Use `pgAdmin` with `admin:<your-password>@salesdb1-instance.cbkw6ke2kh9f.ap-southeast-2.rds.amazonaws.com:5432/salesdb`.

## Deployment Steps

### Backend (Elastic Beanstalk)
1. **Initialize EB:**
   ```bash
   eb init sales-demo-api -p python-3.9 -r ap-southeast-2
   ```
2. **Create Environment:**
   ```bash
   eb create sales-demo-env
   ```
3. **Set Environment Variables:**
   ```bash
   eb setenv RDS_USERNAME=admin RDS_PASSWORD=<your-password> RDS_HOSTNAME=salesdb1-instance.cbkw6ke2kh9f.ap-southeast-2.rds.amazonaws.com RDS_PORT=5432 RDS_DB_NAME=salesdb SECRET_KEY=<your-secret-key>
   ```
4. **Deploy:**
   ```bash
   eb deploy
   ```
   - URL: `http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com`.
   - Check health: `eb status` (expect `Health: Green`).

### Frontend (Static Hosting)
1. **Build:**
   ```bash
   npm run build
   ```
2. **Deploy:**
   - Upload `dist/` to a static host (e.g., AWS S3, Netlify).
   - Example (S3):
     ```bash
     aws s3 sync dist/ s3://your-bucket-name --acl public-read
     ```
   - URL: `https://your-bucket-name.s3.ap-southeast-2.amazonaws.com/index.html` (adjust based on hosting).

## Architectural Choices
- **Backend:**
  - **Flask:** Lightweight, easy to set up for RESTful APIs.
  - **Elastic Beanstalk:** Managed service for deployment, includes load balancing.
  - **RDS PostgreSQL:** Relational DB for structured sales data.
- **Frontend:**
  - **Vue.js:** Reactive UI for dashboard, form, and chart.
  - **Hardcoded URL:** Simplifies config for this demo (vs. `config.json`).
- **Authentication:** JWT for stateless, secure API access.

## Trade-offs
- **Hardcoded URLs:** Quick to implement but less flexible for environment switching (e.g., local vs. prod).
- **No Caching:** Simplifies initial setup but may impact performance with high traffic.
- **Single Instance:** EB default—scales with config but not optimized yet.

## Assumptions
- **User Auth:** Simple username/password check (e.g., `user:pass`) for demo; no user table in DB.
- **Frontend Hosting:** Assumes static hosting separate from EB (not served by Flask).
- **Token Longevity:** JWT tokens don’t expire in this demo—production would need expiration/refresh.

## Known Limitations
- **Frontend Refresh:** Initial issue with sales not displaying (fixed—[describe your fix, e.g., "used `$set` for reactivity"]).
- **Scalability:** No auto-scaling or caching implemented yet—see below.
- **Error Handling:** Basic in frontend; backend could expand validation (e.g., date format).

## Scalability & Performance Plan
- **Auto-Scaling:**
  - Configure EB auto-scaling:
    ```yaml
    # .ebextensions/autoscaling.config
    option_settings:
      aws:autoscaling:asg:
        MinSize: 1
        MaxSize: 4
      aws:autoscaling:trigger:
        MeasureName: CPUUtilization
        UpperThreshold: 70
    ```
  - Adds instances as CPU load increases.
- **Load Balancing:** EB’s Application Load Balancer distributes traffic.
- **Caching:** Future—add AWS ElastiCache (Redis) to cache `GET /sales` results.
- **Database:** RDS can scale vertically (larger instance) or use read replicas.

## Troubleshooting
- **Logs:** `eb logs`—check `web.stdout.log` for backend errors.
- **Display Issue:** Fixed by ensuring Vue reactivity (e.g., `$set` or array spread).
- **RDS Connection:** Verify `eb printenv` matches RDS credentials.

---
```

---

### Notes for You
- **Your Fix:** You said “I found the error”—what was it? Add it under “Known Limitations” or “Troubleshooting” (e.g., “Reactivity fixed with `$set`” or “Backend delay needed 500ms timeout”).
- **Frontend Hosting:** I assumed static hosting (e.g., S3)—update the “Deploy” section if you used something else (e.g., Netlify URL).
- **Scalability:** The plan is basic—expand if you’ve implemented more (e.g., caching).

---

### Steps to Finalize
1. **Copy this README:** Save as `README.md` in your repo root.
2. **Customize:**
   - Add your fix details.
   - Update frontend deployment URL.
   - Adjust any `app.py` specifics if different (e.g., extra endpoints).
3. **Commit & Push:**
   ```bash
   git add README.md
   git commit -m "Add README for exercise"
   git push
   ```
4. **Redeploy (if needed):**
   ```bash
   eb deploy
   npm run build
   # Upload dist/ to hosting
   ```

