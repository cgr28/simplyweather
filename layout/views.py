from django.shortcuts import render

# Create your views here.
def handler404(request, exception=None):
    return render(request, 'layout/404.html')

def handler500(request, exception=None):
    return render(request, 'layout/500.html')
