import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Business Intelligence Dashboard",
    layout="wide"
)


# Load datasets

customer = pd.read_csv("data/customer_churn.csv")
traffic = pd.read_csv("data/web_traffic.csv")
regional = pd.read_csv("data/regional_market.csv")
checkout = pd.read_csv("data/checkout_ab_test.csv")


st.title("📊 Interactive Business Intelligence Dashboard")


# Sidebar Menu

page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Overview",
        "Customer Churn",
        "Web Traffic",
        "Regional Market",
        "Checkout A/B Test"
    ]
)


# ---------------- Overview ----------------

if page == "Overview":

    st.header("Business Overview")

    customer["TotalChargesINR"] = pd.to_numeric(
        customer["TotalChargesINR"],
        errors="coerce"
    )

    customer["MonthlyChargesINR"] = pd.to_numeric(
        customer["MonthlyChargesINR"],
        errors="coerce"
    )


    total_users = customer["CustomerID"].nunique()

    revenue = customer["TotalChargesINR"].sum()

    churn = (
        (customer["Churn"] == "Yes").mean() * 100
    )

    avg_ticket = customer["MonthlyChargesINR"].mean()


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Users",
        total_users
    )


    col2.metric(
        "Revenue",
        f"₹ {revenue:,.0f}"
    )


    col3.metric(
        "Churn %",
        f"{churn:.2f}%"
    )


    col4.metric(
        "Average Ticket",
        f"₹ {avg_ticket:.0f}"
    )


    fig = px.pie(
        customer,
        names="Churn",
        title="Customer Churn"
    )

    st.plotly_chart(fig)



# ---------------- Customer Churn ----------------


elif page == "Customer Churn":

    st.header("Customer Churn Analysis")


    region = st.sidebar.multiselect(
        "Select Region",
        customer["Region"].unique(),
        customer["Region"].unique()
    )


    df = customer[
        customer["Region"].isin(region)
    ]


    fig = px.bar(
        df,
        x="Region",
        y="TotalChargesINR",
        title="Revenue by Region"
    )

    st.plotly_chart(fig)


    fig2 = px.histogram(
        df,
        x="SubscriptionType",
        color="Churn",
        title="Subscription vs Churn"
    )

    st.plotly_chart(fig2)



# ---------------- Web Traffic ----------------


elif page == "Web Traffic":

    st.header("Website Analytics")


    fig = px.bar(
        traffic,
        x="Source",
        title="Traffic Source"
    )

    st.plotly_chart(fig)



# ---------------- Regional Market ----------------


elif page == "Regional Market":

    st.header("Regional Market Analysis")


    fig = px.scatter(
        regional,
        x="EstimatedAcquisitionCostINR",
        y="LeadConversionRate",
        size="MonthlySearchDemand",
        hover_name="City"
    )

    st.plotly_chart(fig)



# ---------------- A/B Test ----------------


elif page == "Checkout A/B Test":

    st.header("Checkout Experiment")


    result = (
        checkout.groupby("Variant")["Converted"]
        .apply(lambda x: (x=="Yes").mean()*100)
        .reset_index()
    )


    fig = px.bar(
        result,
        x="Variant",
        y="Converted",
        title="Conversion Rate"
    )

    st.plotly_chart(fig)