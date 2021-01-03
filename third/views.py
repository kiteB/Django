from django.shortcuts import render, get_object_or_404, redirect
from third.models import Restaurant, Review
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg


# Create your views here.
def list(request):
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point')) # review 중 point의 평균
    paginator = Paginator(restaurants, 5)

    page = request.GET.get('page')  # third.list?page=1
    items = paginator.get_page(page)

    context = {
        'restaurants': items,
    }
    return render(request, 'third/list.html', context)


def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list')
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form': form})


def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        item = get_object_or_404(Restaurant, pk=request.POST.get('id'))
        password = request.POST.get('password', '')
        form = UpdateRestaurantForm(request.POST, instance=item)  # NOTE: instance 인자(수정대상) 지정

        if form.is_valid() and password == item.password:  # 비밀번호 검증 추가
            item = form.save()

    elif 'id' in request.GET:
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        form = RestaurantForm(instance=item)
        form.password = ''  # password 데이터를 비웁니다.
        return render(request, 'third/update.html', {'form': form})

    return HttpResponseRedirect('/third/list/')  # 리스트 화면으로 이동합니다.


def detail(request, id):
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'third/detail.html', {'item': item, 'reviews': reviews})
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('list/')
        return redirect('restaurant-detail', id=id)
    return render(request, 'third/delete.html', {'item': item})


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return redirect('restaurant-detail', id=restaurant_id)

    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item})
    return render(request, 'third/review_create.html', {'form': form, 'item': item})


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()

    return redirect('restaurant-detail', id=restaurant_id)


def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)

    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = {
        'reviews': items
    }
    return render(request, 'third/review_list.html', context)