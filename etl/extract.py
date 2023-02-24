from dotenv import load_dotenv
import boto3
import pandas as pd
from os import environ, listdir
import json

load_dotenv()
AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
BUCKET_NAME = environ['BUCKET_NAME']

file_names = ['movies_file.json', 'movie_details_file.json']
local_directory = 'etl/data'

def extract() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Function to extract files from S3 bucket and returns them as Pandas DataFrames.
    Does not extract files from S3 if the files already exist locally.

    Returns
    ----------
    return_tup: Tuple:
        A tuple of two DataFrames containing the following
        movies_df: pd.DataFrame
            DataFrame of movies. Columns = 
            ['Detail URL', 'Film', 'Producer(s)', 'Production Company(s)',
            'Wiki URL', 'Winner']
        movie_details_df: pd.DataFrame
            DataFrame of movie details. Columns = 
            [' Production company ', ' Release dates ', ' Running time ', 'Budget',
            'Cinematography', 'Country', 'Directed by', 'Distributed by',
            'Edited by', 'Language', 'Music by', 'Produced by', 'Screenplay by',
            'Starring', 'Story by', 'Title', 'Written by', 'Detail URL', 'Based on',
            'Box office', 'Narrated by', ' Production companies ']
    """
    # If files already exists locally, don't download
    check =  all(f in listdir(local_directory) for f in file_names)
    if not check:
        s3_object = boto3.client(
            's3'
            , aws_access_key_id=AWS_ACCESS_KEY_ID
            , aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
        s3_object.download_file(
            Bucket=BUCKET_NAME
            , Key='movies'
            , Filename=f'{local_directory}/movies_file.json'
        )
        s3_object.download_file(
            Bucket=BUCKET_NAME
            , Key='movie-details'
            , Filename=f'{local_directory}/movie_details_file.json'
        )

    # Turn movies file into a df
    with open(f"{local_directory}/movies_file.json") as json_file:
        movies_data = json.load(json_file)
    movies_df = pd.json_normalize(movies_data['results'], record_path=['films'])

    # Turn movie details file into a df
    movie_details_df = pd.read_json(f"{local_directory}/movie_details_file.json", lines=True)
    return_tup = (movies_df, movie_details_df)

    return return_tup

if __name__ == '__main__':
    movies_df, movie_details_df = extract()
