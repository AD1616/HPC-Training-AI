import requests
import pymongo
from bs4 import BeautifulSoup


def get_num_materials():
    url = "https://search-pilot.operations.access-ci.org/hpc-ed-v1/?q=*"

    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    pages = soup.find("div", id="results")
    materials_element = pages.find("div", class_="col-md-8")
    text_element = materials_element.find("h6", class_="h6")
    return int(text_element.text.split()[0])


def get_page_material_links(url: str):
    base_url = "https://search-pilot.operations.access-ci.org"
    material_links = []
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    search_titles = soup.find_all("h3", class_="search-title")
    for search_title in search_titles:
        link_element = search_title.find("a")
        link = base_url + link_element['href']
        material_links.append(link)

    return material_links


def extract_material_metadata():
    material_metadata = []
    base_url = "https://search-pilot.operations.access-ci.org/hpc-ed-v1/?q=*&page="
    count = 0
    page_number = 1
    total_materials = get_num_materials()
    while count < total_materials:
        page_url = base_url + str(page_number)
        page_links = get_page_material_links(page_url)
        for material_link in page_links:
            page = requests.get(material_link, verify=False)
            soup = BeautifulSoup(page.content, "html.parser")

            material_metadata.append({})
            current_material = material_metadata[len(material_metadata) - 1]

            card = soup.find("div", class_="card")
            title = card.find("a", class_="navbar-brand").text
            table = card.find("table", class_="table table-striped table-bordered")
            table_rows = table.find_all("tr")

            current_material["Title"] = title

            for table_row in table_rows:
                table_data = table_row.find_all("td")
                key = table_data[0].text
                value = table_data[1].text
                current_material[key] = value

            count += 1
            if count % 20 == 0:
                print(f"{count} links retrieved.")
        page_number += 1

    return material_metadata


def insert_materials_to_db():
    hpc_ed_data = extract_material_metadata()

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    local_db = client["hpc_training_raw_local_db"]
    db_hpc_ed_col = local_db["hpc_ed"]

    events_in_db = db_hpc_ed_col.count_documents({})

    if events_in_db < len(hpc_ed_data):
        print (f"{hpc_ed_data} materials to insert.")
        index = 0
        db_hpc_ed_col.delete_many({})
        for material in hpc_ed_data:
            material_document = material
            material_document['_id'] = index
            db_hpc_ed_col.insert_one(material_document)
            index += 1
            if index % 20 == 0:
                print(f"{index} materials inserted.")
        print("HPC_ED materials inserted to database.")
    else:
        print("Database already up to data with HPC_ED materials.")


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    insert_materials_to_db()
