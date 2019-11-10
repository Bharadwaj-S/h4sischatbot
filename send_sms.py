from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import chatbot

app = Flask(__name__)

companies = None

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    global companies

    body = request.values.get('Body', None)
    message_limit = 500

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    try:
        if body == 'Wage Theft':
            resp.message("Thanks for using our service. Please enter the name of the company you're interested in")
        elif body.isdigit():
            body = int(body)
            if body < 10000 and companies:
                company = companies[body - 1]
                msg = chatbot.final_response(company)
                resp.message(msg)
            elif body >= 10000:
                new_companies = chatbot.search_by_zip(companies, body)
                msg = str(chatbot.all_results(new_companies))
                if len(msg) <= message_limit:
                    resp.message(msg)
                else:
                    resp.message(f"There are a lot of results for {body}. Please enter the zip code of the company.")
            else:
                resp.message("Please enter the name of the company you're interested in")
        else:
            companies = chatbot.chat(body)
            msg = str(chatbot.all_results(companies))
            if len(msg) <= message_limit:
                resp.message(msg)
            else:
                resp.message(f"There are a lot of results for {body}. Please enter the zip code of the company.")
    except Exception as e:
        resp.message(str(e))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
