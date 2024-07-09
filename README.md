# SingleStore Full Text Search Demo with Flask

## Overview
This Flask application demonstrates the full-text search capabilities of SingleStore DB using a job search scenario. It showcases how to implement autocomplete features and complex search functionalities within a web application. This is ideal for understanding the performance and flexibility of SingleStore's full-text search features in real-world applications.

## Key Features
- **Advanced Search**: Combines multiple search criteria such as job title, company, and location to filter job postings effectively.
- **Performance Metrics**: Measures and displays the time to execute search queries, demonstrating SingleStore's efficiency.

## Installation

### Prerequisites
- Python 3.x
- Flask
- PyMySQL
- SingleStore instance ( this demo is built on S-00 instance)

### Setup
1. Clone this repository.
2. Install required Python packages:
   ```bash
   pip install flask pymysql pyyaml
   ```
3. Update db.yaml with your SingleStore database credentials.
4. Download the dataset from the below link and put it into SingleStore Stage
5. Once in stage use, the "Load to database" option to generate a notebook that will create the table and pipelines to ingest the file
   <img width="1435" alt="image" src="https://github.com/vishwajeetdabholkar/job_description_hybrid_search/assets/36807939/a5beeec5-4eef-4e55-a5dd-414f9c006513">
   <img width="241" alt="image" src="https://github.com/vishwajeetdabholkar/job_description_hybrid_search/assets/36807939/84e81f10-2146-4b0f-ab8e-032981ac053b">
6. once that is done run below to create a full-text search on top of it:
  ```sql
  OPTIMIZE TABLE postings FLUSH;
  ALTER TABLE `postings` ADD FULLTEXT USING VERSION 2 job_search_idx (title, description, location);
  ```
7. once this is done, run the app using `python app.py`
8. the app should be hosted at: `http://localhost:5000/`
9. You can implement Hyrbird search with SingleStore's vector search and full-text search to get more refined results, refer to the below link.

Read more here: 
- https://docs.singlestore.com/cloud/developer-resources/functional-extensions/hybrid-search-re-ranking-and-blending-searches/

We are using this dataset for this demo: 
- https://www.kaggle.com/datasets/arshkon/linkedin-job-postings


Sample Screenshots:
![job_search_demo](https://github.com/vishwajeetdabholkar/job_description_hybrid_search/assets/36807939/f3ffc4ba-53cb-4b87-9918-72829b8fa88a)

<img width="1435" alt="image" src="https://github.com/vishwajeetdabholkar/job_description_hybrid_search/assets/36807939/bbc3ac80-98cd-465a-85a8-215680bb4e12">
<img width="1435" alt="image" src="https://github.com/vishwajeetdabholkar/job_description_hybrid_search/assets/36807939/4df383de-d021-4035-9bcf-6425f3dcc978">



