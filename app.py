from flask import Flask, jsonify
from flask_cors import CORS
import cohere


# Load pretrained model and tokenizer
co = cohere.Client(api_key="a3R3APY9VT4Qeit34TbtUEbaro0i7vWwiH2ISWfB")

app = Flask("__name__")
CORS(app)

# Define questions and context\
docs = [
        {
            "title": "Replicon",
            "snippet": "You can fill or modify your timesheet <a href='https://talent.capgemini.com/in/pages/about_us/global_time_management/' target='_blank'>here</a>."
        },
        {
            "title": "Service Central",
            "snippet": "To fill expense reimbursement, check out <a href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW%2FFill%20Reimbursement%2Epdf&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW' target='_blank'>this guide</a>."
        },
        {
            "title": "PING ID",
            "snippet": "Learn more about Ping ID <a href='https://groupit.capgemini.com/services/pcsecurity/pingid/' target='_blank'>here</a>."
        },
        {
            "title": "Access Card",
            "snippet": "Information about access cards can be found <a href='https://talent.capgemini.com/in/pages/about_us/global_business_lines_/infra_india/hr_corner/New_hire/' target='_blank'>here</a>."
        },
        {
            "title": "Learning Partners",
            "snippet": "Explore our learning partners <a href='https://capgemini.sharepoint.com/sites/universall/SitePages/Learning-Partners.aspx' target='_blank'>here</a>."
        },
        {
            "title": "Where Page",
            "snippet": "Join the Fun Club <a href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?OR=Teams%2DHL&CT=1719904688109&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA1MzEwMTQyMSIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FWHERE%2FFun%5FClub%2Epdf&viewid=d8de8c49%2D67ff%2D446b%2D860c%2D8b181c91e6bc&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FWHERE' target='_blank'>here</a>."
        },
        {
            "title": "Who Page",
            "snippet": "Learn about your organization <a href='https://capgemini.sharepoint.com/sites/GenGarage/SitePages/Meet-the-Team.aspx?xsdata=MDV8MDJ8fGQ0ZDk0OTIxZGRmNTQ4NGI0ZDQ2MDhkYzlhNTk2YmVifDc2YTJhZTVhOWYwMDRmNmI5NWVkNWQzM2Q3N2M0ZDYxfDB8MHw2Mzg1NTQ5NTYwMzMxMTc1MTB8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMMk5vWVhSekx6RTVPbVJqTVRRNFlqazFOREJqT0RSa1ptWmlNak14TmpKak5UQmxZMlF6WkdObFFIUm9jbVZoWkM1Mk1pOXRaWE56WVdkbGN5OHhOekU1T0RrNE9EQXlPVFEwfGJmZjVkYWRmYzBhMTRiYTg0ZDQ2MDhkYzlhNTk2YmVifGQxZGNkY2NiOWE4NTRjNmM4N2FkMWIyMWVkMmRjODEx&sdata=V1hxbFB5QUhQaXNTbEpiVHY3NjV5M1BUWSsxUjRyendOcnZwb0NpOEVEST0=&ovuser=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61,jafrin-shajini.j@capgemini.com&OR=Teams-HL&CT=1719910786773&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA1MzEwMTQyMSIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ==' target='_blank'>here</a>."
        },
        {
            "title": "Gen Garage Clubs",
            "snippet": "Join Gen Garage Clubs <a href='https://forms.office.com/r/g0nyiHhin' target='_blank'>here</a>."
        }
    ]


@app.route('/input/<text>')
def send_output(text):
    message = co.chat(
        model="command-r-plus",
        message=text,
        documents=docs
    )
    op = message.text
    return jsonify({'data': op})


if __name__ == "__main__":
    app.run(debug=True)
