# PriceVecta

### You give us the targets. We deliver the data.

## Description
PriceVecta is a custom price monitoring platform that automates price collection from client-specified e-commerce, retail, and distributor websites. It continuously tracks product prices, stores historical records, and notifies users whenever pricing changes occur.

PriceVecta eliminates manual data collection by combining automated web scraping with a web dashboard, historical analytics, CSV exports, and real-time alerts to provide businesses with actionable market insights, real-time competitive advantages, and data-driven pricing decisions.

## Key Features
- **Custom Automated Extraction:** Continuous price and stock monitoring across client-specified e-commerce, retail, and distributor websites.
- **Visual Intelligence Dashboard:** A clean, responsive interface viewing tracked products, current prices, and key monitoring metrics. 
- **Historical Data Analytics:** Automatically stores pricing history and allows historical data to be exported as CSV for reporting, trend analysis, and business intelligence.
- **Instant Alerting Engine:** Real-time Telegram and Email notifications immediately price changes are detected, including the previous price, current price, and product link.

## System Architecture & Tech Stack
PriceVecta is split into four core layers: Extraction, Storage, dashboard, and Infrastructure.

====== put image architecture here =======


============================================

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


