import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 

st.set_page_config(layout="wide")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('KPMG - Sprocket Data analysis')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Ashish Mhatre](https://www.linkedin.com/in/ashishmhatre927/) and [Ashwin Kadam](https://www.linkedin.com/in/ashwinkadam07/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Hello there! we are Group 5 and we are presenting our analysis on the KPMG - Sprocket dataset.")
    st.markdown("This dataset is about a bicycle retail company and provides valuable insights into the company's operations and performance. Our goal is to perform a general data analysis and present some key findings that can be utilized to make strategic marketing decisions to attract new potential customers. We hope that the insights presented here will give a better understanding of the market and help drive growth for the company. Let's dive into the analysis and explore the potential opportunities that the data presents.")
    

new_cust = pd.read_csv(r"C:\Users\Ashish Mhatre\Desktop\ADM\Assignment 1\cust_clean.csv")
cust_add = pd.read_csv(r"C:\Users\Ashish Mhatre\Desktop\ADM\Assignment 1\custadd_clean.csv")
cust_demo = pd.read_csv(r"C:\Users\Ashish Mhatre\Desktop\ADM\Assignment 1\custdemo_clean.csv")
trans = pd.read_csv(r"C:\Users\Ashish Mhatre\Desktop\ADM\Assignment 1\trans_clean.csv")

trans = trans[trans['order_status'] == 'Approved'].copy()
trans['profit'] = trans['list_price'] - trans['standard_cost']
trans['online_order'] = trans['online_order'].replace({0: 'Offline', 1: 'Online'})

# convert the transaction_date column to a datetime type
trans['transaction_date'] = pd.to_datetime(trans['transaction_date'])

# extract the year and month from the transaction_date column
trans['year'] = trans['transaction_date'].dt.year
trans['month'] = trans['transaction_date'].dt.month

grouped = trans.groupby(['year', 'month', 'online_order'])

aggregated = grouped['profit'].sum().reset_index()
counts = grouped['transaction_id'].count().reset_index()

merged = aggregated.merge(counts, on=['year', 'month', 'online_order'])
merged['YearMonth'] = pd.to_datetime(merged[['year','month']].assign(day=1))

st.markdown("")

st.subheader("Total transactions over year")
st.markdown('**To gain a better understanding of customer buying patterns, we will begin by analyzing the most basic yet essential KPI for any business: total sales or transactions. This analysis will help us to track the spread of sales throughout the year and better plan our production to meet customer demand.**')


fig = px.line(merged, x="YearMonth", y="transaction_id", color='online_order',markers=True, title='No. of Orders by Year and Month, Grouped by Online mode')
# Show the plot
st.plotly_chart(fig)

#########################################################
st.markdown('The transaction data for both online and offline channels were fairly equal during the first half of the year. However, in June, there was a noticeable dip in both transactions. This could be attributed to various reasons such as organizational changes, such as revised pricing, or environmental factors, like the start of the rainy season.')
st.markdown('')
st.markdown('But, in the following two months, July and August, there was a sudden spike in transactions for both channels. This could be due to promotional marketing efforts or discounts on products. This was followed by another dip in sales, but then, in October, there was another surge in transactions, perhaps due to the start of the holiday season. Finally, sales settled back to an average level by the end of the year.')


st.subheader("Total profits over year")
st.markdown('**Gross profit is the amount earned after subtracting the cost of goods sold from total revenue, and it helps to determine whether the company is generating enough revenue to cover its expenses and produce a positive return. Understanding gross profit can also provide insights into pricing strategies, cost management, and overall business efficiency, which can inform decision-making and future planning.**')


fig = px.line(merged, x="YearMonth", y="profit", color='online_order',markers=True, title='Total Profit by Year and Month, Grouped by Order mode')
# Show the plot
st.plotly_chart(fig)

st.markdown("The graph shows the total profit over time, with two lines representing the profit for online orders and offline orders. The x-axis displays the \"Year-Month\" and the y-axis displays the \"profit.\" ")
st.markdown('')

st.markdown("As anticipated, the profits showed a strong correlation with the total transactions. Upon closer examination, it was revealed that the profits from the offline channel of business were higher than those from the online channel. This was especially evident in the month of August where, despite high sales on the online channel, the profits were much lower than those of the offline business. The reason for this disparity can be attributed to a promotion or discount that was being offered on the online channel, which resulted in a lower listing price and, consequently, lower profits. On average, the profit across all months was observed to be $450,000.")

##################################################################
st.subheader("Which products have higher demands ?")
st.markdown("**Understanding the distribution of sales by product is of utmost importance. It provides valuable insights into which products are in high demand and which may not be performing well.**")
st.markdown("**Having this information readily available can help business to stay ahead of its competition.if a particular product is consistently in high demand, a company may choose to invest more resources in its production or marketing or it may be a good idea to discontinue a lower performing product and focus on more profitable products.**")

grouped_brand = trans.groupby(['brand','product_class'])
group_class = grouped_brand['profit'].sum().reset_index()
group_class_trans = grouped_brand['transaction_id'].count().reset_index()
group_class = group_class.merge(group_class_trans, on=['brand','product_class'])
group_class['profit'] = group_class['profit'] / 1000000 

fig = px.bar(group_class, x="brand", y="profit", color="product_class", title="Profit divide by Brand and product class")
st.plotly_chart(fig)

st.markdown("The analysis reveals that WeareA2B, Solex and Trek Bicycles are the top 3 brands in terms of profitability. Meanwhile, Norco Bicycles is the brand that is earning the least profit among all 6 brands. It is worth noting that for each brand, the medium class product is the most successful in terms of sales and profitability. This can be used as a valuable tool for inventory management. to stock medium class products, and avoid overstocking other categories to minimize the risk of dead stock.")

###################################

st.header('Understanding our top 10 customers ')

st.markdown("**Understanding your top customers is crucial for maximizing revenue, building customer loyalty and effectively segmenting your market,   By focusing on your top customers, we can enhance relationships, gather market insights and allocate resources efficiently.**")
grouped_cust_trans = trans.groupby('customer_id')['profit'].sum()
grouped_cust = cust_demo.merge(grouped_cust_trans, on='customer_id').copy()
top10_customer = grouped_cust.sort_values(by='profit', ascending=False ).head(10)
option = st.selectbox(
    '**Break down the customers by ?**',
    ('wealth_segment', 'job_industry_category'))




fig = px.bar(top10_customer, x="first_name", y="profit",
             color=option, barmode='group',
             height=400, title ='Top 10 customer by {}'.format(option))

st.plotly_chart(fig)

st.markdown("This visual representation sheds light on the distribution of our top customers based on their wealth segment. The data reveals that 50% of our top customers fall under the Mass segment, while 30% belong to the High Net Worth category, and the remaining 20% are classified as Affluent customers. This highlights the importance of devising strategies to attract and retain a higher number of Mass customers.")
st.markdown("Furthermore, the data shows that when we analyze the job categories of our top customers, the financial services and manufacturing sectors are equally represented, followed by the retail sector, which accounts for only 20% of the top customers. This information implies that the financial services and manufacturing sectors generate significant profit for our business and should be targeted in our marketing efforts.")
st.markdown("")
st.markdown("but this provides a narrow view of our customer base, specifically focusing on the top 10 customers. However, in order to support our claim that we have a higher volume of business from the financial services and manufacturing sectors, we need to analysis our entire customer population. This will give us a more comprehensive overview of the distribution of our customers across various job categories and provide a more robust basis for our claims.")
###################################################

st.header('Which industries to focus ?')

grouped_industry = grouped_cust.groupby(['job_industry_category'])['profit'].sum().reset_index()
fig = px.pie(grouped_industry, values='profit', names='job_industry_category', title='Breakdown of Profits by Industry')
st.plotly_chart(fig)

st.markdown("The visual presents a detailed analysis of profits generated by various industries. This supports the hypothesis derived from the previous graph, which highlights the importance of focusing on financial services and manufacturing, as these two sectors alone account for 50% of the total profits. Additionally, this chart reveals that the health sector is a significant contributor to the company's revenue, even though it was not present in the top 10 customer analysis. The fact that health sector appears in the cumulative analysis suggests that the company has a large number of medium to low scale customers from this sector, whose combined purchases account for 19% of the total revenue. Other significant contributors to the company's revenue include the retail and property sectors, among others.")
###################################################
st.header('Customer segmentation by wealth')

grouped_wealth = grouped_cust.groupby(['wealth_segment'])['profit'].sum().reset_index()
fig = px.pie(grouped_wealth, values='profit', names='wealth_segment', title='Breakdown of Profits by wealth segment')
st.plotly_chart(fig)

st.markdown("It is evident that the pattern observed in the top 10 customer analysis is reflective of the overall customer base analysis, where mass customers account for 50% of the total profit generated by the business. On the other hand, both high net worth and affluent customers contribute equally with a share of 25% each. This highlights the crucial importance of focusing on mass customers as the top priority customer segment for the company.")

#####################################################

st.title("Customer buying frequency")

st.markdown("Understanding a customer's behavior and patterns of purchasing. businesses can personalize their marketing efforts, plan operations more effectively, and take steps to retain valuable customers. Overall understanding a customer's buying frequency is a key aspect of customer relationship management.")

purchase_grouping = pd.merge(trans,cust_demo, on='customer_id')
purchase_grouping['month_year'] = purchase_grouping['month'].astype(str) + '-' + purchase_grouping['year'].astype(str)
purchase_grouping = purchase_grouping.groupby(['customer_id', 'month_year']).count().reset_index()
purchase_grouping = purchase_grouping[['customer_id','month_year']].copy()
purchase_grouping = purchase_grouping.groupby('customer_id').month_year.nunique().reset_index(name='Count of unique months')
Groups_df = purchase_grouping.sort_values(by='Count of unique months', ascending=False)
groups ={}

for i in range(1,13,1):
  count = len(Groups_df[Groups_df['Count of unique months'] > i])
  groups[' {} Month'.format(i)] = count
    

groups = pd.DataFrame(list(groups.items()), columns=['keys', 'values'])
groups.columns = ['Month', 'Total no. of customers']

fig = px.bar(groups, x='Month', y='Total no. of customers', title='Number of customers by monthy frequency transaction')
st.plotly_chart(fig)

st.markdown("The bar graph depicts the frequency of customer purchases by month from the company in a given year. It can be observed that the majority of customers, approximately 60%, make a single purchase in a year. Additionally, there is a notable number of customers who make at least two purchases, spread evenly over two different months in a year. The number of frequent monthly buyers decreases as the number of months increases, reaching a minimum at the 9-month mark. However, a small portion of customers, approximately 5% of the total buyers, make purchases from the company more than six times in a year.")


st.title("Conclusion")

st.markdown("Based on the insights from the data analysis, it can be concluded that the company should focus on targeting mass customers as they account for 50% of the total profits generated by the business. The company should also concentrate its marketing efforts on the financial services and manufacturing sectors as these two industries account for 50% of the total profits. Additionally, the company should consider focusing on medium class products as they have been observed to be the most successful in terms of sales and profitability. It is also worth noting that the health sector is a significant contributor to the company's revenue, despite not being present in the top 10 customer analysis. To maximize the revenue, the company can look into attracting and retaining a higher number of frequent buyers, particularly those who make purchases more than six times a year.")





