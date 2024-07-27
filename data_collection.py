import glassdoor_scrapper as gs
import pandas as pd 


df = gs.get_jobs('Data Scientist',1000, False)

df.to_csv('glassdoor_jobs.csv')