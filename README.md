# hw01-veterinary-clinic-service-api
Author: Антон Зайцев (МОВС 2023)

My homework 1 for the course "Industrial Development Tools" of the master's program "Machine Learning and Data-Intensive Systems" of the Higher School of Economics

## Task
The director of the veterinary clinic approached us and said:
"The clinic needs a microservice to store and update information for dogs!"
The director talked to the IT department, and they compiled the [documentation in OpenAPI format](clinic.yaml).

## Installing
- clone the GitHub repository
- create python 3.10 virtual environment `pyton -m venv .venv` or `poetry shell`
- activate virtual env `source venv/bin/activate` if using pip
- install packages `pip install -r requirements.txt` or `poetry install`

## Local launching
- run uvicorn server `uvicorn:main --reload`
- open in browser [http://localhost:8000/docs](http://localhost:8000/docs)
