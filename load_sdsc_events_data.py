import requests
import pymongo
from bs4 import BeautifulSoup


def get_event_links():
    base_url = "https://www.sdsc.edu"
    url = "https://www.sdsc.edu/news_and_events/events.html"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    event_list = soup.find("ul", class_="list-events")

    events = event_list.find_all("li", class_="event")

    event_links = []

    for event in events:
        event_link_element = event.find("a")
        event_link = base_url + event_link_element['href'][2:]
        event_links.append(event_link)

    return event_links


"""
Returns Hashmap
Key:   Title
Value: Content
"""
def extract_event_text():
    event_links = get_event_links()

    events_data = {}

    for event_link in event_links:
        event_page = requests.get(event_link)
        soup = BeautifulSoup(event_page.content, "html.parser")

        event_title = soup.find("h1").text
        event_content = soup.find("div", class_="event-description").text
        events_data[event_title] = event_content

    return events_data


"""
Events put in MongoDB

Importantly, we implement custom unique ID's for entries.
This helps us easily get metadata when integrating with langchain.
"""
def insert_events_to_db():
    events_data = extract_event_text()

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    local_db = client["hpc_training_raw_local_db"]
    db_events_col = local_db["sdsc_events"]

    events_in_db = db_events_col.count_documents({})

    if events_in_db < len(events_data):
        index = 0
        db_events_col.delete_many({})
        for key, value in events_data.items():
            event_document = {'_id': index, 'Title': key, 'Content': value}
            db_events_col.insert_one(event_document)
            index += 1
        print("Events inserted to database.")
    else:
        print("Database already up to data with SDSC events.")


if __name__ == "__main__":
    insert_events_to_db()

