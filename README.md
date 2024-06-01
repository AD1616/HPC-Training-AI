# HPC Training AI

Helps a user find relevant training materials in topics related to High Performance Computing. 

### Running locally on MacOS

1. Install [ollama](https://ollama.com/)
2. ```
   ollama pull nomic-embed-text
   ```
3. ```
   ollama run llama3
   ```
4. Install [mongodb community edition](https://www.mongodb.com/try/download/community)
5. ```
   git clone https://github.com/AD1616/HPC-Training-AI.git
   ```
6. ```
   cd HPC-Training-AI/local_scripts
   ```
7. ```
    pip install -r requirements.txt
   ```
8. ```
    chmod +x local_kill.sh
    ```
9. ```
    ./local_kill.sh
    ```
10. ```
    chmod +x local_setup.sh
    ```
11. ```
    ./local_setup.sh
    ```
    
Note that if it says "address already in use", that (likely) means ollama is already running. From the Mac taskbar, you can always quit ollama so you can start and stop from command line. Make sure to run step 11 again if you do this.

![image](https://github.com/AD1616/HPC-Training-AI/assets/64157584/2547e651-3ee8-47bf-ba83-4e4eca0764e9)

Your current terminal is now running ollama, and will show any requests made to ollama. To continue with the next steps, keep this terminal running and open a new terminal window. Navigate to the directory where the cloned repository is located.

12. ```
    python load_sdsc_events_data.py
    ```
13. ```
    python generate_embeddings.py
    ```

If all of the above was done properly, you can now run:

```
python query.py <query>
```

where \<query\> is what you want to learn about, such as:

```
python query.py "I want to learn about Cyberinfrastructure"
```

When finished, run:

```
./local_scripts/local_kill.sh
```

### Notes

This will be migrated to a cluster at SDSC, which means:
* SDSC ollama service will be used
* mongodb database will be hosted on cluster (for raw data)
* chroma database will be hosted on cluster (for vector embeddings)

Data from other sources will be included, which means:
* mongodb database will have multiple collections, theoretically one for each source
* each collection needs to have a proper vector embedding in the chroma database

Miscellaneous
* mongodb database on local is called: "hpc_training_raw_local_db"
* mongodb collection for SDSC events within database is called: "sdsc_events"