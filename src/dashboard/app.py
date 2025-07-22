# streatmlit dashboard for matchaai forecasts
import sys
import streamlit as st
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pandas as pd
from src.nlp_models.trend_analysis import load_social_data, get_trending_drinks, get_sentiment_summary
import plotly.express as px
from src.ml_models.recommender import recommend_drinks, get_customer_taste_profile, recommend_drinks_based_on_taste 

# title 
st.title("🍵 MatchaAI: Business Intelligence Dashboard")

# tabs
tab1, tab2, tab3 = st.tabs(["Sales Forecast", "Drink Recommendation", "Social Media Trend"])

# ==========
# TAB 1 : sales forecast tab section
# ==========
with tab1:
    st.header("Sales Forecasting")
    # loading forecast data
    # forecast_df = pd.read_csv("data/forecast_results.csv")
    forecast_df = pd.read_csv("data/forecast_results.csv")
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
    
    # sidebar: forcasting period
    st.sidebar.header("Forecasting Sales Period")

    # sidebar : selecting drink type
    drink_types = forecast_df["Drink"].unique()
    selected_drink = st.sidebar.selectbox("Select Matcha Drink:", drink_types)

    # side bar : date range filter
    min_date = pd.to_datetime(forecast_df['ds']).min()
    max_date = pd.to_datetime(forecast_df['ds']).max()
    selected_dates = st.sidebar.date_input(
        "Select Date Range:",
        value=[min_date, max_date],
        key="date_range"
    )

    # convert selected_dates to pd timestamps
    if isinstance(selected_dates, (list, tuple)):
        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])
    else:
        start_date = pd.to_datetime(selected_dates)
        end_date = pd.to_datetime(selected_dates)

    # filtering data 
    mask = (forecast_df['ds'] >= start_date) & (forecast_df['ds'] <= end_date)
    filtered_df = forecast_df[mask & (forecast_df['Drink'] == selected_drink)]

    # using start_date and end_date for comparison chart
    comparison_df = forecast_df[(forecast_df['ds'] >= start_date) & (forecast_df['ds'] <= end_date)]

    # line chart : actual vs forecasted
    fig = px.line(
        filtered_df, 
        x='ds', y='yhat',
        title=f"{selected_drink} Sales Forecast",
        labels={'ds': 'Date', 'yhat': 'Predicted Sales'},
        line_shape='spline'
    )

    st.plotly_chart(fig)

    # kpis
    total_sales = filtered_df['yhat'].sum()
    avg_daily_sales = filtered_df['yhat'].mean()
    st.metric("Total Predicted Sales", f"{total_sales:.0f} units")
    st.metric(" Avg Daily Sales", f"{avg_daily_sales:.1f} units/day")

    # calculating % change in sales over forecasted periods
    first_day = filtered_df['yhat'].iloc[0]
    last_day = filtered_df['yhat'].iloc[-1]
    growth_rate = ((last_day - first_day) / first_day) * 100

    # smart recommendations
    st.subheader("Smart Recommendations")

    # generating recommendation
    if growth_rate > 10:
        recommendation = f"📈 {selected_drink} is predicted to grow by {growth_rate:.1f}%. Consider increasing stock or promoting this drink."
    elif growth_rate < -10:
        recommendation = f"📉 {selected_drink} is predicted to decline by {abs(growth_rate):.1f}%. Consider reducing stock or creating a special deal."
    else:
        recommendation = f"➡️ {selected_drink} sales are stable. Maintain current stock levels."

    # displaying recommendation
    st.info(recommendation)

    # comparison chart for all drinks
    st.subheader("Sales Forecast Comparison (All Drinks)")
    comparison_df = forecast_df[(forecast_df['ds'] >= pd.Timestamp(selected_dates[0])) & 
                                (forecast_df['ds'] <= pd.Timestamp(selected_dates[1]))]
    fig2 = px.line(
        comparison_df, 
        x='ds', y='yhat', color='Drink',
        labels={'ds': 'Date', 'yhat': 'Predicted Sales'},
        line_shape='spline'
    )
    st.plotly_chart(fig2)

    # displaying and downloading filtered forecast data 
    if st.button("Download Forecast Data as CSV"):
        filtered_df.to_csv("filtered_forecast.csv", index=False)
        st.success(" Download complete!")

# ==========
# TAB 2 : drink recommendation tab section
# ==========
with tab2:
    st.header("Drink Recommendation")

    # creating sub-tabs
    rec_tab, filter_tab = st.tabs(["View Recommendations", "Filter Preferences"])

    # -------------------------------
    # Sub-Tab 1: Personalized Recommendations
    # -------------------------------
    with rec_tab:
        st.subheader("AI-Powered Personalized Recommendations")

        customer_df = pd.read_csv("data/customer_orders.csv")
        customer_ids = customer_df["CustomerID"].unique()
        selected_customer = st.selectbox("Select Customer:", customer_ids)

        # Get AI-based recommendations
        recommended_drinks = recommend_drinks(selected_customer, customer_df)

        # Display them
        st.subheader(f" Recommendations for Customer {selected_customer}")
        for drink in recommended_drinks:
            st.write(f"✅ {drink}")

        # Show customer taste profile
        taste_profile = get_customer_taste_profile(
            selected_customer,
            "data/customer_orders.csv",
            "data/drink_profiles.csv"
        )

        st.subheader(f"Taste Profile for Customer {selected_customer}")
        st.write("**Favorite Flavors:**", taste_profile["flavor"])

        st.header("Tailored Drink Recommendations")
        recommended_df = recommend_drinks_based_on_taste(
            taste_profile,
            "data/drink_profiles.csv"
        )

        if not recommended_df.empty:
            for _, row in recommended_df.iterrows():
                st.markdown(f"✅ **{row['Drink']}**")
                st.write(f" - **Flavor**: {row['Flavor']}")
                st.write(f" - **Caffeine Level**: {row['Caffeine']}")
                st.write(f" - **Sweetness**: {row['Sweetness']}")
                st.write(f" - **Season**: {row['Season']}")
                st.write(f" - **Trending**: {'🔥 Yes' if row['Trending'] else 'No'}")
                st.markdown("---")
        else:
            st.warning("No matching drinks found for this customer.")

    # -------------------------------
    # Sub-Tab 2: Filter Preferences
    # -------------------------------
    with filter_tab:
        st.subheader("Filter Drinks by Preferences")

        # Load drinks
        drink_profiles = pd.read_csv("data/drink_profiles.csv")

        # Filter options
        selected_flavors = st.multiselect(
            "Choose Preferred Flavors:",
            options=drink_profiles["Flavor"].unique().tolist(),
            default=drink_profiles["Flavor"].unique().tolist()
        )
        selected_sweetness = st.selectbox(
            "Preferred Sweetness Level:",
            options=["Low", "Medium", "High"]
        )
        selected_milk = st.radio(
            "Milk Preference:",
            options=["Yes", "No"]
        )

        # calculating match score for all drinks
        def calculate_match_score(drink, taste_profile):
            score = 0
            total = 4  # Total preference categories

            if drink["Flavor"] in selected_flavors:
                score += 1
            if drink["Sweetness"] == selected_sweetness:
                score += 1
            if drink["Milk"] == selected_milk:
                score += 1
            return int((score / total) * 100)

        # adding match schore to filter drinks
        drink_profiles["MatchScore"] = drink_profiles.apply(
            lambda row: calculate_match_score(row, taste_profile), axis=1)
        sorted_drinks = drink_profiles.sort_values(by="MatchScore", ascending=False)

        # match score slider
        match_threshold = st.slider(
            "Set Match Score Threshold (%)",
            min_value=50,
            max_value=100,
            value=70
        )

        # filter drinks based on threshold
        high_match_drinks = drink_profiles[drink_profiles["MatchScore"]>= match_threshold]

        # display drinks
        if not high_match_drinks.empty:
            st.subheader(f"🥤 Drinks Matching {match_threshold}%+ for Customer {selected_customer}")

        for _, row in high_match_drinks.iterrows():
                st.markdown(f"✅ **{row['Drink']}**")
                match_score = row["MatchScore"]
                # progress bar with color
                if match_score >= 80:
                    bar_color = "green"
                elif match_score >= 60:
                    bar_color = "yellow"
                else:
                    bar_color = "red"

                st.progress(match_score / 100, text=f"Match Score: {match_score}%")  

                st.write(f" - **Flavor**: {row['Flavor']}")
                st.write(f" - **Caffeine Level**: {row['Caffeine']}")
                st.write(f" - **Sweetness**: {row['Sweetness']}")
                st.write(f" - **Milk**: {row['Milk']}")
                st.write("---")

# ==========
# TAB 3 : social media trend analysis tab section
# ==========
with tab3:
    st.header("Social Media Trend Analysis")

    # loading social posts
    social_df = load_social_data("data/social_posts.csv")

    # trending drinks
    trending = get_trending_drinks(social_df)
    trending_df = pd.DataFrame(list(trending.items()), columns=["Drink", "Mentions"])

    # bar chart of trending drinks
    fig3 = px.bar(
        trending_df, 
        x="Drink", y="Mentions", 
        title="Trending Drinks on Social Media",
        labels={"Mentions": "Number of Mentions"},
        color="Mentions",
        color_continuous_scale="greens"
    )
    st.plotly_chart(fig3)

    # sentiment analysis
    st.subheader("Social Media Sentiment Analysis")

    # analyze sentiment
    sentiment = get_sentiment_summary(social_df)
    sentiment_df = pd.DataFrame(list(sentiment.items()), columns=["Sentiment", "Count"])

    # pie chart of sentiment
    fig4 = px.pie(
        sentiment_df, 
        names="Sentiment", values="Count",
        title="Sentiment Breakdown of Social Media Posts",
        color_discrete_map={"Positive": "lightgreen", "Negative": "salmon", "Neutral": "lightgray"}
    )
    st.plotly_chart(fig4)


