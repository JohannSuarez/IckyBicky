import time
import logging
from datetime import datetime

from dateutil.parser import parse
from dotenv import dotenv_values

from scraper.icbc import check_icbc
from sms.send_sms import text, call

logging.basicConfig(filename="log.txt", level=logging.DEBUG)
config = dotenv_values(".env")


def get_last_checked_date() -> str:
    file1 = open("last_checked_date.txt","r")
    last_date = file1.read().splitlines()
    file1.close()
    return last_date[0]

def write_last_checked_date(date: str) -> str:
    file1 = open("last_checked_date.txt","w")
    file1.write(date)
    file1.close()
    pass


def main():
    logging.debug("Starting...")
    my_appointment_date = datetime.strptime("1/30/2023", "%m/%d/%Y")
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

    desired_months = ['12', '1']

    # If a prior scan was done, we keep track of the last scan date
    # so we don't end up spamming ourselves with calls or texts.
    print(get_last_checked_date())

    #last_checked_date = datetime.strptime("1/30/2023", "%m/%d/%Y")
    last_checked_date = datetime.strptime(get_last_checked_date(), "%m/%d/%Y")
    print(last_checked_date)

    if date_res_month in desired_months:
        if date_res_month == '12':
            body= f"DECEMBER APPOINTMENT DAY FOUND: {string_version}"
            call(config["TWILIO_ACCOUNT_SID"],
                 config["TWILIO_ACCOUNT_AUTH_TOKEN"],
                 config["TWILIO_SMS_FROM"],
                 config["SMS_TO"],
                 body)
            return
        else:
            # Something VERY early
            logging.debug("Really appointment date found...")
            body= f"REALLY EARLY APPOINTMENT DAY FOUND: {string_version}"
            print(body)
            '''
            text(config["TWILIO_ACCOUNT_SID"],
                 config["TWILIO_ACCOUNT_AUTH_TOKEN"],
                 config["TWILIO_SMS_FROM"],
                 config["SMS_TO"],
                 body)
            '''

            return


    # Anything earlier than appointment date.
    if date_res <= my_appointment_date:
        if not date_res == last_checked_date:
            body= f"EARLIER APPOINTMENT DAY FOUND: {string_version}"
            print(body)
            '''
            text(config["TWILIO_ACCOUNT_SID"],
                 config["TWILIO_ACCOUNT_AUTH_TOKEN"],
                 config["TWILIO_SMS_FROM"],
                 config["SMS_TO"],
                 body)
            '''

            write_last_checked_date(string_version)
            # Overwrite last checked_date
        else:
            print("Already notified of this date.")
    else:
        print(f"The earliest is at {string_version}")

if __name__ == "__main__":
    #get_last_checked_date()
    main()
