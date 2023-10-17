from django.shortcuts import redirect


def index(request):
    return redirect('soft_loading:sl_filter', permanent=False, language='ru')

