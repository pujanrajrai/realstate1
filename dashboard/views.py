from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from accounts.models import MyUser
from decorator import is_user, is_admin_or_user, is_admin
from property.models import PropertyBookMark, Comments, Property, PropertyCategory
from myprofile.models import Profile


@is_admin_or_user()
def home(request):
    properties = Property.objects.all()
    context = {
        'total_properties': properties.count(),
        'total_comment': Comments.objects.all().count(),
        'total_property_categories': PropertyCategory.objects.all().count(),
        'total_users': MyUser.objects.all().count(),
        'total_book_marked': PropertyBookMark.objects.all().count(),
        'female': Profile.objects.filter(gender__name='FEMALE').count(),
        'male': Profile.objects.filter(gender__name='MALE').count(),
        'others': Profile.objects.filter(gender__name='OTHERS').count(),
        'apartment_count': properties.filter(category__category='APARTMENT').count(),
        'villa_count': properties.filter(category__category='VILLA').count(),
        'home_count': properties.filter(category__category='HOME').count(),
        'office_count': properties.filter(category__category='OFFICE').count(),
        'building_count': properties.filter(category__category='BUILDING').count(),
        'townhouse_count': properties.filter(category__category='TOWNHOUSE').count(),
        'shop_count': properties.filter(category__category='SHOP').count(),
        'garage_count': properties.filter(category__category='GARAGE').count(),
    }
    return render(request, 'dashboard/home.html', context)


@is_admin_or_user()
def property_visit_req(request):
    property_visit_req = PropertyBookMark.objects.filter(property__user=request.user)
    context = {"property_visit_req": property_visit_req}
    return render(request, 'dashboard/property_visit_req.html', context)


@is_admin()
def all_user(request):
    context = {
        'users': MyUser.objects.all()
    }
    return render(request, 'dashboard/users_list.html', context)


@is_admin_or_user()
def my_properties(request):
    context = {
        'properties': Property.objects.filter(user=request.user)
    }
    return render(request, 'property/property_list_view.html', context)


@is_admin_or_user()
def my_comment(request):
    context = {
        'comments': Comments.objects.filter(Q(property__user=request.user) | Q(user=request.user)).order_by(
            '-date_of_added')
    }
    return render(request, 'dashboard/my_comments.html', context)


@is_admin_or_user()
def remove_comment(request):
    if request.method == 'POST':
        try:
            Comments.objects.filter(Q(property__user=request.user) | Q(user=request.user)).filter(
                pk=request.POST['pk']).delete()
        except:
            pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def block_user(request, username):
    try:
        MyUser.objects.filter(username=username).update(is_active=False)
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unblock_user(request, username):
    try:
        MyUser.objects.filter(username=username).update(is_active=True)
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
