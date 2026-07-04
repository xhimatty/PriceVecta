# PriceVecta

### You give us the targets. We deliver the data.

## Description
PriceVecta is a custom price monitoring platform that automates price collection from client-specified e-commerce, retail, and distributor websites. It continuously tracks product prices, stores historical records, and notifies users whenever pricing changes occur.

<img width="2736" height="1562" alt="Screenshot 2026-06-28 015828" src="https://github.com/user-attachments/assets/41f24274-de3d-4221-ab8d-08b33aca0de8" />


PriceVecta eliminates manual data collection by combining automated web scraping with a web dashboard, historical analytics, CSV exports, and real-time alerts to provide businesses with actionable market insights, real-time competitive advantages, and data-driven pricing decisions.

## Key Features
- **Custom Automated Extraction:** Continuous price and stock monitoring across client-specified e-commerce, retail, and distributor websites.
- **Visual Intelligence Dashboard:** A clean, responsive interface viewing tracked products, current prices, and key monitoring metrics. 
- **Historical Data Analytics:** Automatically stores pricing history and allows historical data to be exported as CSV for reporting, trend analysis, and business intelligence.
- **Instant Alerting Engine:** Real-time Telegram and Email notifications immediately price changes are detected, including the previous price, current price, and product link.
- **Scalable Data Pipeline:** Built with Scrapy, Flask, SQLAlchemy, and Docker to support reliable, automated monitoring workflows.
- **Cloud-Based Scheduling:** Automated scraping jobs deployed on Google Cloud Compute Engine using Linux cron jobs.

### Target Audience
**PriceVecta is engineered to power data-driven decisions for:**
- E-Commerce Businesses & Retailers: Dynamically optimize repricing strategies.
- Procurement Teams & Distributors: Monitor vendor compliance and identify cost-saving opportunities.
- Market Researchers & Competitive Intelligence Teams: Track long-term market trends and competitor behaviors.

## System Architecture & Tech Stack
PriceVecta is split into four core layers: Extraction, Storage, dashboard, and Infrastructure.

<img width="1280" height="698" alt="WhatsApp Image 2026-07-03 at 11 50 48 AM" src="https://github.com/user-attachments/assets/4b9d939e-d320-4f75-b13c-4422d731acf4" />


## Dashboard
The dashboard provides a centralized view of monitored products, including:

* Total products tracked
* Highest recorded price
* Lowest recorded price
* Last update timestamp

Each product links directly to its historical pricing page, where users can review previous prices and export the data as a CSV file.

## Price Change Detection
Whenever a scraper runs, newly collected prices are compared against the latest stored values.

If a change is detected, PriceVecta automatically:
* Records the new price
* Stores the previous price history
* Updates the dashboard
* Sends Telegram notifications
* Sends email alerts

Each notification includes:
* Product name
* Previous price
* Current price
* Product URL

## Technology Stack
### Backend
* Python
* Flask
* Scrapy
* SQLAlchemy

### Database
* SQLite

### Data Processing
* Pandas

### Notifications
* Telegram Bot API
* Email

### Infrastructure & Deployment
* Docker
* Google Cloud Compute Engine
* Linux Cron Jobs

### Technical Challenges & Engineering Resilience 
- **Adaptive Target Structural Failovers:** E-commerce architectures frequently undergo layout updates and minor frontend revisions that can disrupt brittle parsing logic. To prevent pipeline downtime, the extraction engine utilises a defensive multi-layered data extraction strategy, prioritising semantic structural metadata and falling back gracefully to contextual arrays.
 
- **Pipeline Longevity & Network Optimisation:** Web data acquisition at production scale requires strict compliance with remote server stability. The pipeline enforces request throttling, organic delay distributions, and custom profiling to mimic standard user agents. This ensures the scraping engine remains low-impact, respects target bandwidth limits, and avoids triggering automated rate-limiting flags.


### Highlights

* Automated price monitoring
* Historical pricing database
* Real-time alerts
* CSV exports
* Dashboard reporting
* Client-specific monitoring targets
* Containerized deployment
* Cloud-based scheduled execution

### Production Roadmap
- Migration from SQLite to a highly available PostgreSQL instance on GCP Cloud SQL.
- Integration of advanced browser-automation fallback layers for heavy JavaScript-rendered single-page applications.
- Implementation of a visual configuration wizard allowing users to add custom targets directly from the UI.
