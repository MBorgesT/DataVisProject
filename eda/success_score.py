import pandas as pd
import sqlalchemy as db

import math


def avgRatingScore(avgRating, avgRatingMulti=4, maxAvgRating=9.7, minAvgRating=4):
    return (max(minAvgRating, avgRating) - minAvgRating) / (maxAvgRating - minAvgRating)


def nVotesScore(nVotes, maxNVotes=2060874, minNVotes=1899, log_base=5000):
    return max(0, math.log((nVotes - minNVotes) / (maxNVotes - minNVotes), log_base) + 1)


def nCountryScore(nCountry, maxNCountry=99, minNCountry=1):
    return (nCountry - minNCountry) / (maxNCountry - minNCountry)


def timeScore(nEpisodes, runtimeMinutes, maxTime=13716, minTime=0, maxRuntime=120, log_base=5000):
    timeScoreOrig = (
        (nEpisodes * (min(maxRuntime, runtimeMinutes) / 60)) - minTime
    ) / (maxTime - minTime)
    return max(0, math.log(timeScoreOrig, log_base) + 1)


def success_score(
        row,
        avgRatingMulti=4, nVotesMulti=5, nCountryReleasesMulti=1.6, timeMulti=.6):
    return (
        (avgRatingScore(row['averageRating']) * avgRatingMulti) +
        (nVotesScore(row['numVotes']) * nVotesMulti) +
        (nCountryScore(row['nCountryReleases']) * nCountryReleasesMulti) +
        (timeScore(row['nEpisodes'], row['runtimeMinutes']) * timeMulti)
    )


def normalize(col):
    col = (col - col.min()) / (col.max() - col.min())
    return col


def get_clean_dataset_with_ss():
    connection_str = f'mysql+pymysql://root:admin@172.17.0.2:3306/imdb'
    engine = db.create_engine(connection_str)
    conn = engine.connect()
    
    query = '''
        SELECT tb.tconst, tb.genres, tr.averageRating, tr.numVotes, tb.runtimeMinutes, tb.nCountryReleases, tb.nEpisodes
        FROM title_basics tb
        LEFT JOIN title_ratings tr ON tb.tconst = tr.tconst
        WHERE tr.numVotes >= 1900
    '''
    df = pd.read_sql(query, conn)
    
    df['successScore'] = df.apply(success_score, axis=1)
    df['successScore'] = normalize(df['successScore'])
    
    return df
