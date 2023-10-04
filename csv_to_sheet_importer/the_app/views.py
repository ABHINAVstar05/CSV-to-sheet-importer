from django.shortcuts import render

# Create your views here.


def upload_csv(request) :
    return render(request, 'upload_csv.html')