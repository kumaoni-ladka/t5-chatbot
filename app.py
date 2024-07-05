from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import cohere
 
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
 
# Initialize Cohere client
co = cohere.Client(api_key="a3R3APY9VT4Qeit34TbtUEbaro0i7vWwiH2ISWfB")
 
# Load the intents data
 
# Prepare the documents for Cohere
documents = [
    {
        "title": "greeting",
        "snippet": "<b>Hi! Hope you are doing great.<br><br> I'm your friendly Freddie, at your service!<br><br>I can take care of all of your questions which you have regarding the Organization. If I won't be able to answer any questions, I will note that down and try to work on it.<br>I can take care of your 'How', 'What', 'Where', 'When' and 'Who'.<br>So, What do you want to know?<br>"
    },
    {
        "title": "Replicon",
        "snippet": "Replicon is your new Global Time Management solution in Capgemini India for managing work time by submitting weekly timesheets and booking time off requests.<br>•To access Replicon, you can use your Single Sign-On (SSO) credentials or connect to the VPN for secure access.<br>•Additionally, you can download the Replicon mobile app from Microsoft Intune through your Work profile<br>For more information about Replicon, refer to <a class='button-style' href='https://talent.capgemini.com/media_library/Medias/Documents/Indian_Documents/Replicon_Global_Time_Management_SOP_V1.1.pdf' target='_blank'>this document</a>."
    },
    {
        "title": "TimeCard",
        "snippet": "You can fill or modify your timesheet <a class='button-style' href='https://talent.capgemini.com/in/pages/about_us/global_time_management/' target='_blank'>here</a>"
    },
    {
        "title": "Leaves",
        "snippet": "To apply leave, follow these <a class='button-style' href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW%2FApply%20Leave%2Epdf&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW' target='_blank'>steps</a>."
    },
    {
        "title": "Information",
        "snippet": "ServiceCentral is a platform where you can manage various IT-related services and requests.<br>For an overview of Service Central, view <a class='button-style' href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW%2FService%20Central%20Overview%2Epdf&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW' target='_blank'>this document</a>."
    },
    {
        "title": "Reimbursement",
        "snippet": "To fill expense reimbursement, check out <a class='button-style' href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW%2FFill%20Reimbursement%2Epdf&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW' target='_blank'>this guide</a>."
    },
    {
        "title": "Troubleshoot",
        "snippet": "Facing hardware/software issues? Find solutions <a class='button-style' href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW%2FHardware%26SoftwareIssue%2Epdf&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FHOW' target='_blank'>here</a>."
    },
    {
        "title": "Install",
        "snippet": "Need to install new software? Follow these <a class='button-style' href='https://servicecentral.capgemini.com/kb_view.do?sysparm_article=KB0119871&sysparm_rank=1&sysparm_tsqueryId=3a8e06a1db1d299016daf462f3961961' target='_blank'>instructions</a>. <br>Or<br>To get access to licensed software, refer to <a class='button-style' href='https://servicecentral.capgemini.com/sc?id=kb_article_view&sysparm_article=KB0120741&sys_kb_id=3779cbd4db69a5d46c9150d3f396197d&spa=1' target='_blank'>this article</a>."
    },
    {
        "title": "PING ID",
        "snippet": "Learn more about Ping ID <a class='button-style' href='https://groupit.capgemini.com/services/pcsecurity/pingid/' target='_blank'>here</a>."
    },
    {
        "title": "Access Card",
        "snippet": "Information about access cards can be found <a class='button-style' href='https://talent.capgemini.com/in/pages/about_us/global_business_lines_/infra_india/hr_corner/New_hire/' target='_blank'>here</a>."
    },
    {
        "title": "Learning Partners",
        "snippet": "Explore our learning partners <a class='button-style' href='https://capgemini.sharepoint.com/sites/universall/SitePages/Learning-Partners.aspx' target='_blank'>here</a>."
    },
    {
        "title": "HR queries",
        "snippet": "For HR queries, you can ask MAiA <a class='button-style' href='https://talent.capgemini.com/in/pages/supportfunctions/human_resources/' target='_blank'>here</a>."
    },
    {
        "title": "IT support",
        "snippet": "Get IT support from the Help Desk <a class='button-style' href='https://groupit.capgemini.com/it_contacts/' target='_blank'>here</a>."
    },
    {
        "title": "Fun Club",
        "snippet": "Join the Fun Club <a class='button-style' href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?OR=Teams%2DHL&CT=1719904688109&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA1MzEwMTQyMSIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FWHERE%2FFun%5FClub%2Epdf&viewid=d8de8c49%2D67ff%2D446b%2D860c%2D8b181c91e6bc&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FWHERE' target='_blank'>here</a>."
    },
    {
        "title": "Gym",
        "snippet": "At Capgemini, we understand that a healthy workforce is a productive workforce. That's why we have invested in creating gyms at different locations that caters to all fitness levels and preferences. Whether you're into cardio, weightlifting, or yoga, our gym has the equipment and space to accommodate your workout routine. Currently Capgemini is providing gym services in following Cities:<br><br>1. Mumbai<br>2. Chennai<br>3. Bengaluru<br>4. Hyderabad<br>5. Noida<br>6. Gurgaon<br>7. Pune."
    },
    {
        "title": "Gym Registration",
        "snippet": "To know more about the fee, the no. of gyms and registration, please go through the Gym registration form <a class='button-style' href='https://forms.office.com/e/JehuhqmxjB'>here</a>"
    },
    {
        "title": "Sports arena",
        "snippet": "Explore the Sports Arena details <a class='button-style' href='https://capgemini.sharepoint.com/sites/Freshers_Buddy/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FWHERE%2FSports%20Arena%2Epdf&viewid=d8de8c49%2D67ff%2D446b%2D860c%2D8b181c91e6bc&parent=%2Fsites%2FFreshers%5FBuddy%2FShared%20Documents%2FAttachments%2FWHERE' target='_blank'>here</a>."
    },
    {
        "title": "Library",
        "snippet": "Access our library resources <a class='button-style' href='https://talent.capgemini.com/in/pages/learning/library' target='_blank'>here</a>."
    },
    {
        "title": "Creche",
        "snippet": "Information about creche facilities can be found <a class='button-style' href='https://talent.capgemini.com/in/pages/Architects_of_Positive_Future/winspire_di/winspire_advancing_gender_balance/Child_care_benefits/creche_tie_up_details' target='_blank'>here</a>."
    }
]
 
# Run the chatbot
def get_response(user_input):
    # Get the response from Cohere
    response = co.chat(
        model="command-r-plus",
        message=user_input,
        documents=documents
    )
    return response.text
 
# Run Gunicorn server using subprocess
 
 
# Define Flask routes
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('message')
    elif request.method == 'GET':
        user_input = request.args.get('message')
    else:
        return "Method not allowed", 405
 
    if not user_input:
        return "No message provided", 400
 
    response = get_response(user_input)
    return jsonify({'response': response})
 
if __name__ == '__main__':
   app.run(debug=True)
