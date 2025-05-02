import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Set page config
st.set_page_config(page_title="Simple Market Analysis", layout="centered")
engine = create_engine('postgresql+psycopg2://postgres.pwzqpxyqjewxibyfabhr:zGp7PKRkPmL1IhIX\
@aws-0-eu-central-1.pooler.supabase.com/postgres')
# Load data
@st.cache_data
def load_data():
    df = pd.read_sql_table('companies', engine)
    df_history = pd.read_sql_table('market_history', engine)
    df_history['date'] = pd.to_datetime(df_history['date'], errors='coerce')
    return df, df_history

df, df_history = load_data()

# Simple filter
st.sidebar.header("Quick Filter")
selected_industry = st.sidebar.selectbox(
    "Filter by industry:", 
    ['All'] + list(df['industry_labels'].unique())
)

if selected_industry != 'All':
    filtered_df = df[df['industry_labels'] == selected_industry]
    st.sidebar.write(f"Showing {len(filtered_df)} companies in {selected_industry}")
else:
    filtered_df = df
    st.sidebar.write(f"Showing all {len(df)} companies")

# Title
st.title("Simple Market Analysis")
st.write("Explore company financial data and market trends")

# Main analysis
st.header("1. Market Overview")
st.dataframe(df.describe())

# Industry distribution
st.subheader("Companies by Industry")
industry_count = df['industry_labels'].value_counts()
fig1 = px.bar(industry_count, title="Number of Companies per Industry")
st.plotly_chart(fig1)

# Market cap analysis
st.header("I. Market Cap Analysis")
fig2 = px.box(df, x='industry_labels', y='market cap in Million', 
             title="Market Cap by Industry")
fig2.update_yaxes(type = 'log')
st.plotly_chart(fig2)

# Top companies
st.subheader("Top 10 Companies by Market Cap")
top_companies = df.nlargest(10, 'market cap in Million')
fig3 = px.bar(top_companies, x='name', y='market cap in Million', 
             color='industry_labels', title="Market Cap Leaders")
st.plotly_chart(fig3)


# Average Closing per Indusrty
st.header("2. Industry Overview")

# Market cap analysis
st.header("I. Market Cap Analysis")
fig2 = px.box(filtered_df, x='industry_labels', y='market cap in Million', 
             title="Market Distribution")
st.plotly_chart(fig2)
fig8 = px.violin(filtered_df, x='industry_labels', y='market cap in Million', 
             title="Market Distribution")
st.plotly_chart(fig8)
fig12 = px.bar(filtered_df, x='name', y='market cap in Million', 
             color='industry_labels', title="Market Distribution")
st.plotly_chart(fig12,key="unique2")

# Top companies
st.subheader("Top 10 Companies by Market Cap")
top_companies = filtered_df.nlargest(10, 'market cap in Million')
fig7 = px.bar(top_companies, x='name', y='market cap in Million', 
             color='industry_labels', title="Market Cap Leaders")
st.plotly_chart(fig7,key="unique")


# Revenue analysis
st.header("II. Revenue Analysis")
fig22 = px.box(filtered_df, x='industry_labels', y='revenue in Million', 
             title="Revenue Distribution")
st.plotly_chart(fig22)
fig82 = px.violin(filtered_df, x='industry_labels', y='revenue in Million', 
             title="Revenue Distribution")
st.plotly_chart(fig82)
fig122 = px.bar(filtered_df, x='name', y='revenue in Million', 
             color='industry_labels', title="Revenue Distribution")
st.plotly_chart(fig122,key="unique22")

# Top companies
st.subheader("Top 10 Companies by Revenue")
top_companies2 = filtered_df.nlargest(10, 'revenue in Million')
fig72 = px.bar(top_companies2, x='name', y='revenue in Million', 
             color='industry_labels', title='revenue in Million')
st.plotly_chart(fig72,key="unique12")

st.header("III. Industry Performance Analysis")
indusrty_data = df_history[df_history['symbol'].isin(filtered_df['symbol'])]
average_per_day = indusrty_data.groupby(by='date').agg(closing = ("close",'mean'))
if not average_per_day.empty:
    fig5 = px.line(average_per_day, x=average_per_day.index, y='closing', 
                  title=f"Average Closing Price for {selected_industry}")
    st.plotly_chart(fig5)
else:
    st.warning("No price data available for this industry")

# Price history
st.header("3. Price History Explorer")
selected_company = st.selectbox("Select a company:", df['symbol'].unique())

company_data = df_history[df_history['symbol'] == selected_company]
if not company_data.empty:
    fig4 = px.line(company_data, x='date', y='close', 
                  title=f"Closing Price for {selected_company}")
    st.plotly_chart(fig4)
else:
    st.warning("No price data available for this company")


