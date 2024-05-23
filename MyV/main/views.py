from django.shortcuts import render
from django.http import HttpResponse

def main_1(request):
    return render(request, 'main/main_1.html')

def upload_max_min(request):
    if request.method == 'POST':
        min_file = request.FILES.get('min-file', None)
        max_file = request.FILES.get('max-file', None)
        
        if min_file and max_file:
            upload_to_s3(min_file, max_file)
            return HttpResponse("Files uploaded successfully")
        else:
            return HttpResponse("Failed to upload files")
    
    return HttpResponse("Failed to upload files")

def main_2(request):
    return render(request,'main/loading.html')

def main_3(request):
    return render(request, 'main/main_3.html')