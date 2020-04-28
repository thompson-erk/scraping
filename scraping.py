import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

jobs = []
for page in list(range(1,4)):
    data = requests.get('https://www.governmentjobs.com/jobs?page={page}&location={city}%2C{state}&distance=25&sort=date&isDescendingSort=True&isTransfer=False&isPromotional=False)'.format(page=page,city='raleigh',state='nc'))
    soup = BeautifulSoup(data.text, 'html.parser')

    rawjobs = soup.find('ul',{'class':'unstyled job-listing-container'})

    for job in rawjobs.find_all('div',{'class':'span12'}):
        jobname = job.find('a',{'class':'job-details-link'}).text.strip()
        jobloc = job.find_all('div',{'class':'primaryInfo'})[0].text.strip()
        jobsalary = job.find_all('div',{'class':'primaryInfo'})[1].text.strip()
        jobs.append((jobname,jobloc,jobsalary))
        print(jobname)
        print(jobloc)
        print(jobsalary)
    time.sleep(3)

df = pd.DataFrame(jobs,columns = ['jobname','location','salary'])
print(df)

