import pandas as pd
import numpy as np

df = pd.read_csv('Jobs.csv')

#Drop rows with missing 'Salary Estimate'
df = df.dropna(subset=['Salary Estimate'])

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

# Define the function to process the 'min_salary'
# def extract_min_salary(salary_range):
#     try:
#         return int(float(salary_range.split('-')[0].strip()))
#     except ValueError:
#         return None

df['min_salary'] = min_hr.apply(lambda x: int(float(x.split('-')[0])))


def extract_max_salary(value):
    try:
        return int(value.split('-')[-1].strip())  # Access the last element
    except (ValueError, IndexError):
        return 0  # Handle errors

df['max_salary'] = min_hr.apply(extract_max_salary)
# df['max_salary'] = min_hr.apply(lambda y: int(y.split('-')[1].strip()))

df['avg_salary'] = (df.min_salary+df.max_salary)/2

#state field 
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[0])

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

df_out = df.drop(['Unnamed: 0'], axis =1)

df_out.to_csv('salary_data_cleaned.csv',index = False)