from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os
from config import DB_NAME, URL, TARGET_LOCATION
from db import execute_sql, create_db, read_kl_outlets
from fastapi.responses import JSONResponse

def find_kl_outlets():
    driver = webdriver.Chrome()
    driver.get(URL)

    if not os.path.isfile(DB_NAME):
        create_db()

    insert_sql = """
                    INSERT INTO KL_OUTLETS (NAME, ADDRESS, OPERATING_HOUR, WAZE_LINK, LONGITUDE, LATITUDE)
                    VALUES 
                """

    try:
        # Perform search
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fp_searchAddress'))  
        )
        search_input.send_keys(TARGET_LOCATION)
        search_input.send_keys(Keys.RETURN)  

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'fp_locationlist')))
        search_results = driver.find_elements(By.CSS_SELECTOR, '.fp_listitem')  # Search results

        i=0
        
        json_resp = {
            "data": []
        }

        # Loop through the search results
        for result in search_results:
            waze=latitude=longitude=""
            target=result.text.split("\n")
            tmp_data = {
                "name": "",
                "address": "",
                "operating_hour": "",
                "waze_link": ""
            }
            try:
                classname = result.get_attribute('class').split(" ")[1]
                latitude = result.get_attribute("data-latitude")
                longitude = result.get_attribute("data-longitude")

                waze = driver.find_element(By.CSS_SELECTOR, f'.{classname} a:nth-of-type(2)').get_attribute('href')
                tmp_data['name'] = target[0]
                tmp_data['address'] = target[1]
                tmp_data['operating_hour'] = target[2]
                tmp_data['waze_link'] = waze

                json_resp['data'].append(tmp_data)
                insert_sql += f"('{target[0]}', '{target[1]}', '{target[2]}', '{waze}', '{longitude}', '{latitude}'),"
            except:
                pass
            i+=1
        json.dump(json_resp, open("result.json", "w"), indent=6)

        # Insert into DB
        execute_sql(insert_sql[:-1]) # Skip the last comma in SQL
    except Exception as e:
        print("Error: ", e)
    finally:
        driver.quit()

def kl_outlets():
    find_kl_outlets()
    kl_outlets = read_kl_outlets()

    resp = []

    for outlet in kl_outlets:
        tmp_resp = {
            "name": outlet[0],
            "address": outlet[1],
            "operating_hour": outlet[2],
            "waze": outlet[3],
            "longitude": outlet[4],
            "latitude": outlet[5]
        }
        resp.append(tmp_resp)
    
    return JSONResponse(content=resp, status_code=200)