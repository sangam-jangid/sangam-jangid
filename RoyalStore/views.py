from django.shortcuts import render

def Home(request):
    return render(request, 'website/home.html' )

def Contact(request):
    return render(request, 'website/contact.html')
