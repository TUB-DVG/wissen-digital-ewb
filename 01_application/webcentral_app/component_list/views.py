from django.shortcuts import render

# Create your views here.
def components(request):
    return render(request, 'component_list/components.html')

def dataProcessing(request):
    return render(request, 'component_list/dataProcessing.html')