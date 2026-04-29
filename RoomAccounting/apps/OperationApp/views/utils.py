from django.shortcuts import render


def result_page(request, result):
    return render(request, 'result.html', context={'result': result})
