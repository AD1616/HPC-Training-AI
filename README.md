# HPC Training AI

Helps a user find relevant training materials in topics related to High Performance Computing. 

### Running locally on MacOS

1. Install [ollama](https://ollama.com/)
2. ```
   ollama pull nomic-embed-text
   ```
3. ```
   ollama pull llama3
   ```
   
Step 4 is optional, only if you want to try different chat models.

4. ```
   ollama pull gemma
   ```

5. Install [mongodb community edition](https://www.mongodb.com/try/download/community)

6. ```
   git clone https://github.com/AD1616/HPC-Training-AI.git
   ```
7. ```
   cd HPC-Training-AI/local_scripts
   ```
8. ```
   pip install -r requirements.txt
   ```
9. ```
   chmod +x local_kill.sh
   ```
10. ```
    ./local_kill.sh
    ```
11. ```
    chmod +x local_setup.sh
    ```
12. ```
    ./local_setup.sh
    ```
    
Note that if it says "address already in use", that (likely) means ollama is already running. From the Mac taskbar, you can always quit ollama so you can start and stop from command line. Make sure to run step 12 again if you do this.

![image](https://github.com/AD1616/HPC-Training-AI/assets/64157584/2547e651-3ee8-47bf-ba83-4e4eca0764e9)

Your current terminal is now running ollama, and will show any requests made to ollama. To continue with the next steps, keep this terminal running and open a new terminal window. Navigate to the directory where the cloned repository is located.

13. ```
    python load_sdsc_events_data.py
    ```
14. ```
    python load_sdsc_events_with_transcripts.py
    ```
15. ```
    python generate_embeddings.py
    ```

If all of the above was done properly, you can now run:

```
python query.py <query> <model>
```

where \<query\> is what you want to learn about and \<model\> is a LLM model you pulled from ollama, such as:

```
python query.py "I want to learn about Cyberinfrastructure" "llama3"
```

```
python query.py "I want to learn about parallel computing" "gemma"
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

Data
* mongodb database on local is called: "hpc_training_raw_local_db"
* mongodb collection for SDSC events within database is called: "sdsc_events"
