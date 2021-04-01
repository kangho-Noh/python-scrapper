import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs"
# https://stackoverflow.com/jobs/521213


def get_last_page():
    result = requests.get(f"{URL}?q=python")
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"}).find_all("a")
    print("last page")
    print(pagination[-2])
    return int(pagination[-2].find("span").text)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class": "mb4"}).find_all(
        "span", recursive=False)
    # span 안에 span이 또 있어서 그건 안가져오기 위함
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {"title": title, "company": company, "location": location,
            "apply_link": f"{URL}/{job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page:{page}")
        result = requests.get(f"{URL}?q=python&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for r in results:
            job = extract_job(r)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
