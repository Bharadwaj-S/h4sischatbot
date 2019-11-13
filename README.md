# How to run
1. Create a Twilio account in www.twilio.com and register and verify your phone number. Also note down the Twilio provided automatic phone number
2. Download Python 3 and the required libraries from requirements.txt
3. In a terminal window navigate to the folder with all the files and type `python send_sms.py` or `python3 send_sms.py`
4. Open another terminal window in the folder and type `twilio phone-numbers:update "<your-twilio-phone-number> --sms-url="http://localhost:5000/sms`
5. Send a text to your twilio phone number and chat with the bot.
