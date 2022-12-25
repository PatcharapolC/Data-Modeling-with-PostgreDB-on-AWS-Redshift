# Data-Modeling-with-PostgreDB-on-AWS-Redshift
# Songplays Data Modeling with Postgre Database on AWS Redshift data warehouse

## Background

    A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. 
    Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Objective
    - Song play data tables Designed for data analysis. 
    - Queries optimization on with a Postgres Database.
    - Builded ETL pipeline and database schema for data analysis on AWS Redshift (Cloud).
    - Evaluated data modeling with Sparkify's expected results.

### Data Fields for each table in this project
    staging_events_table :
        1. artist
        2. auth
        3. first_name
        4. gender
        5. itemInSession
        6. last_name
        7. length
        8. level
        9. location
        10. method
        11. page
        12. registration
        13. session_id
        14. song
        15. status
        16. ts
        17. user_agent
        18. user_id
        
        
    staging_songs_table :
        1. artist_id
        2. latitude
        3. location
        4. longitude
        5. name
        6. duration
        7. num_songs
        8. song_id
        9. title
        10. year
        
    songplays table :
        1. songplay_id 
        2. start_time
        3. user_id
        4. level
        5. song_id
        6. artist_id
        7. session_id
        8. location
        9. user_agent

    users table:
        1. user_id
        2. first_name
        3. last_name
        4. gender
        5. level

    songs table:
        1. song_id
        2. title
        3. artist_id
        4. year
        5. duration


    artists table :
        1. artist_id
        2. name
        3. location
        4. latitude
        5. longitude

    time
        1. start_time
        2. hour
        3. day
        4. week
        5. month
        6. year
        7. weekday

## Schema diagram

<a href="https://ibb.co/yqmqnqD"><img src="https://i.ibb.co/L1D1z1M/songplays-schema.png" alt="songplays-schema" border="0"></a>

## Project files

- `sql_queries.py` - SQL commands for creating tables, insert values, drop tables and select tables.
- `create_tables.py` - Create and drop table from 'sql_queries.py' commands.
- `song_data` and `log_data` labels; source : 'http://millionsongdataset.com/'

        song data : s3://udacity-dend/song_data
<a href="https://ibb.co/rypRsGS"><img src="https://i.ibb.co/9Y4kt9L/song-event-data-1.png" alt="song-event-data-1" border="0" /></a>

        song log data : s3://udacity-dend/log_data
<a href="https://ibb.co/f94hp92"><img src="https://i.ibb.co/DY5xCYt/song-log-data-1.png" alt="song-log-data-1" border="0" /></a>

- `etl.py` - Final ETL Processing file from etl.ipynb and ready to use it for dataset or song metadata files !
- `dwh.cfg` - Cloud configuration with IAM User, IAM Role, Redshift Cluster, S3 Bucket for dataset and Data warehouse configuration.

## For implementation this project
    1. Open your Terminal and clear all existed tables
    2. Created tables in your database with Cloud configuration (following dwh.cfg file)
       command : python create_tables.py
        2.1. Completed statement in sql_queries.py
    3. run etl.py when ETL Process implementation in sql_queries.py is completed
        3.1. Don't forget recheck sql_queries.py command is correct !
        3.2. Don't forget deleted or drop existed talbes before running all files
        3.3.Don't forget update and recheck cloud configuration in dwh.cfg file.
    4. Finished or Completed, If not have ERROR after ran 'etl.py' and recheck tables with query editor on your redshfit cluster is correct.
    
## How to run ?
    0. Open your Terminal and clear all existed tables
    1. Created tables in your database
       command : python create_tables.py
    2. Executed for ETL process and data processing
       command : python etl.py
    3. DONE !
    
## My git : https://gist.github.com/MosesOhYes
## Related Project : https://gist.github.com/MosesOhYes/6f5e761c74fde816cb83d10338786ec6
