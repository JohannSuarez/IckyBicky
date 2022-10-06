from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
TO-DO:
Let a systemd service call this every five minutes.

If an earlier appointment is found, check if user is notified already within this day.
If not, message the user and tick a boolean called is_notified_today.
"""

def check_icbc(icbc_login_url: str,
               login_name: str,
               login_license_Number: str,
               login_key_word: str) -> str | None:

    # Instance of Firefox webdriver is created.
    driver = webdriver.Firefox()
    url = icbc_login_url

    # The driver.get method will navigate to a page given by the URL.
    # WebDriver will wait until the page has fully loaded ( that is, the "onload" event has fired. )
    # before returning control to your test or script. Be aware that if your page uses a lot of AJAX
    # on load then WebDriver may not know when it has completely loaded.
    driver.get(url)

    assert "Book a road test" in driver.title
    date_result: str | None = None

    # Grabbing the form information, and the buttons to click.
    try:
        name = driver.find_element(By.ID, "mat-input-0")
        license_num = driver.find_element(By.ID, "mat-input-1")
        key_word = driver.find_element(By.ID, "mat-input-2")
        tos_checkbox = driver.find_element(By.XPATH,"//input[@id='mat-checkbox-1-input']/./..")
        sign_in_button = driver.find_element(By.CLASS_NAME, "mat-raised-button")

        # Logging in
        name.send_keys(login_name)
        license_num.send_keys(login_license_Number)
        key_word.send_keys(login_key_word)

        tos_checkbox.click()
        sign_in_button.click()

        WebDriverWait(driver, 15).until(EC.url_changes(url))
        time.sleep(1.4)

        # Booking a resched to arrive to appointment selection
        resched_appointment = driver.find_element(By.CLASS_NAME, "mat-raised-button")
        resched_appointment.click()
        dialog_box = driver.find_element(By.CLASS_NAME, "mat-dialog-container")
        yes_button_xpath="//app-cancel/div/div/div[contains(@class, 'mat-dialog-actions')]/button[contains(@class, 'mat-raised-button')]"
        yes_button = dialog_box.find_element(By.XPATH, yes_button_xpath)
        yes_button.click()

        # Inputting a partial search in the form so that suggestions pop up
        location = driver.find_element(By.ID, "mat-input-3")
        location.clear()
        location.send_keys("Nanaimo")
        #time.sleep(0.2)
        #location.send_keys("BC")

        # Letting suggestions load
        time.sleep(2.0)
        # Select the first suggestion

        first_result = driver.find_elements(By.CLASS_NAME, "mat-option")
        #first_result = driver.find_elements(By.ID, "mat-option")
        first_result[0].click()


        # Click the "Search" button.
        search_button = driver.find_element(By.CLASS_NAME, "mat-raised-button")
        search_button.click()

        # Clicking the closest location.
        nearest_location = driver.find_element(By.CLASS_NAME, "appointment-location-wrapper")
        nearest_location.find_element(By.CLASS_NAME, "department-title")
        print(nearest_location.text)
        if "Nanaimo" not in nearest_location.text:
            print(nearest_location.text)
            print("Wrong Venue")
            raise Error("Wrong venue.")

        nearest_location.click()

        # Letting the schedules load.
        WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "date-title"))
            )

        closest_date = driver.find_element(By.CLASS_NAME, "date-title")
        date_result = closest_date.text
    except Exception:
        print(Exception)
        print("Website issue")
    finally:
        driver.close()

    return date_result
