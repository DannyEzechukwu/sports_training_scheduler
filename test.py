import unittest
import server

import athlete_crud
import coach_crud
import event_crud

from server import app
from model import db, connect_to_db

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

chrome_driver = "/Users/dannyezechukwu/Desktop/selenium_chrome_driver/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

connect_to_db(app)

class AppTest(unittest.TestCase):
    
    # setUpClass runs once before all test methods
    # are run
    def setUp(self):
            self.client = app.test_client()
            app.config['TESTING'] = True

    #Home Page unittest
    def test_home_page(self):
        client = server.app.test_client()
        result = client.get("/")
        self.assertIn(b"GAINZ", result.data)

    # Corey Brooks coach log in unittest
    # Should be redirected to homepage because session is not started until
    # coach or athlete logs in
    def test_corey_brooks_coach_login(self):
        client = server.app.test_client()
        result = client.get("/coach/1/CoreyBrooks")

        self.assertIn(b"Redirecting...", result.data)
    
    # Mary Walters athlete log in unittest
    # Should be redirected to homepage because session is not started until
    # coach or athlete logs in
    def test_mary_walters_athlete_login(self):
        client = server.app.test_client()
        result = client.get("/athlete/2/MaryWalters")
        self.assertIn(b"Redirecting...", result.data)

    # New Athlete creation integration test
    def test_new_athlete_creation(self):
        result = self.client.post("/new_athlete_account/json",
                                  data={"new-athlete-fname" : "Mark",
                                        "new-athlete-lname" : "Weaver",
                                        "new-athlete-username" : "mweaver",
                                        "new-athlete-email" : "mweaver@gmail.com",
                                        "new-athlete-password" : "test"},
                                  follow_redirects=True)
        self.assertIn(b"valid athlete", result.data)
        athlete = athlete_crud.get_athlete_by_username("mweaver")
        db.session.delete(athlete)
        db.session.commit()
    
    # New Coach creation integration test
    def test_new_athlete_creation(self):
        result = self.client.post("/new_coach_account/json",
                                  data={"new-coach-fname" : "Leanne",
                                        "new-coach-lname" : "Thomas",
                                        "new-coach-username" : "lthomas",
                                        "new-coach-email" : "lthomas@gmail.com",
                                        "new-coach-password" : "test"},
                                  follow_redirects=True)
        self.assertIn(b"valid coach", result.data)
        coach = coach_crud.get_coach_by_username("lthomas")
        db.session.delete(coach)
        db.session.commit()


    # Athlete login and event selection end to end test
    def test_get_favorites(self):
        username = "tchandler"
        password = "test"
        start_date = "01/01/2024"
        end_date = "01/06/2024"
        driver.get("http://localhost:5000/")
        time.sleep(3)
        driver.find_element(By.ID,"athletes").click()
        time.sleep(3)
        driver.find_element(By.ID, "athlete-username").send_keys(username)
        time.sleep(3)
        driver.find_element(By.ID, "athlete-password").send_keys(password)
        time.sleep(3)
        driver.find_element(By.ID, "athlete-submit").click()
        time.sleep(3)
        driver.find_element(By.ID, "past-sessions").click()
        time.sleep(3)
        driver.find_element(By.ID, "future-sessions").click()
        time.sleep(3)
        driver.find_element(By.ID, "add-sessions").click()
        time.sleep(3)
        driver.find_element(By.ID, "selected-start-date").send_keys(start_date)
        time.sleep(3)
        driver.find_element(By.ID, "selected-end-date").send_keys(end_date)
        time.sleep(3)
        driver.find_element(By.ID, "athlete-form-submit-1").click()
        time.sleep(3)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.PAGE_UP)
        time.sleep(2)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.PAGE_UP)
        time.sleep(2)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.PAGE_UP)
        time.sleep(3)
        driver.find_element(By.ID, "event-schedule-94").click()
        time.sleep(3)
        driver.find_element(By.ID, "coach-94-0").click()
        time.sleep(3)
        driver.find_element(By.TAG_NAME, value = "dialog").send_keys(Keys.END)
        time.sleep(3)
        driver.find_element(By.ID, "athlete-form-submit-2").click()
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert.accept()
        time.sleep(3)
        driver.find_element(By.ID, "log-out").click()
        time.sleep(5)
        driver.quit()
        print("Success")

    

if __name__ =="__main__":
    unittest.main()