"""
Created on Sat Jul 2024

author: Moiz-Punisher
url: https://github.com/Moiz-Punisher/Selenium-Job-Scraper/tree/main
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1120, 1000)
    char = str(len(keyword))
    url = 'https://www.glassdoor.com/Job/' + keyword + '-jobs-SRCH_KO0,' + char + '.htm'
    driver.get(url)
    jobs = []
    time.sleep(5)
    processed = set()

    while len(jobs) < num_jobs:
        # Going through each job in this page
        try:
            job_cards = driver.find_elements(By.CLASS_NAME, 'JobCard_jobCardContainer___hKKI')
            print("Found job cards:", len(job_cards))
        except:
            continue

        print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
        if len(jobs) >= num_jobs:
            break

        for job_card in job_cards:
            if len(jobs) >= num_jobs:
                return pd.DataFrame(jobs)
            try:
                driver.find_element(By.XPATH, "/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button").click()  # clicking to the X.
                print("clicked the cross")
            except NoSuchElementException:
                pass

            job_url = job_card.find_element(By.CLASS_NAME, 'JobCard_jobTitle___7I6y').get_attribute('href')
            if job_url not in processed:
                try:
                    job_card.click()
                    time.sleep(2)
                    collected_successfully = False
                    while not collected_successfully:
                        try:
                            company_name = job_card.find_element(By.CLASS_NAME, 'EmployerProfile_compactEmployerName__LE242').text
                            location = job_card.find_element(By.CLASS_NAME, 'JobCard_location__rCz3x').text
                            job_title = job_card.find_element(By.CLASS_NAME, 'JobCard_jobTitle___7I6y').text
                            job_description = job_card.find_element(By.CLASS_NAME, 'JobCard_jobDescriptionSnippet__yWW8q').text
                            collected_successfully = True
                            processed.add(job_url)
                        except NoSuchElementException:
                            time.sleep(5)
                    try:
                        salary_estimate = job_card.find_element(By.CLASS_NAME, 'JobCard_salaryEstimate__arV5J').text
                    except NoSuchElementException:
                        salary_estimate = None  # Set to None if not found

                    try:
                        rating = job_card.find_element(By.CLASS_NAME, 'EmployerProfile_ratingContainer__ul0Ef').text
                    except NoSuchElementException:
                        rating = None  # Set to None if not found

                    # Printing for debugging
                    if verbose:
                        print("Job Title: {}".format(job_title))
                        print("Salary Estimate: {}".format(salary_estimate))
                        print("Job Description: {}".format(job_description[:500]))
                        print("Rating: {}".format(rating))
                        print("Company Name: {}".format(company_name))
                        print("Location: {}".format(location))

                    # Going to the Company tab...
                    time.sleep(4)
                    j = 1
                    try:
                        size = driver.find_element(By.XPATH, '(//div[@class="JobDetails_overviewItemValue__xn8EF"])['+str(j)+']').text
                        j += 1
                    except NoSuchElementException:
                        size = None

                    if verbose:
                        print("Size: {}".format(size))

                    jobs.append({
                        "Job Title": job_title,
                        "Salary Estimate": salary_estimate,
                        "Job Description": job_description,
                        "Rating": rating,
                        "Company Name": company_name,
                        "Location": location,
                        "Size": size,
                    })
                except ElementClickInterceptedException:
                    print("Error clicking on job card")
                    continue
                except ElementNotInteractableException:
                    print("Job card not interactable")
                    continue

        try:
            load_more_button = driver.find_element(By.XPATH, '(//button[@data-test="load-more"])')
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    driver.quit()
    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.

