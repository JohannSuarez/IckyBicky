# IckyBicky
A web scraper for checking the earliest ICBC driving exam appointment you can book for.

The wait list for a driving test provided by ICBC is usually several months long.
This incentivizes rescheduling to nearer dates whenever possible in case someone cancels
their appointment, potentially saving you months of waiting.

Using Selenium, we can automate the process of logging into our ICBC accounts and acquiring the
earliest possible date we can book. If the acquired date is earlier than our originally booked
appointment, this means there is a new slot available that we can take.

# Configuration
Refer to the provded .env_example as reference for populating the environment variables
with your private information.

There are eight private variables required for running the script.
  - ICBC_LOGIN_URL
  - LOGIN_NAME
  - LOGIN_LICENSE_NUMBER
  - LOGIN_KEY_WORD
  - TWILIO_ACCOUNT_SID
  - TWILIO_ACCOUNT_AUTH_TOKEN
  - TWILIO_SMS_FROM
  - SMS_TO
  
While not a sensitive private variable, ICBC_LOGIN_URL is the url of the
login page required for logging in and viewing the available appointments. As such it is
expected to change over time, and is better off being a variable than being hardcoded.

LOGIN_NAME, LOGIN_LICENSE_NUMBER, LOGIN_KEY_WORD, are your private credentials that you input
in order to log in to your icbc.com account.

TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are credentials
you obtain from your Twilio console in order to send text message alerts (see: https://console.twilio.com/)

TWILIO_SMS_FROM is a number you have registered on your Twilio account that you can use to send
messages from. SMS_TO will be the recipient.
