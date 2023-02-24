import pandas as pd
from extract import extract
from transform import transform

def main():
    movies_df, movie_details_df = extract()
    df = transform(movies_df, movie_details_df)
    local_path = 'etl/data/output.csv'
    df.to_csv(local_path)
    return 

if __name__ == '__main__':
    main()
