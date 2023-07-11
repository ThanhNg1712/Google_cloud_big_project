
# Google Cloud Data Engineer Project

## Project Overview
The primary goal of this project is to build a scalable and automated data engineering pipeline that facilitates the migration, transformation, and analysis of data. By utilizing Google Cloud services, we can leverage their robust infrastructure and powerful tools to handle large datasets efficiently


## Step 1: Export Data From Mong DB to GoogleCloud bucket

Script: `Push_data_mongo2cloud.py`
- Data is uploaded from Mongo DB to the Google Cloud Storage bucket
- A Google Storage credential key needs to be set up
- Unnecessary fields are eliminated to avoid error

## Step 2: Transfer Data from Google Cloud Bucket to Google Biquery

Script: `main.py`
Script: `requirement.txt`

- The Google Cloud function is used to transfer data from the bucket to Bigquery
- When new data is uploaded from MongoDB to the bucket, an event is triggered to transfer data to Bigquery
  
## Step 3: Create Seller Data

- A new table is created by the transferred data from Google Cloud Bucket for further analysis
```sql
CREATE OR REPLACE TABLE `tiki-project-390622.tiki_product.seller_data` AS
SELECT specifications, current_seller, id, name, price, images, warranty_info, categories, description,
    short_description, rating_average, all_time_quantity_sold, brand, sku, review_text, review_count
FROM `tiki-project-390622.tiki_product.tiki_data`
```

  
## Step 4: Connect Data Studion and Generate a report

- Several analyses are generated in the customer query in Data Studio
- Table has a nested structure, apply the "unest" function to flatten the nested structure
- Visualization of the report can be found in the PDF file below
[Click here to view the Tiki Data Studio report](https://github.com/ThanhNg1712/Google_cloud_big_project/blob/main/tiki_data_studio.pdf)

```sql
--query 1
SELECT categories.id,categories.name, 
        
        SUM(all_time_quantity_sold) AS total_quantity_sold
FROM `tiki-project-390622.tiki_product.seller_data`
GROUP BY categories.id,categories.name
order by total_quantity_sold desc
limit 10;

--query 2
SELECT current_seller.id AS seller_id, 
      current_seller.name AS seller_name, 
      COUNT(*) AS product_count
FROM `tiki-project-390622.tiki_product.seller_data`
GROUP BY seller_id, seller_name
Order By product_count DESC limit 10;

--query 3
SELECT u.id, u.name,u.categories.name,u.current_seller.name
FROM `tiki-project-390622.tiki_product.seller_data` u,
UNNEST(specifications) AS spec,
UNNEST(spec.attributes) AS attr
WHERE attr.code = "origin" AND attr.value = "Trung Quốc";
```
## Step 5: Data Migration Automation

Script: `log_check.py`
- A cron job is set up to automate the transfer of data from MongoDB to Google Cloud Storage
- The task is scheduled to run daily at 20:00
- log_check.py is executed at the scheduled time, triggering the execution of Push_data_mongo2cloud.py
- The script creates and updates a script.log file in the same local directory, providing detailed status updates for each run
- crontab command can be found below

env EDITOR= nano crontab -e
00 20 * * * /Users/path/to/folder/log_check.py

Detailed status updates are logged in the script.log file, facilitating monitoring and troubleshooting of the data migration process.
  

## License

Specify the license for the project.

## Contributing

Guidelines for contributing to the project.

## Authors

List the authors or contributors of the project.

## Acknowledgments

Credits or acknowledgments for any resources or inspiration used in the project.

