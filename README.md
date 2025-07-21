# HealthKart Influencer ROI

This project provides a simulated dashboard for tracking and visualizing the **ROI of influencer campaigns** for **HealthKart**, built using **Python**, **pandas** for data handling, and **Dash** for the interactive web application. It's designed to be run within a **Jupyter Notebook environment** and can be accessed from other devices on your network.

## Context

HealthKart manages influencer campaigns across various social platforms to promote products from brands like **MuscleBlaze**, **HKVitals**, and **Gritzo**. Influencers are compensated either **per post** or **per order**. This dashboard offers insights into:

- Campaign performance  
- Incremental ROAS  
- Influencer effectiveness  
- Payout tracking

## Objective

To build an open-source tool/dashboard that can **track and visualize ROI** of influencer campaigns effectively.

## Features

### Data Simulation

Generates mock datasets for:

- **Influencers**: `ID`, `name`, `category`, `gender`, `follower count`, `platform`
- **Posts**: `influencer_id`, `platform`, `date`, `URL`, `caption`, `reach`, `likes`, `comments`
- **Tracking Data**: `source`, `campaign`, `influencer_id`, `user_id`, `product`, `brand`, `date`, `orders`, `revenue`
- **Payouts**: `influencer_id`, `basis` (`post`/`order`), `rate`, `orders`, `total_payout`

### Campaign Performance Tracking

Displays key metrics:

- Total Revenue  
- Total Orders  
- Total Payout  
- ROAS  
- Incremental ROAS

### Visualizations

- **Revenue Over Time** (Line Chart)  
- **Revenue by Platform** (Bar Chart)  
- **Revenue by Campaign** (Bar Chart)  

### Filtering

Dynamic filtering by:

- Brand  
- Product  
- Influencer Category  
- Platform  

### Influencer Insights

Identifies:

- Top 5 Influencers by Revenue  
- Top 5 Influencers by ROAS  
- Best Performing Personas by Avg. ROAS  
- Poor ROIs (ROAS < 1)

### Payout Tracking

Detailed payout tables per influencer.

### Export Functionality

Exports currently filtered data into a `.zip` file with CSVs of:

- Influencers  
- Posts  
- Tracking Data  
- Payouts  

## Assumptions

- **Data Source**: Simulated in-memory; in production, replace with real data ingestion.
- **Incremental ROAS**: Assumes 70% of revenue is incremental.
- **Payout Filtering**: Filtered based on matching influencer tracking.
- **Primary Platform**: Only one listed per influencer.
- **No External Database**: All data lives within the session.
- **UI/UX**: Uses **Dash** components with **Tailwind CSS** and **Font Awesome** for responsiveness and styling.

## Setup and Running in Jupyter Notebook

### Install Dependencies

pip install pandas dash plotly

## Launch the Dashboard

### Using Jupyter Notebook

1. Open **Jupyter Notebook** or **JupyterLab**.
2. Create a new **Python 3** notebook.
3. Copy the entire Python code.
4. Paste it into a cell and run it using `Shift + Enter`.

## Access the Dashboard

### Local Access
- Visit: [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

## Screenshots
<img width="487" height="415" alt="image" src="https://github.com/user-attachments/assets/1c562165-bfdf-40d5-b319-78899f11429e" />
<img width="473" height="383" alt="image" src="https://github.com/user-attachments/assets/a27fb266-6c45-4706-9aff-58c4c3f2736a" />
<img width="456" height="427" alt="image" src="https://github.com/user-attachments/assets/11621886-6a9a-4695-b2ae-907ed886afe8" />
<img width="473" height="321" alt="image" src="https://github.com/user-attachments/assets/0b06206d-2b73-4acb-a6f4-80912abe178d" />

