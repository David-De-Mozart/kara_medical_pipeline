# Kara Medical Pipeline: End-to-End Data Product for Ethiopian Medical Businesses

---

## Project Overview

This project delivers a robust **end-to-end data pipeline** that extracts, processes, enriches, and serves data scraped from public Telegram channels related to Ethiopian medical businesses.

Built as part of a data engineering challenge at Kara Solutions, the pipeline leverages modern technologies including:

- **Telegram API** via Telethon for data extraction
- **PostgreSQL** for data warehousing
- **dbt (Data Build Tool)** for ELT transformations and dimensional modeling
- **YOLOv8** for object detection on scraped images, enriching the dataset
- **FastAPI** to expose an analytical API answering business questions
- **Dagster** to orchestrate the entire workflow in a scalable, observable manner
- **Docker & Docker Compose** for containerization and environment reproducibility

---

## Business Problem

How can we provide actionable insights on medical products and their availability across Ethiopian Telegram channels? This pipeline answers questions like:

- What are the top 10 most frequently mentioned medical products or drugs?
- How do prices or availability vary across channels?
- Which channels share the most visual content (e.g., images of pills vs creams)?
- What are the posting trends over time for health-related topics?

---

## Features

- **Automated Telegram data scraping** with error handling and logging
- **Raw data lake** organized by date and channel for easy incremental processing
- **Star schema data warehouse** built using dbt to enable fast, reliable analytics
- **Image enrichment** with YOLOv8 object detection, linked to messages
- **RESTful API** serving analytical endpoints tailored to business needs
- **Dagster orchestrated pipeline** for scheduling and monitoring ETL/ELT jobs
- **Containerized environment** for seamless deployment and reproducibility

---

## Project Structure
kara_medical_pipeline/
├── api/ # FastAPI application modules
│ ├── main.py
│ ├── crud.py
│ ├── database.py
│ ├── models.py
│ └── schemas.py
├── data/ # Raw Telegram data JSON files
│ └── raw/
├── dbt_project/ # dbt project files & models
├── images/ # Scraped images for YOLO detection
├── docker-compose.yml
├── Dockerfile
├── dagster_pipeline.py # Dagster job definitions and orchestration
├── requirements.txt
├── .env.example # Environment variables template (no secrets)
├── screenshots/ # Screenshots demonstrating functionality
└── README.md # This file


---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Telegram API credentials (API ID & Hash)
- PostgreSQL credentials

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/David-De-Mozart/kara_medical_pipeline.git
   cd kara_medical_pipeline

2. **Create .env file:**

    Copy .env.example to .env and fill in your credentials:
    cp .env.example .env

3. **Build and start containers:**

    docker-compose up --build

4. **Run the Dagster UI to orchestrate pipeline:**

    dagster dev
    Access Dagster UI at http://localhost:3000

5. **Access FastAPI docs:**
    Once the API is running (typically on port 8000), visit:
    http://localhost:8000/docs
    

**How to Use**

- Scrape Telegram data: Trigger scraping to populate the raw data lake.

- Load raw data to PostgreSQL: Raw JSON files are loaded into a raw schema.

- Run dbt transformations: Transform raw data into star schema models.

- Run YOLO object detection: Enrich image data with detected objects.

- Query the API: Use REST endpoints to answer key business questions.

- Orchestrate with Dagster: Schedule and monitor all pipeline steps.


**Key Endpoints**

***Endpoint***	                                ***Description***

/api/reports/top-products?limit=10     	Top 10 most frequently mentioned products
/api/channels/{channel_name}/activity	Posting activity trends for a channel
/api/search/messages?query=paracetamol	Search messages containing keyword

**Technologies Used**

- Python 3.11

- Telethon (Telegram API client)

- PostgreSQL

- dbt

- Ultralytics YOLOv8

- FastAPI

- Dagster

- Docker & Docker Compose


**License**

This project is licensed under the MIT License.

Thank you for exploring this project!