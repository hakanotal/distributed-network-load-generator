## Commands

#### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

#### 2. Run server

```powershell
python3 server.py
```

#### 3. Generate Distribution

```powershell
python3 gui.py
```

#### 4. Run Locust

```powershell
locust -f locustfile.py,shape.py --csv=loadresults/load -H http://127.0.0.1:8000 --run-time 60 -L WARNING 
```

#### 5. Run Docker Compose

```powershell
docker-compose up --build --force-recreate -d --scale cdl-worker=2
```