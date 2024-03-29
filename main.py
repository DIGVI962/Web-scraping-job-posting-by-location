import requests
from bs4 import BeautifulSoup
import argparse


def scrape_jobs(location=None):
    if location:
        URL = (
            f"https://www.monster.com/jobs/search/"
            f"?q=Software-Developer&where={location}"
        )
    else:
        URL = "https://www.monster.com/jobs/search/?q=Software-Developer"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="ResultsContainer")
    return results


def filter_jobs_by_keyword(results, word):
    filtered_jobs = results.find_all(
        "h2", string=lambda text: word in text.lower()
    )
    for f_job in filtered_jobs:
        link = f_job.find("a")["href"]
        print(f_job.text.strip())
        print(f"Apply here: {link}\n")


def print_all_jobs(results):
    job_elems = results.find_all("section", class_="card-content")

    for job_elem in job_elems:
        title_elem = job_elem.find("h2", class_="title")
        company_elem = job_elem.find("div", class_="company")
        location_elem = job_elem.find("div", class_="location")
        if None in (title_elem, company_elem, location_elem):
            continue
            # print(job_elem.prettify())
        print(title_elem.text.strip())
        link_elem = title_elem.find("a")
        print(link_elem["href"])
        print(company_elem.text.strip())
        print(location_elem.text.strip())
        print()
