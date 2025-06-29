import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://weworkremotely.com/categories/remote-data-jobs"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Jobs are inside a <section> with id "category-remote-data-jobs" and inside <ul class="jobs">
section = soup.find('section', id='category-remote-data-jobs')
if section:
    jobs_ul = section.find('ul', class_='jobs')
    if jobs_ul:
        jobs = jobs_ul.find_all('li', recursive=False)
    else:
        jobs = []
else:
    jobs = []

job_list = []

for job in jobs:
    # There are some <li> that are just spacers or headers; filter those
    if 'view-all' in job.get('class', []):
        continue
    try:
        link_tag = job.find('a', href=True)
        link = "https://weworkremotely.com" + link_tag['href'] if link_tag else ''

        company = job.find('span', class_='company')
        company = company.text.strip() if company else ''

        title = job.find('span', class_='title')
        title = title.text.strip() if title else ''

        region = job.find('span', class_='region')
        region = region.text.strip() if region else ''

        job_list.append({
            'Job Title': title,
            'Company': company,
            'Location': region,
            'Job URL': link
        })
    except Exception as e:
        continue

df = pd.DataFrame(job_list)
df.to_csv('weworkremotely_jobs.csv', index=False)

print(f"✅ Scraped {len(df)} job listings and saved to 'weworkremotely_jobs.csv'")
