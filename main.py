import time
import logging
from datetime import datetime

from dateutil.parser import parse
from dotenv import dotenv_values

from scraper.icbc import check_icbc
from sms.send_sms import text

logging.basicConfig(filename="log.txt", level=logging.DEBUG)
config = dotenv_values(".env")

def main():
    logging.debug("Starting...")
    my_appointment_date = datetime.strptime("11/22/2022", "%m/%d/%Y")
    start_time = time.time()

    date_res = None

    while not date_res:
        # False positive warnings coming from the type hinting of dotenv_values()
        date_res = check_icbc(config["ICBC_LOGIN_URL"], # type: ignore
                              config["LOGIN_NAME"],     # type: ignore
                              config["LOGIN_LICENSE_NUMBER"], # type: ignore
                              config["LOGIN_KEY_WORD"])       # type: ignore

    if date_res:
        date_res: datetime = parse(date_res)
    else: return

    print(time.time() - start_time)

    string_version = date_res.strftime('%m/%d/%Y')
    date_res_month = date_res.strftime('%m')
    print(date_res_month)
    print(type(date_res_month))

    desired_months = ['9', '10', '11']


    if date_res_month in desired_months:
        logging.debug("Really appointment date found...")
        body= f"REALLY EARLY APPOINTMENT DAY FOUND: {string_version}"
        print(body)
        text(config["TWILIO_ACCOUNT_SID"],
             config["TWILIO_ACCOUNT_AUTH_TOKEN"],
             config["TWILIO_SMS_FROM"],
             config["SMS_TO"],
             body)
        return


    if date_res <= my_appointment_date:
        body= f"EARLIER APPOINTMENT DAY FOUND: {string_version}"
        print(body)
        text(config["TWILIO_ACCOUNT_SID"],
             config["TWILIO_ACCOUNT_AUTH_TOKEN"],
             config["TWILIO_SMS_FROM"],
             config["SMS_TO"],
             body)
    else:
        print(f"The earliest is at {string_version}")

if __name__ == "__main__":
    main()
