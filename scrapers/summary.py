import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tqdm import tqdm


def scrap_summary(tconst):
    url = f'https://www.imdb.com/title/{tconst}/'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features='lxml')
    
    summary = soup.find('span', {'class': 'sc-16ede01-0 fMPjMP'}).text
    return summary


if __name__ == '__main__':
    with open('treated_datasets/most_successful_333.txt', 'r') as f:
        top_tconsts = f.read().split('\n')
        
    summaries = []
    for tconst in tqdm(top_tconsts):
        summaries.append(scrap_summary(tconst))
    
    df = pd.DataFrame({'tconst': top_tconsts, 'summary': summaries})
    df.to_csv('treated_datasets/top333_summaries.tsv', sep='\t')