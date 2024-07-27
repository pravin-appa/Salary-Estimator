import pandas as pd
import numpy as np

df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing 

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(float(x.split('-')[0].strip())) if '-' in x else int(float(x.strip())))
df['max_salary'] = min_hr.apply(lambda x: int(float(x.split('-')[1].strip())) if '-' in x else int(float(x.strip())))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#state field 
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[0])
df.job_state.value_counts()

# Function to convert values to integers, with default for non-numeric entries
def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return -1

# Apply the conversion and then calculate the age
df['age'] = df['Founded'].apply(lambda x: convert_to_int(x)).apply(lambda x: x if x < 1 else 2020 - x)

#parsing of job description (python, etc.)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
#r studio 
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)


#spark 
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)


#aws 
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)


#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

print(df.columns)
df_out = df.drop(['-1'], axis =1)

df_out.to_csv('salary_data_cleaned.csv',index = False)
