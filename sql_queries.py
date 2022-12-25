import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= (""" create table if not exists staging_events_table(
                                              artist varchar, 
                                              auth varchar, 
                                              first_name varchar, 
                                              gender varchar, 
                                              itemInSession integer, 
                                              last_name varchar,
                                              length float,
                                              level varchar,
                                              location varchar,
                                              method varchar,
                                              page varchar,
                                              registration varchar,
                                              session_id int,
                                              song varchar,
                                              status varchar,
                                              ts bigint,
                                              user_agent varchar,
                                              user_id int
                                            );
""")

staging_songs_table_create = ("""create table if not exists staging_songs_table( 
                                            artist_id varchar, 
                                            latitude float,
                                            location varchar, 
                                            longitude float,
                                            name varchar, 
                                            duration float,
                                            num_songs int,
                                            song_id varchar,
                                            title varchar,
                                            year int
                                        );
""")

songplay_table_create = ("""create table if not exists songplays (
                                        songplay_id int identity(0, 1) primary key, 
                                        start_time timestamp not null REFERENCES time (start_time), 
                                        user_id int not null REFERENCES users (user_id), 
                                        level varchar,
                                        song_id varchar REFERENCES songs (song_id), 
                                        artist_id varchar REFERENCES artists (artist_id), 
                                        session_id int, 
                                        location varchar, 
                                        user_agent varchar
                                    );
""")


user_table_create = ("""create table if not exists users (
                                    user_id int primary key, 
                                    first_name varchar, 
                                    last_name varchar, 
                                    gender varchar, 
                                    level varchar
                                );
""")

song_table_create = ("""create table if not exists songs (
                                    song_id varchar primary key,
                                    title varchar not null, 
                                    artist_id varchar REFERENCES artists (artist_id),
                                    year int, 
                                    duration float not null
                                );
""")

artist_table_create = ("""create table if not exists artists (
                                    artist_id varchar primary key, 
                                    name varchar, 
                                    location varchar,
                                    latitude float, 
                                    longitude float
                                );
""")

time_table_create = ("""create table if not exists time(
                            start_time timestamp primary key, 
                            hour varchar,
                            day varchar,
                            week varchar,
                            month varchar,
                            year int,
                            weekday varchar
                        );
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events_table from {}
credentials 'aws_iam_role={}'
    FORMAT AS JSON {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
copy staging_songs_table from {} 
credentials 'aws_iam_role={}'
    FORMAT AS JSON 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""insert into songplays(
                                        start_time,
                                        user_id,
                                        level,
                                        song_id,
                                        artist_id,
                                        session_id,
                                        location,
                                        user_agent
                            )
                            select  distinct timestamp 'epoch' + se.ts/1000 * interval '1 second', 
                                    se.user_id, 
                                    se.level,
                                    ss.song_id, 
                                    ss.artist_id, 
                                    se.session_id, 
                                    se.location, 
                                    se.user_agent
                            from staging_events_table as se
                            join staging_songs_table as ss
                            on (se.artist = ss.name)
                            where se.page = 'NextSong'
                        ;
""")

user_table_insert = ("""insert into users(
                                    user_id, 
                                    first_name, 
                                    last_name, 
                                    gender, 
                                    level
                            )
                            select  se.user_id, 
                                    se.first_name, 
                                    se.last_name,
                                    se.gender, 
                                    se.level
                            from staging_events_table as se
                            where se.user_id is not null
                            and se.page = 'NextSong'
                        ;
""")

song_table_insert = ("""insert into songs(
                                    song_id, 
                                    title, 
                                    artist_id, 
                                    year, 
                                    duration
                            )
                            select  ss.song_id,
                                    ss.title,
                                    ss.artist_id,
                                    ss.year,  
                                    ss.duration
                            from staging_songs_table as ss
                            where song_id is not null
                        ;
""")

artist_table_insert = ("""insert into artists(
                                    artist_id, 
                                    name, 
                                    location,
                                    latitude, 
                                    longitude
                            )
                            select ss.artist_id, 
                                   ss.name, 
                                   ss.location, 
                                   ss.latitude, 
                                   ss.longitude
                            from staging_songs_table as ss
                            where artist_id is not null
                        ;
""")

time_table_insert = ("""insert into time(
                                    start_time, 
                                    hour , 
                                    day,
                                    week, 
                                    month, 
                                    year, 
                                    weekday
                            )
                            select  distinct timestamp 'epoch' + se.ts/1000 * interval '1 second' as start_time, 
                            extract (HOUR FROM start_time), 
                            extract (DAY FROM start_time),
                            extract (WEEK FROM start_time), 
                            extract (MONTH FROM start_time),
                            extract (YEAR FROM start_time), 
                            extract (WEEKDAY FROM start_time) 
                            from staging_events_table as se
                            where se.page = 'NextSong'
                            ;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, artist_table_create, song_table_create, user_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [artist_table_insert, song_table_insert, user_table_insert, time_table_insert, songplay_table_insert]
