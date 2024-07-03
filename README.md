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
    
Note that if it says "address already in use", that (likely) means ollama is already running. From the Mac taskbar, you can always quit ollama so you can start and stop from command line. Make sure to run step 12 again if you do this.

![image](https://github.com/AD1616/HPC-Training-AI/assets/64157584/2547e651-3ee8-47bf-ba83-4e4eca0764e9)

Your current terminal is now running ollama, and will show any requests made to ollama. To continue with the next steps, keep this terminal running and open a new terminal window. Navigate to the directory where the cloned repository is located.

12. ```
    python load_sdsc_events_data.py
    ```
13. ```
    python load_sdsc_events_with_transcripts.py
    ```
14. ```
    python generate_all_dense_embeddings.py
    ```
15. ```
    python sparse_embeddings.py
    ```

If all of the above was done properly, you can now run:

```
python query.py <query>
```

where \<query\> is what you want to learn about.

```
python query.py "I want to learn about parallel computing"
```

For the web interface, run:

```
python app.py
```

Then navigate to [localhost](http://localhost:5000/). 

When finished, run:

```
./local_scripts/local_kill.sh
```

### Running after initial setup

1. ```
   ./local_scripts/start.sh
   ```
2. ```
   python app.py 
   ```

When finished, run:

```
./local_scripts/local_kill.sh
```


