from django.shortcuts import render

# Create your views here.


def upload_csv(request) :
    if request.method == 'GET' :
        return render(request, 'upload_csv.html')

    else :
        file = request.FILES['file']
        print(file.name)
        allowed_extensions = ['csv']
        file_extension = file.name.split('.')[-1]

        if file_extension not in allowed_extensions :
            print('File type not allowed')
        else :
            print('CSV file found')

        return render(request, 'upload_csv.html')