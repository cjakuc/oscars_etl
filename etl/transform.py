import pandas as pd
import datefinder
import numpy as np
import re
import unicodedata
from extract import extract

def transform(
    movies_df: pd.DataFrame
    , movie_details_df: pd.DataFrame
    ) -> pd.DataFrame:
    """
    Transforms 2 Pandas DataFrames according to this promt:
        Find all movies that won an Oscar after year 1955 
        and had a minimum budget of $15mm USD
        Final df:
        movie name, original currency, original budget, budget in USD, 
        release date, year, wikipedia url

    Parameters
    ----------
    movies_df : pd.DataFrame
        DataFrame of movies. Columns = 
            ['Detail URL', 'Film', 'Producer(s)', 'Production Company(s)',
            'Wiki URL', 'Winner']
    movie_details_df : pd.DataFrame
        DataFrame of movie details. Columns = 
            [' Production company ', ' Release dates ', ' Running time ', 'Budget',
            'Cinematography', 'Country', 'Directed by', 'Distributed by',
            'Edited by', 'Language', 'Music by', 'Produced by', 'Screenplay by',
            'Starring', 'Story by', 'Title', 'Written by', 'Detail URL', 'Based on',
            'Box office', 'Narrated by', ' Production companies ']

    Returns
    -------
    pd.DataFrame
        Final DataFrame. Columns =
        ['name', 'original_currency', 'original_budget', 
        'original_budget_in_usd', 'release_date', 'award_year']
    """

    # Oscar eligiblity rules require:
        # - must open in previous calendar year in LA county
        # - play for 7 consecutive days
        # - have 3 showings a day, at least one between 6 and 10pm
    # Eligibility assumption:
        # - the year of release means award year is the next year
        # - the first 4 consecutive numbers in the release date string captures the year correctly
            # min is 1927 and max is 2014, looks good enough for first pass

    # Use datefinder to get the first of the messy dates
    # Assuming first date is the correct release date
    movie_details_df['release_date'] = movie_details_df[' Release dates '].apply(lambda x: list(datefinder.find_dates(x))[0])
    movie_details_df['release_year'] = movie_details_df['release_date'].apply(lambda x: x.year)
    movie_details_df['award_year'] = movie_details_df['release_year'] + 1
    # Filter to release date of at least 1954 (eligible in 1955)
    movie_details_df = movie_details_df.loc[movie_details_df['award_year'] > 1954]

    # We need budget to answer the prompt so let's drop null budgets
    movie_details_df = movie_details_df.loc[movie_details_df['Budget'].notna()]

    # After above filtering there are no budgets without a $
    # There was before so this ensures it doesn't break
    # We could convert the currency but for now let's drop them if they don't have a '$'
    movie_details_df['original_budget'] = movie_details_df['Budget'].str.replace(unicodedata.lookup('EURO SIGN'), 'Euro')
    movie_details_df['original_budget'] = movie_details_df['original_budget'].str.replace('£', 'POUND SIGN')
    movie_details_df = movie_details_df.loc[~movie_details_df['original_budget'].str.contains('EURO SIGN')]
    movie_details_df = movie_details_df.loc[~movie_details_df['original_budget'].str.contains('POUND SIGN')]
    movie_details_df = movie_details_df.loc[movie_details_df['original_budget'].str.contains('$')]
    movie_details_df['original_budget'] = movie_details_df['original_budget'].apply(lambda x: x.split('$')[-1])
    movie_details_df['original_budget'] = movie_details_df['original_budget'].apply(lambda x: x.split('$')[-1])
    movie_details_df['original_currency'] = 'USD'

    # Looks like budgets > 999,999 always contain 'million
    movie_details_df['original_budget'] = movie_details_df['original_budget'].str.lower()
    movie_details_df = movie_details_df.loc[movie_details_df['original_budget'].str.contains('million')]

    movie_details_df['original_budget'] = movie_details_df['original_budget'].apply(lambda x: x.split('–')[-1])
    # Remove everything after the number
    movie_details_df['original_budget'] = movie_details_df['original_budget'].apply(lambda x: x.split(' ')[0])
    # Issue with some splitting, removing the 9 failures for now
    movie_details_df = movie_details_df.loc[~movie_details_df['original_budget'].str.contains('million')]
    movie_details_df['original_budget'] = movie_details_df['original_budget'].replace('', np.nan)
    movie_details_df = movie_details_df.dropna(subset=['original_budget'])
    movie_details_df['original_budget'] = movie_details_df['original_budget'].apply(lambda x: x.split('-')[-1])
    movie_details_df['original_budget'] = movie_details_df['original_budget'].astype(float)

    # Filter to >= 15 million
    movie_details_df = movie_details_df.loc[movie_details_df['original_budget'] >= 15]

    movie_details_df['name'] = movie_details_df['Title'].str.lower()
    movies_df['name'] = movies_df['Film'].str.lower()

    final_df = movie_details_df.merge(
        movies_df
        , left_on='name'
        , right_on='name'
        , how='left')
    final_df = final_df.loc[final_df['Winner']]
    final_df = final_df.reset_index()
    final_df['original_budget_in_usd'] = final_df['original_budget']*1e6
    final_df['original_budget_in_usd'] = '$' + final_df['original_budget_in_usd'].astype(str)
    final_cols = ['name', 'original_currency', 'original_budget', 'original_budget_in_usd', 'release_date', 'award_year']
    final_df = final_df[final_cols]
    
    return final_df


if __name__ == '__main__':
    movies_df, movie_details_df = extract()
    final_df = transform(movies_df, movie_details_df)
