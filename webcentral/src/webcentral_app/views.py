from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, Http404

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def custom_400_view(request, exception):
    return render(request, '400.html', status=400)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def test_400(request):
    return custom_400_view()

def test_403(request):
    return custom_403_view()

def test_404(request):
    return custom_404_view()

def test_500(request):
    return custom_500_view()