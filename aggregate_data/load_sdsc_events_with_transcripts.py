from tqdm import tqdm
import pymongo
import json


def insert_data_to_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    local_db = client["hpc_training_raw_local_db"]
    db_events_col = local_db["sdsc_events_with_transcripts"]

    events_data = json.load(open('events.json'))

    index = 0
    for event in tqdm(events_data):
        events_data[event]["_id"] = index
        events_data[event]["Title"] = events_data[event]["title"]
        if events_data[event]["vid_link"] is None:
            events_data[event]["Link"] = "Link not provided."
        else:
            events_data[event]["Link"] = events_data[event]["vid_link"]
        transcript_path = f"transcripts/{event}.json"
        try:
            transcript_data = json.load(open(transcript_path))
            events_data[event]["transcript"] = transcript_data
        except:
            transcript_data = "Not currently provided."
            events_data[event]["transcript"] = transcript_data
        db_events_col.insert_one(events_data[event])
        index += 1


if __name__ == "__main__":
    insert_data_to_db()