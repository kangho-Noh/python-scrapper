import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("ul", {"class": "pagination-list"})
    spans = pagination.find_all("span")
    spans = spans[:-2]
    pages_num = []
    for span in spans:
        pages_num.append(int(span.string))
    max_page = pages_num[-1]
    return max_page


def extract_job(html, page):
    title = html.find("h2", {'class': 'title'}).find(
        "a", {"class": "jobtitle"})["title"]
    company = html.find("span", {'class': 'company'})
    company_anchor = company.find('a')
    if(company_anchor is not None):
        company = company_anchor.string
    else:
        company = company.string
    company = str(company).strip()
    location = html.find("div", {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']

    return {'title': title, 'company': company, 'location': location,
            "link": f"https://www.indeed.com/viewjob?jk={job_id}", 'page': page}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page}")
        result = requests.get(URL+f"&start{page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            jobs.append(extract_job(result, page))
    return jobs


def get_jobs():
    last_pages = get_last_page()
    jobs = extract_jobs(last_pages)
    return jobs
