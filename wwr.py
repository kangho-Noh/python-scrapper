import requests
from bs4 import BeautifulSoup

URL = "https://weworkremotely.com"


def extract_job(html):
    title = html.find("span", {"class": "title"})
    if title is None:
        return None
    title = title.text
    company = html.find("span", {"class": "company"})
    if company is None:
        company = "[Not Found]"
    else:
        company = company.text

    location = html.find("span", {"class": "region"})
    if location is None:
        location = "[Not Found]"
    else:
        location = location.text
    url = html.find_all('a')[1]['href']
    return {"title": title, "company": company, "location": location, "apply_link": f"{URL}{url}"}


def extract_jobs(term):
    jobs = []
    print(f"Scrapping {term} on weworkremotely")
    result = requests.get(f"{URL}/remote-jobs/search?term={term}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    for r in results:
        job = extract_job(r)
        jobs.append(job)
    return jobs


def get_jobs(term):
    jobs = extract_jobs(term)
    return jobs
