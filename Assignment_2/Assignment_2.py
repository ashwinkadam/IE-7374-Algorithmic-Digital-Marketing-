import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
# import missingno as msno
# from textwrap import wrap
import matplotlib.pyplot as plt
import warnings
import os
warnings.filterwarnings('ignore')
import streamlit as st
# from snowflake.snowpark.session import Session
# from snowflake.snowpark.functions import avg, sum, col,lit
from snowflake.connector import connect

st.set_page_config(page_title='Sprocket Bikes', page_icon=':bike:')


# account = os.environ.get('account')
# user = os.environ.get('user')
# password = os.environ.get('password')
# role = os.environ.get('role')
# warehouse = os.environ.get('warehouse')
# database = os.environ.get('database')
# schema = os.environ.get('schema')



#connection to snowflake
# Define the connection parameters
connection_parameters = {
    "account": "ca60211.us-east4.gcp",
    "user": "PYASHISHMHATRE",
    "password": "!Ashish123",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SPROCKET",
    "schema": "PUBLIC"
}





# connection_parameters = {
#     "account": os.environ.get("SNOWFLAKE_ACCOUNT"),
#     "user": os.environ.get("SNOWFLAKE_USER"),
#     "password": os.environ.get("SNOWFLAKE_PASSWORD"),
#     "role": os.environ.get("SNOWFLAKE_ROLE"),
#     "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
#     "database": os.environ.get("SNOWFLAKE_DATABASE"),
#     "schema": os.environ.get("SNOWFLAKE_SCHEMA")
# }


# SNOWFLAKE_ACCOUNT = "ca60211.us-east4.gcp"
# SNOWFLAKE_USER = "PYASHISHMHATRE"
# SNOWFLAKE_PASSWORD = "!Ashish123"
# SNOWFLAKE_ROLE = "SYSADMIN"
# SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
# SNOWFLAKE_DATABASE = "SPROCKET"
# SNOWFLAKE_SCHEMA = "PUBLIC"



# Define the SQL query to retrieve data from a Snowflake table
query = "SELECT * FROM biketransactions"

# Establish a connection to Snowflake
conn = connect(**connection_parameters)

# Execute the query and retrieve the results as a Pandas DataFrame
transaction_df = pd.read_sql(query, conn)

# Close the connection to Snowflake
conn.close()

#functions
#will return year, month of the trans date
def get_month(x): return dt.datetime(x.year, x.month, 1) 

def split_date(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    return year, month

#object to time
transaction_df['TRANSACTION_DATE'] = pd.to_datetime(transaction_df['TRANSACTION_DATE'])


# st.title("Welcome to my Streamlit app!")

st.markdown("<h1 style='text-align: center; color: white; font-size: 40px; font-family: Arial, sans-serif;'>Cohort Analysis of Sprocket Bikes!</h1>", unsafe_allow_html=True)

with st.expander("About"):
    st.write("This is a simple Streamlit app that demonstrates Cohort analysis on Sprocket Bikes, Sprocket bikes is a hypothetical bike company.",)
    st.write("Cohort analysis is a powerful tool for businesses to understand the behavior of specific groups of customers over time.")
    st.write("We have three types of cohort analysis, Customer Retention, Avg List Price, and Avg Standard Cost as shown below.")
    st.write("We have used Data from [here](https://www.kaggle.com/datasets/archit9406/customer-transaction-dataset) to perform the analysis.")
    st.write("Inspired by [1](https://www.analyticsvidhya.com/blog/2021/06/cohort-analysis-using-python-for-beginners-a-hands-on-tutorial/) and [2](https://github.com/streamlit/example-app-cohort-analysis)")

#######################################Customer Retention#########################################

#TransactionMonth column will keep transaction year , month and force day to 1.
#CohortMonth will very first transaction date done by that customer and similarly will keep transaction year , month and force day to 1.
transaction_df['TransactionMonth'] = transaction_df['TRANSACTION_DATE'].apply(get_month) 
transaction_df['CohortMonth'] = transaction_df.groupby('CUSTOMER_ID')['TransactionMonth'].transform('min')

transcation_year, transaction_month = split_date(transaction_df, 'TransactionMonth')
cohort_year, cohort_month = split_date(transaction_df, 'CohortMonth')

years_diff = transcation_year - cohort_year
months_diff = transaction_month - cohort_month
transaction_df['CohortIndex'] = years_diff * 12 + months_diff  + 1 

# Counting daily active user from each chort
cohort_data = transaction_df.groupby(['CohortMonth', 'CohortIndex'])['CUSTOMER_ID'].apply(pd.Series.nunique).reset_index()

# Assigning column names to the dataframe created above
cohort_counts = cohort_data.pivot(index='CohortMonth',
                                 columns ='CohortIndex',
                                 values = 'CUSTOMER_ID').round(1)

cohort_sizes = cohort_counts.iloc[:,0]
retention = cohort_counts.divide(cohort_sizes, axis=0).round(3)

retention.index = retention.index.strftime('%Y-%m')

st.markdown("<h1 style='font-size:24px;font-weight:bold;'>Monthly Cohorts : Retention Rate in percentage</h1>", unsafe_allow_html=True)

# st.title('Retention Rate in percentage : Monthly Cohorts')

# Create a heatmap
fig, ax = plt.subplots(figsize=(20, 12))
sns.heatmap(retention, annot=True, fmt= '.0%',cmap='YlGnBu', vmin = 0.0 , vmax = 0.6, ax=ax)
ax.set_ylabel('Cohort Month')
ax.set_xlabel('Cohorts')
ax.set_yticklabels(retention.index, rotation='horizontal')

# Show the plot in Streamlit
st.pyplot(fig)


#######################################AVG List Price#########################################
# Create a groupby object and pass the monthly cohort and cohort index as a list
grouping = transaction_df.groupby(['CohortMonth', 'CohortIndex']) 

# Calculate the average of the list price column
cohort_data = grouping['LIST_PRICE'].mean()

# Reset the index of cohort_data before pivot
cohort_data = cohort_data.reset_index()

# Create a pivot 
average_list = cohort_data.pivot(index='CohortMonth',
                                  columns='CohortIndex',
                                  values='LIST_PRICE')

average_list_cost = average_list.round(1)

average_list_cost.index = average_list_cost.index.strftime('%Y-%m')

# Initialize the figure
plt.figure(figsize=(16, 10))

# Adding a title
# plt.title('Average List Price : Monthly Cohorts', fontsize = 14)

# st.title('Average List Price : Monthly Cohorts')

st.markdown("<h1 style='font-size:24px;font-weight:bold;'>Monthly Cohorts : Average List Price</h1>", unsafe_allow_html=True)

# Create a heatmap
fig, ax = plt.subplots(figsize=(16, 12))
sns.heatmap(average_list_cost, annot = True,vmin = 0.0, vmax =20,cmap="nipy_spectral", fmt='g', ax=ax)
ax.set_ylabel('Cohort Month')
ax.set_xlabel('Cohorts')
ax.set_yticklabels(retention.index, rotation='horizontal')

# Show the plot in Streamlit
st.pyplot(fig)



#######################################AVG Standard Cost#########################################

# Create a groupby object and pass the monthly cohort and cohort index as a list
grouping = transaction_df.groupby(['CohortMonth', 'CohortIndex']) 

# Calculate the standard  average cost of the standard_cost column
cohort_data = grouping['STANDARD_COST'].mean()

# Reset the index of cohort_data before pivot
cohort_data = cohort_data.reset_index()

# Create a pivot 
average_order = cohort_data.pivot(index='CohortMonth',
                                  columns='CohortIndex',
                                  values='STANDARD_COST')

average_standard_cost = average_order.round(1)

average_standard_cost.index = average_standard_cost.index.strftime('%Y-%m')

# st.title('Average Standard Cost : Monthly Cohorts')

st.markdown("<h1 style='font-size:24px;font-weight:bold;'>Monthly Cohorts : Average Standard Cost</h1>", unsafe_allow_html=True)

# Create a heatmap
fig, ax = plt.subplots(figsize=(16, 12))
sns.heatmap(average_standard_cost, annot = True,vmin = 0.0, vmax =20,cmap="YlGnBu", fmt='g', ax=ax)
ax.set_ylabel('Cohort Month')
ax.set_xlabel('Cohorts')
ax.set_yticklabels(retention.index, rotation='horizontal')

# Show the plot in Streamlit
st.pyplot(fig)
