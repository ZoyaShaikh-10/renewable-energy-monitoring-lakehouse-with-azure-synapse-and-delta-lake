
# Renewable Energy Monitoring Lakehouse with Azure Synapse and Delta Lake


## Overview
The goal of this project is to build a modern lakehouse architecture to process, store, and analyze renewable energy data. The system is designed to ingest data from multiple sources, process it using Azure Synapse Analytics and Delta Lake, and store it in Azure Data Lake Storage

## High-Level Architecture


**Data Sources:** 

- Real-Time Data: Energy consumption and production data ingested via API.
- Batch Data: Historical energy datasets stored in CSV files.

**Data Ingestion:**

-   Azure Blob Storage / ADLS Gen2: Serves as a landing zone for both real-time and batch data before further processing.
  
**Data Storage:**

-   Azure Data Lake Storage Gen2 (ADLS): Stores raw, processed, and data in a structured format for easy access and scalability.

- Delta Lake: Adds transactional reliability to the data stored in ADLS. Supports ACID operations, version control, and time travel for analytical consistency..
  
**Data Processing:**

-   Azure Databricks: Handles real-time and batch data transformations.

**Data Insights**:

-  Azure Synapse Studio: Facilitates creation of data views for ad-hoc analysis and reporting.

**End Users:**

Data scientists, analysts, and decision-makers can access insights via BI tools or dashboards.


![plot](./energy-pipeline-images/Blank diagrame.png)


## Project Workflow

- **Data Sources → ADLS (Raw Zone) :**
    -   Raw data from real-time and batch is ingested into Azure Data Lake Storage Gen2 in the Raw Zone.

    ![plot](./energy-pipeline-images/raw_data_to_adls.png)


-   **Delta Lake (Raw Data Storage):**
    -   Raw data is stored in Delta Lake for reliability, versioning, and easy accessibility.
    ![plot](./energy-pipeline-images/upload-raw-data-to-delta-lake.png)
    ![plot](./energy-pipeline-images/raw-data-to-delta.png)

-   **Processing (Databricks) → Delta Lake (Processed Zone):**

    -   Data is cleaned, transformed, and aggregated in Azure Databricks. Processed data is stored back into Delta Lake in the Processed Zone with optimized partitioning for analytics.
    ![plot](./energy-pipeline-images/upload-processed-data-to-delta-lake.png)
    ![plot](./energy-pipeline-images/processed-data-to-delta-lake.png)

- **Analytics (Synapse Analytics):**

    -   Azure Synapse Analytics connects to the Processed Zone of Delta Lake, enabling SQL-based querying, advanced analytics, and data preparation for reporting.
    ![plot](./energy-pipeline-images/loading-data-into-synapse.png)
    ![plot](./energy-pipeline-images/sample-visual-in-synapse.png)


-   **Visualization (Power BI or Synapse Studio)**
    -   Insights and trends are visualized using Power BI dashboards or quick visualizations in Synapse Studio for decision-making.

This workflow ensures a streamlined approach from data ingestion to actionable insights, leveraging the power of Azure's ecosystem.


