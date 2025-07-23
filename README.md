# 🍵 MatchaAI: Business Intelligence Dashboard for Matcha Startups

MatchaAI is an Ai-powered business intelligence platform designed to help matcha beverage business optimize their sales forecasting, personalized drink recommendations, and social media trend analysis.

This interactive dashboard provides data-driven insights to empower managers and baristas to make smarter business decisions and deliver tailored customer experiences.

## Features
- 🍵 Sales & Inventory Forecasting
  - Predicts future sales trends using machine learning.
  - Highlights top-performing drinks and growth opportunities.
- 🍵 Personalized Drink Recommendation Engine
  - Suggests drinks based on customer order history and taste profiles.
  - Includes interactive filters for flavors, sweetness, and milk preferences.
- 🍵 Social Media Trend Analysis
  - Tracks trending drinks from social platforms for marketing strategies. 
- 🍵 Interactive Business Intelligence Dashboard
  - Built with Streamlit for a clean, intuitive user experiences.

This project demonstrates how aritifical intelligence and machine learning can be applied in real-world business scenario to drive data-infomred decisions.

## Tech Stack
- Python 3.12
- Pandas & Scikit-learn (data processing & ML models)
- Streamlit (dashboard UI)
- Matplotlib/Plotly (visualizations)

## AI Models
- Sales Forecasting: Linear regression model to predict daily sales.
- Drink Recommendations:
  - Rule-based model: Recommends drinsk based on order history & taste profiles.
  - Interactive filters: Lets users customize preferences dynamically.

## Project Structure
<pre>
  matcha-ai-platform/
  ├── data/
  │     ├── customer_order.csv
  │     ├── drink_profiles.csv
  │     ├── forecast_results.csv
  │     ├── Online Retail.xlsx
  │     └── social_posts.csv
  ├── notebook/
  │     └── sales_forecasting_all_drinks.ipynb
  ├── src/
  │     ├── dashboard/
  │     │     └── app.py
  │     ├── ml_models/
  │     │     ├── generate_social_posts.py 
  │     │     └── recommender.py
  │     ├── nlp_models/
  │     │     ├── __init__.py
  │     │     ├── trend_analysis.py
  │     └─ __init__.py
  ├── requirements.txt
  └── README.md
</pre>

## Running the App Locally
If you'd like to run the Matcha AI app on your own machine, follow these steps below: 
1. Clone the Repository
   <pre>
    bash
     
    git clone https://github.com/your-username/matcha-ai-platform.git
    cd matcha-ai-platform
   </pre>
   
2. Create and Activate a Virtual Environment
   <pre>
     bash

     # creating virtual environment
     python-m venv venv

     # activating environment
     # windows
     venv\Scripts\activate
     # macOS/Linux
     source venv/bin/activate
   </pre>
3. Install Dependencies
   <pre>
     bash

     pip install -r requirements.txt
   </pre>
4.  run the Streamlit App
     <pre>
       bash

       streamlit run src/dashboard/app.py
     </pre>
## Example Use Cases
- 📈 Managers: Adjust inventory based on predicted demand.
- 🥤 Baristas: Recommend drinks tailored to each customer.
- 📣 Marketing Teams: Identify trending drinks to promote on social media.
- 🍵 Customer Experience: Offer personalized drink recommendations based on customer history and preferences.
