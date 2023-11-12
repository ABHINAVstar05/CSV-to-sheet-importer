from django.shortcuts import render, redirect
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Create your views here.


def filter(request, file_name) :
    df = pd.read_json(request.session.get('df'))
    df.to_csv()
    columns = list(df.columns)

    if request.method == 'GET' :
        return render(request, 'filters.html', {'columns': columns})
    
    else :
        data = request.POST
        selected_columns = data.getlist('cols')
        
        for col in columns :
            if col not in selected_columns :
                df = df.drop([col], axis = 1)

        # Authenticate with Google Sheets API using credentials.json
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        cred = ServiceAccountCredentials.from_json_keyfile_name('the_app/credentials.json', scope)
        gc = gspread.Client(cred)

        # Create a new Google Sheet
        spreadsheet = gc.create(file_name)
        spreadsheet.share('', perm_type='anyone', role='writer')
        worksheet = spreadsheet.get_worksheet(0)

        # Write data from DataFrame to Google Sheet
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

        # View the Google Sheet in the default web browser
        #spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
        spreadsheet_url = spreadsheet.url
        return redirect(spreadsheet_url)
    

def upload_csv(request) :
    if request.method == 'GET' :
        return render(request, 'upload_csv.html')
    
    else :
        file = request.FILES['file']
        allowed_extensions = ['csv']
        file_extension = file.name.split('.')[-1]
        file_name = file.name.split('.')[0]

        error_message = None

        if file_extension not in allowed_extensions :
            error_message = 'File is not in supported format.'
            return render(request, 'upload_csv.html', {'error' : error_message})
        
        df = pd.read_csv(file)
        request.session['df'] = df.to_json()
        return redirect(filter, file_name)
    