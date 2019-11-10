from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import chatbot

app = Flask(__name__)

companies = None  # To save the list of companies queried by user

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    global companies
    message_limit = 500  # To prevent sending the user a barrage of messages

    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    try:
        # Welcome Message
        if body == 'Wage Theft':
            resp.message("Thanks for using our service. Please enter the name of the company you're interested in")
        elif body.isdigit():
            body = int(body)
            
            # User has entered the number of the company from the list
            if body < 10000 and companies:
                company = companies[body - 1]
                msg = chatbot.final_response(company)
                resp.message(msg)

            # User has entered a zipcode
            elif body >= 10000:
                companies = chatbot.search_by_zip(companies, body)
                addresses = chatbot.all_addresses(companies)
                msg = str(chatbot.format_addresses(addresses))
                if len(msg) <= message_limit:
                    resp.message(msg)
                else:
                    resp.message(f"There are a lot of results for {body}. Please enter the zip code of the company.")
            else:
                resp.message("Please enter the name of the company you're interested in")
        else:
            companies = chatbot.chat(body)
            addresses = chatbot.all_addresses(companies)
            msg = str(chatbot.format_addresses(addresses))
            if len(msg) <= message_limit:
                resp.message(msg)
            else:
                resp.message(f"There are a lot of results for {body}. Please enter the zip code of the company.")
    except:
        resp.message("Sorry, we didn't quite get that. Please say that again")

    return str(resp)  # Output to the webhook - doesn't get sent to user

if __name__ == "__main__":
    app.run(debug=True)
