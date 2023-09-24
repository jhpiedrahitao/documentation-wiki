# Get Started with Data Wrangler<a name="data-wrangler-getting-started"></a>

Amazon SageMaker Data Wrangler is a feature in Amazon SageMaker Studio\. Use this section to learn how to access and get started using Data Wrangler\. Do the following:

1. Complete each step in [Prerequisites](#data-wrangler-getting-started-prerequisite)\.

1. Follow the procedure in [Access Data Wrangler](#data-wrangler-getting-started-access) to start using Data Wrangler\.

## Prerequisites<a name="data-wrangler-getting-started-prerequisite"></a>

To use Data Wrangler, you must complete the following prerequisites\. 

1. To use Data Wrangler, you need access to an Amazon Elastic Compute Cloud \(Amazon EC2\) instance\. For more information about the Amazon EC2 instances that you can use, see [Instances](data-wrangler-data-flow.md#data-wrangler-data-flow-instances)\. To learn how to view your quotas and, if necessary, request a quota increase, see [AWS service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html)\.

1. Configure the required permissions described in [Security and Permissions](data-wrangler-security.md)\. 

To use Data Wrangler, you need an active Studio instance\. To learn how to launch a new instance, see [Onboard to Amazon SageMaker Domain](gs-studio-onboard.md)\. When your Studio instance is **Ready**, use the instructions in [Access Data Wrangler](#data-wrangler-getting-started-access)\.

## Access Data Wrangler<a name="data-wrangler-getting-started-access"></a>

The following procedure assumes you have completed the [Prerequisites](#data-wrangler-getting-started-prerequisite)\.

To access Data Wrangler in Studio, do the following\.

1. Sign in to Studio\. For more information, see [Onboard to Amazon SageMaker Domain](gs-studio-onboard.md)\.

1. Choose **Studio**\.

1. Choose **Launch app**\.

1. From the dropdown list, select **Studio**\.

1. Choose the Home icon\.

1. Choose **Data**\.

1. Choose **Data Wrangler**\.

1. You can also create a Data Wrangler flow by doing the following\.

   1. In the top navigation bar, select **File**\.

   1. Select **New**\.

   1. Select **Data Wrangler Flow**\.  
![\[Image NOT FOUND\]](http://docs.aws.amazon.com/sagemaker/latest/dg/images/studio/mohave/new-flow-file-menu.png)

1. \(Optional\) Rename the new directory and the \.flow file\. 

1. When you create a new \.flow file in Studio, you might see a carousel that introduces you to Data Wrangler\.

   **This may take a few minutes\.**

   This messaging persists as long as the **KernelGateway** app on your **User Details** page is **Pending**\. To see the status of this app, in the SageMaker console on the **Amazon SageMaker Studio** page, select the name of the user you are using to access Studio\. On the **User Details** page, you see a **KernelGateway** app under **Apps**\. Wait until this app status is **Ready** to start using Data Wrangler\. This can take around 5 minutes the first time you launch Data Wrangler\.  
![\[Image NOT FOUND\]](http://docs.aws.amazon.com/sagemaker/latest/dg/images/studio/mohave/gatewayKernel-ready.png)

1. To get started, choose a data source and use it to import a dataset\. See [Import](data-wrangler-import.md) to learn more\. 

   When you import a dataset, it appears in your data flow\. To learn more, see [Create and Use a Data Wrangler Flow](data-wrangler-data-flow.md)\.

1. After you import a dataset, Data Wrangler automatically infers the type of data in each column\. Choose **\+** next to the **Data types** step and select **Edit data types**\. 
**Important**  
After you add transforms to the **Data types** step, you cannot bulk\-update column types using **Update types**\. 

1. Use the data flow to add transforms and analyses\. To learn more see [Transform Data](data-wrangler-transform.md) and [Analyze and Visualize](data-wrangler-analyses.md)\.

1. To export a complete data flow, choose **Export** and choose an export option\. To learn more, see [Export](data-wrangler-data-export.md)\. 

1. Finally, choose the **Components and registries** icon, and select **Data Wrangler** from the dropdown list to see all the \.flow files that you've created\. You can use this menu to find and move between data flows\.

After you have launched Data Wrangler, you can use the following section to walk through how you might use Data Wrangler to create an ML data prep flow\. 

## Update Data Wrangler<a name="data-wrangler-update"></a>

We recommend that you periodically update the Data Wrangler Studio app to access the latest features and updates\. The Data Wrangler app name starts with **sagemaker\-data\-wrang**\. To learn how to update a Studio app, see [Shut down and Update Studio Apps](studio-tasks-update-apps.md)\.

## Demo: Data Wrangler Titanic Dataset Walkthrough<a name="data-wrangler-getting-started-demo"></a>

The following sections provide a walkthrough to help you get started using Data Wrangler\. This walkthrough assumes that you have already followed the steps in [Access Data Wrangler](#data-wrangler-getting-started-access) and have a new data flow file open that you intend to use for the demo\. You may want to rename this \.flow file to something similar to `titanic-demo.flow`\.

This walkthrough uses the [Titanic dataset](https://s3.us-west-2.amazonaws.com/amazon-sagemaker-data-wrangler-documentation-artifacts/walkthrough_titanic.csv)\. It's a modified version of the [Titanic dataset](https://www.openml.org/d/40945) that you can import into your Data Wrangler flow more easily\. This data set contains the survival status, age, gender, and class \(which serves as a proxy for economic status\) of passengers aboard the maiden voyage of the *RMS Titanic* in 1912\.

In this tutorial, you perform the following steps\.

1. Do one of the following:
   + Open your Data Wrangler flow and choose **Use Sample Dataset**\.
   + Upload the [Titanic dataset](https://s3.us-west-2.amazonaws.com/amazon-sagemaker-data-wrangler-documentation-artifacts/walkthrough_titanic.csv) to Amazon Simple Storage Service \(Amazon S3\), and then import this dataset into Data Wrangler\.

1. Analyze this dataset using Data Wrangler analyses\. 

1. Define a data flow using Data Wrangler data transforms\.

1. Export your flow to a Jupyter Notebook that you can use to create a Data Wrangler job\. 

1. Process your data, and kick off a SageMaker training job to train a XGBoost Binary Classifier\. 

### Upload Dataset to S3 and Import<a name="data-wrangler-getting-started-demo-import"></a>

To get started, you can use one of the following methods to import the Titanic dataset into Data Wrangler:
+ Importing the dataset directly from the Data Wrangler flow
+ Uploading the dataset to Amazon S3 and then importing it into Data Wrangler

To import the dataset directly into Data Wrangler, open the flow and choose **Use Sample Dataset**\.

Uploading the dataset to Amazon S3 and importing it into Data Wrangler is closer to the experience you have importing your own data\. The following information tells you how to upload your dataset and import it\.

Before you start importing the data into Data Wrangler, download the [Titanic dataset](https://s3.us-west-2.amazonaws.com/amazon-sagemaker-data-wrangler-documentation-artifacts/walkthrough_titanic.csv) and upload it to an Amazon S3 \(Amazon S3\) bucket in the AWS Region in which you want to complete this demo\.

If you are a new user of Amazon S3, you can do this using drag and drop in the Amazon S3 console\. To learn how, see [Uploading Files and Folders by Using Drag and Drop](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html#upload-objects-by-drag-and-drop) in the Amazon Simple Storage Service User Guide\.

**Important**  
Upload your dataset to an S3 bucket in the same AWS Region you want to use to complete this demo\. 

When your dataset has been successfully uploaded to Amazon S3, you can import it into Data Wrangler\.

**Import the Titanic dataset to Data Wrangler**

1. Choose the **Import data** button in your **Data flow** tab or choose the **Import** tab\.

1. Select **Amazon S3**\.

1. Use the **Import a dataset from S3** table to find the bucket to which you added the Titanic dataset\. Choose the Titanic dataset CSV file to open the **Details** pane\.

1. Under **Details**, the **File type** should be CSV\. Check **First row is header** to specify that the first row of the dataset is a header\. You can also name the dataset something more friendly, such as **Titanic\-train**\.

1. Choose the **Import ** button\.

When your dataset is imported into Data Wrangler, it appears in your **Data Flow** tab\. You can double click on a node to enter the node detail view, which allows you to add transformations or analysis\. You can use the plus icon for a quick access to the navigation\. In the next section, you use this data flow to add analysis and transform steps\.

### Data Flow<a name="data-wrangler-getting-started-demo-data-flow"></a>

In the data flow section, the only steps in the data flow are your recently imported dataset and a **Data type** step\. After applying transformations, you can come back to this tab and see what the data flow looks like\. Now, add some basic transformations under the **Prepare** and **Analyze** tabs\. 

#### Prepare and Visualize<a name="data-wrangler-getting-started-demo-prep-visualize"></a>

Data Wrangler has built\-in transformations and visualizations that you can use to analyze, clean, and transform your data\. 

The **Data** tab of the node detail view lists all built\-in transformations in the right panel, which also contains an area in which you can add custom transformations\. The following use case showcases how to use these transformations\.

To get information that might help you with data exploration and feature engineering, create a data quality and insights report\. The information from the report can help you clean and process your data\. It gives you information such as the number of missing values and the number of outliers\. If you have issues with your data, such as target leakage or imbalance, the insights report can bring those issues to your attention\. For more information about creating a report, see [Get Insights On Data and Data Quality](data-wrangler-data-insights.md)\.

##### Data Exploration<a name="data-wrangler-getting-started-demo-explore"></a>

First, create a table summary of the data using an analysis\. Do the following:

1. Choose the **\+** next to the **Data type** step in your data flow and select **Add analysis**\.

1. In the **Analysis** area, select **Table summary** from the dropdown list\.

1. Give the table summary a **Name**\.

1. Select **Preview** to preview the table that will be created\.

1. Choose **Save** to save it to your data flow\. It appears under **All Analyses**\.

Using the statistics you see, you can make observations similar to the following about this dataset: 
+ Fare average \(mean\) is around $33, while the max is over $500\. This column likely has outliers\. 
+ This dataset uses *?* to indicate missing values\. A number of columns have missing values: *cabin*, *embarked*, and *home\.dest*
+ The age category is missing over 250 values\.

Next, clean your data using the insights gained from these stats\. 

##### Drop Unused Columns<a name="data-wrangler-getting-started-demo-drop-unused"></a>

Using the analysis from the previous section, clean up the dataset to prepare it for training\. To add a new transform to your data flow, choose **\+** next to the **Data type** step in your data flow and choose **Add transform**\.

First, drop columns that you don't want to use for training\. You can use [pandas](https://pandas.pydata.org/) data analysis library to do this, or you can use one of the built\-in transforms\.

Use the following procedure to drop the unused columns\.

To drop the unused columns\.

1. Open the Data Wrangler flow\.

1. There are two nodes in your Data Wrangler flow\. Choose the **\+** to the right of the **Data types** node\.

1. Choose **Add transform**\.

1. In the **All steps** column, choose **Add step**\.

1. In the **Standard** transform list, choose **Manage Columns**\. The standard transformations are ready\-made, built\-in transformations\. Make sure that **Drop column** is selected\.

1. Under **Columns to drop**, check the following column names:
   + cabin
   + ticket
   + name
   + sibsp
   + parch
   + home\.dest
   + boat
   + body

1. Choose **Preview**\.

1. Verify that the columns have been dropped, then choose **Add**\.

To do this using pandas, follow these steps\.

1. In the **All steps** column, choose **Add step**\.

1. In the **Custom** transform list, choose **Custom transform**\.

1. Provide a name for your transformation, and choose **Python \(Pandas\)** from the dropdown list\.

1. Enter the following Python script in the code box\.

   ```
   cols = ['name', 'ticket', 'cabin', 'sibsp', 'parch', 'home.dest','boat', 'body']
   df = df.drop(cols, axis=1)
   ```

1. Choose **Preview** to preview the change, and then choose **Add** to add the transformation\. 

##### Clean up Missing Values<a name="data-wrangler-getting-started-demo-missing-vals"></a>

Now, clean up missing values\. You can do this with the **Handling missing values** transform group\.

A number of columns have missing values\. Of the remaining columns, *age* and *fare* contain missing values\. Inspect this using a **Custom Transform**\.

Using the **Python \(Pandas\)** option, use the following to quickly review the number of entries in each column:

```
df.info()
```

![\[Image NOT FOUND\]](http://docs.aws.amazon.com/sagemaker/latest/dg/images/studio/mohave/inspect-missing-pandas.png)

To drop rows with missing values in the *age* category, do the following: 

1. Choose **Handle missing**\. 

1. Choose **Drop missing** for the **Transformer**\.

1. Choose *age* for the **Input column**\.

1. Choose **Preview** to see the new data frame, and then choose **Add** to add the transform to your flow\.

1. Repeat the same process for *fare*\. 

You can use `df.info()` in the **Custom transform** section to confirm that all rows now have 1,045 values\.

##### Custom Pandas: Encode<a name="data-wrangler-getting-started-demo-encode"></a>

Try flat encoding using Pandas\. Encoding categorical data is the process of creating a numerical representation for categories\. For example, if your categories are `Dog` and `Cat`, you may encode this information into two vectors: `[1,0]` to represent `Dog`, and `[0,1]` to represent `Cat`\.

1. In the **Custom Transform** section, choose **Python \(Pandas\)** from the dropdown list\.

1. Enter the following in the code box\.

   ```
   import pandas as pd
   
   dummies = []
   cols = ['pclass','sex','embarked']
   for col in cols:
       dummies.append(pd.get_dummies(df[col]))
       
   encoded = pd.concat(dummies, axis=1)
   
   df = pd.concat((df, encoded),axis=1)
   ```

1. Choose **Preview** to preview the change\. The encoded version of each column is added to the dataset\. 

1. Choose **Add** to add the transformation\. 

#### Custom SQL: SELECT Columns<a name="data-wrangler-getting-started-demo-sql"></a>

Now, select the columns you want to keep using SQL\. For this demo, select the columns listed in the following `SELECT` statement\. Because *survived* is your target column for training, put that column first\.

1. In the **Custom Transform** section, select **SQL \(PySpark SQL\)** from the dropdown list\.

1. Enter the following in the code box\.

   ```
   SELECT survived, age, fare, 1, 2, 3, female, male, C, Q, S FROM df;
   ```

1. Choose **Preview** to preview the change\. The columns listed in your `SELECT` statement are the only remaining columns\.

1. Choose **Add** to add the transformation\. 

### Export to a Data Wrangler Notebook<a name="data-wrangler-getting-started-export"></a>

When you've finished creating a data flow, you have a number of export options\. The following section explains how to export to a Data Wrangler job notebook\. A Data Wrangler job is used to process your data using the steps defined in your data flow\. To learn more about all export options, see [Export](data-wrangler-data-export.md)\.

#### Export to Data Wrangler Job Notebook<a name="data-wrangler-getting-started-export-notebook"></a>

When you export your data flow using a **Data Wrangler job**, the process automatically creates a Jupyter Notebook\. This notebook automatically opens in your Studio instance and is configured to run a SageMaker processing job to run your Data Wrangler data flow, which is referred to as a Data Wrangler job\. 

1. Save your data flow\. Select **File** and then select **Save Data Wrangler Flow**\.

1. Back to the **Data Flow** tab, select the last step in your data flow \(SQL\), then choose the **\+** to open the navigation\.

1. Choose **Export**, and **Amazon S3 \(via Jupyter Notebook\)**\. This opens a Jupyter Notebook\.  
![\[Image NOT FOUND\]](http://docs.aws.amazon.com/sagemaker/latest/dg/images/studio/mohave/export-select-step.png)

1. Choose any **Python 3 \(Data Science\)** kernel for the **Kernel**\. 

1. When the kernel starts, run the cells in the notebook book until **Kick off SageMaker Training Job \(Optional\)**\. 

1. Optionally, you can run the cells in **Kick off SageMaker Training Job \(Optional\)** if you want to create a SageMaker training job to train an XGBoost classifier\. You can find the cost to run a SageMaker training job in [Amazon SageMaker Pricing](http://aws.amazon.com/sagemaker/pricing/)\. 

   Alternatively, you can add the code blocks found in [Training XGBoost Classifier](#data-wrangler-getting-started-train-xgboost) to the notebook and run them to use the [XGBoost](https://xgboost.readthedocs.io/en/latest/) open source library to train an XGBoost classifier\. 

1. Uncomment and run the cell under **Cleanup** and run it to revert the SageMaker Python SDK to its original version\.

You can monitor your Data Wrangler job status in the SageMaker console in the **Processing** tab\. Additionally, you can monitor your Data Wrangler job using Amazon CloudWatch\. For additional information, see [Monitor Amazon SageMaker Processing Jobs with CloudWatch Logs and Metrics](https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html#processing-job-cloudwatch)\. 

If you kicked off a training job, you can monitor its status using the SageMaker console under **Training jobs** in the **Training section**\.

#### Training XGBoost Classifier<a name="data-wrangler-getting-started-train-xgboost"></a>

You can train an XGBoost Binary Classifier using either a Jupyter notebook or a Amazon SageMaker Autopilot\. You can use Autopilot to automatically train and tune models on the data that you've transformed directly from your Data Wrangler flow\. For information about Autopilot, see [Automatically Train Models on Your Data Flow](data-wrangler-autopilot.md)\.

In the same notebook that kicked off the Data Wrangler job, you can pull the data and train an XGBoost Binary Classifier using the prepared data with minimal data preparation\. 

1. First, upgrade necessary modules using `pip` and remove the \_SUCCESS file \(this last file is problematic when using `awswrangler`\)\.

   ```
   ! pip install --upgrade awscli awswrangler boto sklearn
   ! aws s3 rm {output_path} --recursive  --exclude "*" --include "*_SUCCESS*"
   ```

1. Read the data from Amazon S3\. You can use `awswrangler` to recursively read all the CSV files in the S3 prefix\. The data is then split into features and labels\. The label is the first column of the dataframe\.

   ```
   import awswrangler as wr
   
   df = wr.s3.read_csv(path=output_path, dataset=True)
   X, y = df.iloc[:,:-1],df.iloc[:,-1]
   ```
   + Finally, create DMatrices \(the XGBoost primitive structure for data\) and do cross\-validation using the XGBoost binary classification\.

     ```
     import xgboost as xgb
     
     dmatrix = xgb.DMatrix(data=X, label=y)
     
     params = {"objective":"binary:logistic",'learning_rate': 0.1, 'max_depth': 5, 'alpha': 10}
     
     xgb.cv(
         dtrain=dmatrix, 
         params=params, 
         nfold=3,
         num_boost_round=50,
         early_stopping_rounds=10,
         metrics="rmse", 
         as_pandas=True, 
         seed=123)
     ```

#### Shut down Data Wrangler<a name="data-wrangler-getting-started-shut-down"></a>

When you are finished using Data Wrangler, we recommend that you shut down the instance it runs on to avoid incurring additional charges\. To learn how to shut down the Data Wrangler app and associated instance, see [Shut Down Data Wrangler](data-wrangler-shut-down.md)\. 