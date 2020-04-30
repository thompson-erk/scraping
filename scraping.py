import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

class JobScraper(object):
    def __init__(self):
        self._jobs = []
        self._city_dict = {}
        self._search_df = pd.DataFrame()

    def list_to_dict(self,city_list):
        self._city_dict = {}
        for city in city_list:
            self._city_dict[city_list.index(city)] = {'city': city.split(',')[0],
                                                'state': city.replace(' ', '').split(',')[1]}
        return self._city_dict


    def job_search(self,city_dict=None):
        if city_dict == None:
            pass
        else:
            self._city_dict = city_dict

        for i in range(0,len(self._city_dict)):
            city = self._city_dict[i]['city']
            state = self._city_dict[i]['state']
            for page in list(range(1,4)):
                data = requests.get('https://www.governmentjobs.com/jobs?page={page}&location={city}%2C{state}&distance=25&sort=date&isDescendingSort=True&isTransfer=False&isPromotional=False'\
                                    .format(page=page,city=city,state=state))
                soup = BeautifulSoup(data.text, 'html.parser')

                rawjobs = soup.find('ul',{'class':'unstyled job-listing-container'})

                for job in rawjobs.find_all('div',{'class':'span12'}):
                    jobname = job.find('a',{'class':'job-details-link'}).text.strip()
                    jobloc = job.find_all('div',{'class':'primaryInfo'})[0].text.strip()
                    jobsalary = job.find_all('div',{'class':'primaryInfo'})[1].text.strip()
                    self._jobs.append((jobname,jobloc,jobsalary))
            time.sleep(3)


    def get_jobs_list(self):
        return self._jobs

    def set_search_df(self):
        self._search_df = pd.DataFrame(self.get_jobs_list(),columns = ['jobname','location','salary'])

    def get_search_df(self):
        return self._search_df

if __name__ == '__main__':
    city_dict = {0:{'city':'raleigh','state':'nc'},1:{'city':'san diego','state':'ca'}}
    city_list = ['raleigh, nc','san diego, ca','seattle, wa']

    # jsObj = JobScraper()
    # jsObj.list_to_dict(city_list)
    # jsObj.job_search()
    # jsObj.set_search_df()
    # print(jsObj.get_search_df())
    # print(jsObj.get_search_df()['location'])
    # print(jsObj.get_search_df()['jobname'])
    # print(jsObj.get_search_df()['salary'])







