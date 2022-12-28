
## COMMANDS

#### 1. Install dependencies
- pip install -r requirements.txt

#### 2. Run server
- python3 server.py

#### 3. Generate Distribution
- python3 gui.py

#### 4. Run Locust
- locust -f locustfile.py,custom_load.py --csv=results/load -H http://127.0.0.1:8000 -L WARNING
