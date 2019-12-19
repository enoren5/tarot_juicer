from django.shortcuts import render


def work_orders(request):
    return render(request, 'work_orders/first.html')
