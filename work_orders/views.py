from django.shortcuts import render


def first_work_order(request):
    return render(request, 'work_orders/first_work_order.html')


def second_work_order(request):
    return render(request, 'work_orders/second_work_order.html')
