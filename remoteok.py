import requests
from bs4 import BeautifulSoup

URL = "https://remoteok.io"


def extract_job(html):
    title = html.find("h2", {"itemprop": "title"})
    if title is None:
        return None
    title = title.text
    company = html['data-company']
    location = html.find("div", {"class": "location"})
    if location is None:
        location = "[Not Found]"
    else:
        location = location.text
    job_id = html['data-href']
    return {"title": title, "company": company, "location": location,
            "apply_link": f"{URL}{job_id}"}


def extract_jobs(term):
    jobs = []
    print(f"Scrapping remoteok")
    result = requests.get(f"{URL}/remote-{term}-jobs")
    soup = BeautifulSoup(result.text, "html.parser")
    print(soup)
    results = soup.find_all("tr", {"class": "job"})
    for r in results:
        job = extract_job(r)
        jobs.append(job)
    return jobs


def get_jobs(term):
    jobs = extract_jobs(term)
    return jobs
