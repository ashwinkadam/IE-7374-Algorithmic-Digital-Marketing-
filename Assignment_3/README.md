# Customer Spending Prediction using Snowflake Dataplatform
This project aims to predict customer spending based on some important features using Snowflake Dataplatform. Snowflake is a cloud-based data warehousing platform that provides various capabilities such as UDF (User Defined Function), Sproc (Stored Procedure) and Stage area to store ML models.

<img width="897" alt="image" src="https://user-images.githubusercontent.com/53835307/224519623-af6f0c43-ffcc-4844-b3ed-94d80377032a.png">


## Project Overview
In this project, we have used Snowflake Dataplatform to store our ML model and perform customer spending prediction. We have trained our model locally using Snowflake sample data and then stored the model in Snowflake stage. Additionally, we have created stored procedures and user-defined functions that can be leveraged to perform prediction on new data.

Finally, we have deployed our ML model in a Streamlit app where the user can upload new data and get predicted values in return.


<img width="767" alt="image" src="https://user-images.githubusercontent.com/53835307/224519832-f7e01d83-37d6-4f5f-90e6-ea3fd355827e.png">


<img width="817" alt="image" src="https://user-images.githubusercontent.com/53835307/224519842-b242a30d-bd73-4048-9bd1-6d228c268068.png">



## How to Use
1. Clone this repository to your local machine.
2. Create a Snowflake account and set up the required credentials.
3. To create Database, feature table and to tarined model run locally script 'Customer_Spending_Prediction.ipynb'
4. Run the Streamlit app using the following command: streamlit run 'Customer_Spend_app.py'
5. Upload a CSV file with the required features to the Streamlit app.
6. Get the predicted values for customer spending.

## Conclusion
This project demonstrated how to use Snowflake Dataplatform to perform customer spending prediction using an ML model. By leveraging the platform's capabilities like UDF, Sproc, and Stage area, we were able to store and deploy our ML model effectively. The Streamlit app provided a user-friendly interface to upload new data and get predicted values.




Codelab Link : https://docs.google.com/document/d/e/2PACX-1vQVDmyOos9SDuZjedVESNmPEoj8VSN3QCRlkZ76QySHVto0BuXoeDE4ThypLrRUaQjQkTpbWYSDcUSd/pub


App Link : https://ashwinkadam-ie-7374-algor-assignment-3customer-spend-app-a5cegx.streamlit.app/
