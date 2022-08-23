from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_sms(twilio_account_sid: str,
             twilio_account_auth_token: str,
             twilio_sms_from: str,
             sms_to: str):

    client = Client(twilio_account_sid, twilio_account_auth_token)

    message = client.messages \
        .create(
            body="Test message",
             from_=twilio_sms_from,
             to=sms_to
         )
