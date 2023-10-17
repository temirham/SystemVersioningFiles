from django.http import HttpResponseNotFound, HttpResponseServerError

appologize = 'Something went wrong, im sorry :<'
def Default404Error(request, exception):
    return HttpResponseNotFound(f'<h1>Error(404)</h1><h3>Not found. <p>{appologize}</h3>')

def Default500Error(request):
    return HttpResponseServerError(f'<h1>Error(500)</h1><h3>Server error.<p>{appologize}</h3>')