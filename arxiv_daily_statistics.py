import os, sys
from copy import copy
import json
from datetime import date


today = date.today()
d1 = today.strftime("%Y-%m/%d")

cache_folder = "cache/%s/" % d1
cache_file = "%s/arxiv-cs.html" % cache_folder
os.makedirs(cache_folder, exist_ok=True)

if not os.path.exists(cache_file):
    import requests
    url = "https://arxiv.org/list/cs/new"
    r = requests.get(url)
    html = r.text
    with open(cache_file, "w") as fp:
        fp.write(html)
else:
    with open(cache_file, "r") as fp:
        html = fp.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

s = soup.find(class_="list-dateline").text.split("announced")[-1].strip()
day, month, year = [_.strip() for _ in s.split(",")[-1].split()]
info_folder = "info/%s-%s/%s" % (year, month, day)
os.makedirs(info_folder, exist_ok=True)


count = 0
information = []
for dl in soup.find_all("dl"):
    count += len(dl.find_all("dd"))
    dds = dl.find_all("dd")
    dts = dl.find_all("dt")

    dds_dts = zip(dds, dts)

    for (dd, dt) in dds_dts:
        # arXiv id
        list_identifier = dt.find(class_="list-identifier")
        id = list_identifier.a.text

        # title
        list_title = dd.find_all(class_="list-title")[0]
        if list_title.span.attrs["class"] == ["descriptor"]:
            list_title.span.extract()
        title = list_title.text.strip()

        # authors
        list_authors = dd.find_all(class_="list-authors")
        authors = [_.text for _ in list_authors[0].find_all("a")]

        # subjectives / areas
        list_subjects = dd.find_all(class_="list-subjects")[0]
        if list_subjects.span.attrs["class"] == ["descriptor"]:
            list_subjects.span.extract()
        subjectives = list_subjects.text.strip()
        subjectives = [_.strip() for _ in subjectives.split(";")]

        paper_info = {
            "id": id,
            "title": title,
            "authors": authors,
            "subjectives": subjectives
        }
        information.append(paper_info)



with open("%s/paper_info.json" % info_folder, "w") as fp:
    json.dump(information, fp, indent=2)

with open("%s/paper_counts.txt" % info_folder, "w") as fp:
    fp.write(str(count))

print(count)
print(information[:3])
