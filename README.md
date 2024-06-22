<h1>KL Subway Outlets Finder Project (Backend)</h1>
<h2>Introduction</h2>

The <b>KL Subway Outlets Finder Project</b> is a project which webscrap the Subway outlets in Kuala Lumpur area from the <a href="https://subway.com.my/find-a-subway">offical outlet locator</a>. 

This repository contains the backend script for this project.  
It should be used together with the <a href="https://github.com/TeoJJss/subway-kl-frontend">frontend script</a>. 

The backend script is built using Python and FastAPI, with the support of Selenium, SQLite3 and NLTK.  

<h2>Prerequisites</h2>

<b>Python 3.11</b> is used for the development.  
Please create a virtual environment and install all libraries:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
After that, the server should be able to launch through the following command:  
```
uvicorn app:app
```
The backend server should be launched simultaneously when the frontend script is launched. 

<h2>Important Notes</h2>

- There are some configurations can be editted at `config.py`
- This backend script should be used together with the frontend script at https://github.com/TeoJJss/subway-kl-frontend. The frontend script will send HTTP requests to the APIs in this backend server. 
- The backend server is hosted at the 8000 port by default. If it is changed, please change the URL at frontend script.