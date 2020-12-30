from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader
from datetime import datetime
import random


# Create your views here.
def index(request):
    now = datetime.now()
    context = {
        'current_date': now
    }
    return render(request, 'first/index.html', context)


def select(request):
    context = {}
    return render(request, 'first/select.html', context)


def result(request):
    chosen = int(request.GET['number'])  # GET으로 전달된 것은 string!
    results = []

    # 만약 수가 범위를 초과하지 않으면 결과 값에 미리 선택한 수를 넣는다.
    if 1 <= chosen <= 45:
        results.append(chosen)

    # 값을 꺼낼 박스를 마련한다.
    box = []
    for i in range(0, 45):
        if chosen != i + 1:
            box.append(i + 1)

    # 랜덤하게 뒤섞는다.
    random.shuffle(box)

    # results 개수가 6개가 될 때 까지 값을 하나씩 꺼낸다.
    while len(results) < 6:
        results.append(box.pop())

    context = {
        'numbers': results
    }
    return render(request, 'first/result.html', context)