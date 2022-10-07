import time
import logging
from datetime import datetime

from dateutil.parser import parse
from dotenv import dotenv_values

from scraper.icbc import check_icbc
from sms.send_sms import text, call

#logging.basicConfig(filename="log.txt", level=logging.INFO)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
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


    dates: List = []
    if date_res:
        for date_item in date_res:
            #date_res: datetime =
            dates.append(parse(date_item))
    else: return

    #print(dates)
    #return

    earliest_date_string_version = dates[0].strftime('%m/%d/%Y')
    earliest_date_month = dates[0].strftime('%m')

    desired_months = ['12', '1']

    # If a prior scan was done, we keep track of the last scan date
    # so we don't end up spamming ourselves with calls or texts.
    last_checked_date = datetime.strptime(get_last_checked_date(), "%m/%d/%Y")

    for day in dates:
        day_month = day.strftime('%m')
        if day_month in desired_months:
            body= f"DESIRED APPOINTMENT DAY FOUND: {day.strftime('%m/%d/%Y')}"
            call(config["TWILIO_ACCOUNT_SID"],
                 config["TWILIO_ACCOUNT_AUTH_TOKEN"],
                 config["TWILIO_SMS_FROM"],
                 config["SMS_TO"],
                 body)
            return


    # Anything earlier than appointment date.
    if dates[0] <= my_appointment_date:
        """
        To keep from being notified twice.
        For November and December dates, repeating notifications
        is accepted.
        """

        if not parse(date_res[0]) == last_checked_date:
            body= f"EARLIER APPOINTMENT DAY FOUND: {earliest_date_string_version}"
            text(config["TWILIO_ACCOUNT_SID"],
                 config["TWILIO_ACCOUNT_AUTH_TOKEN"],
                 config["TWILIO_SMS_FROM"],
                 config["SMS_TO"],
                 body)

            # Overwrite last checked_date
            write_last_checked_date(earliest_date_string_version)
        else:
            logging.info("Already notified of this date.")
    else:
        logging.info(f"The earliest is at {earliest_date_string_version}")

if __name__ == "__main__":
    main()
