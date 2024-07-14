import requests
from bs4 import BeautifulSoup as bs
import csv
from itertools import zip_longest

page_num = 0
Keyword = input("write what you are searching for --> ")

# Initialize lists to store data
job_title = []
company_names = []
location = []
employement_type = []
links = []

# Loop through pages
while True:
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q={Keyword}&start={page_num}")
    source = result.content
    soup = bs(source, "lxml")

    # Find page limit
    if page_num == 0:
        page_limit_text = soup.find("strong").text.replace(",", "")
        page_limit = int(page_limit_text)
        
    # Find all job elements
    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    companies = soup.find_all("div", {"class": "css-d7j1kk"})
    locations = soup.find_all("span", {"class": "css-5wys0k"})
    employement_type_element = soup.find_all("span", {"class": "css-1ve4b75 eoyjyou0"})

    # Break the loop if no more jobs are found
    if not job_titles:
        print("Pages ended")
        break

    # Extract data
    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text.strip())
        
        company_name = companies[i].find("a", {"class": "css-17s97q8"})
        company_names.append(company_name.text.strip())

        location.append(locations[i].text.strip())


        employement_type.append(employement_type_element[i].text.strip())

        
        link = job_titles[i].find("a")
        links.append(link.attrs["href"])


    page_num += 1
    print("Page switched")

# Export data to CSV
files_list = [job_title, company_names, location, employement_type,links]
exported = zip_longest(*files_list)

with open("D:\wuzzuf_Search_tool.csv", "w", newline="", encoding="utf-8") as output_file:
    wr = csv.writer(output_file)
    wr.writerow(["job title", "company names", "location", "employment type","links"])
    wr.writerows(exported)
