# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACa8d63de6f10787427b81dad99e6b775c'
auth_token = '416a389edf8e0963d0d6967ae8960e58'
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12024109147',
                     to='+15107015152'
                 )

print(message.sid)


