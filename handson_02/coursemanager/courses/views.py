from django.http import HttpResponse


def index(request):
    return HttpResponse('Course Management API - Handson 02')
