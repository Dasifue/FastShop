# Hello FastAPI

### It's my pet project with Asyncio and FastAPI - Fast Shop

## Installation

1. Clone repository
```bash
git clone https://...
```

2. Change directory
```bash
cd FastShop
```

3. Create Virtual Environment
```bash
python3.12 -m venv env
```

4. Activate env
* Unix
```bash
source env/bin/activate
```

* Windows (is this how windows users do this?)
```bash
env/Scripts/activate
```

5. Install all requirements
```bash
pip install -r requirements.txt
```
6. Open PSQL and create database :)

7. Create `.env` file and insert `DATABASE_URL` as in `.env.example`

8. Run application
```bash
python3.12 main.py create_tables
```

argument `create_tables` needs for table creation. It's optional for second project run