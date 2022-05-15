from django.contrib import messages
from django.db.models import F, Q
from django.shortcuts import render

from property.models import Property, State, PropertyStatus, PropertyCategory, PropertyBookMark, Comments
from django.http import Http404, HttpResponseRedirect

from .forms import ContactForm
from decorator import is_user, is_admin_or_user, is_admin
from datetime import datetime


# Create your views here.
def home(request):
    properties = Property.objects.filter(is_available=True).filter(is_blocked=False)

    context = {
        'properties': properties.order_by('-total_click')[:6],
        'states': State.objects.all(),
        'properties_status': PropertyStatus.objects.all(),
        'properties_categories': PropertyCategory.objects.all(),
        'apartment_count': properties.filter(category__category='APARTMENT').count(),
        'villa_count': properties.filter(category__category='VILLA').count(),
        'home_count': properties.filter(category__category='HOME').count(),
        'office_count': properties.filter(category__category='OFFICE').count(),
        'building_count': properties.filter(category__category='BUILDING').count(),
        'townhouse_count': properties.filter(category__category='TOWNHOUSE').count(),
        'shop_count': properties.filter(category__category='SHOP').count(),
        'garage_count': properties.filter(category__category='GARAGE').count(),
    }
    # to differentiate between bookmarked and non bookmarked proties
    try:
        bookmarked = PropertyBookMark.objects.filter(user=request.user)
        bookmarked_properties = []
        for bookmark in bookmarked:
            bookmarked_properties.append(bookmark.property)
        context['bookmarked_properties'] = bookmarked_properties
    except:
        pass

    return render(request, 'home/home.html', context)


def property_desc(request, pk):
    try:
        property = Property.objects.get(pk=pk)
        Property.objects.filter(pk=pk).update(total_click=F('total_click') + 1)

        comments = Comments.objects.filter(property__pk=pk).order_by('-date_of_added')
    except Property.DoesNotExist:
        raise Http404
    context = {
        'property': property,
        'comments': comments
    }

    try:
        is_requested = PropertyBookMark.objects.filter(user=request.user).filter(property__pk=pk).filter(
            is_vist_req=True).exists()
        context['is_requested'] = is_requested

    except:
        pass
    return render(request, 'home/property_desc.html', context)


# for searching properties
def property_search(request):
    context = {
        'properties': Property.objects.filter(is_available=True).filter(is_blocked=False).order_by('-total_click')[:6],
        'states': State.objects.all(),
        'properties_status': PropertyStatus.objects.all(),
        'properties_categories': PropertyCategory.objects.all()
    }
    if request.method == 'GET':
        if request.GET['state']:
            state = request.GET['state']
        else:
            state = 'any'

        if request.GET['category']:
            category = request.GET['category']
        else:
            category = 'any'

        if request.GET['status']:
            status = request.GET['status']
        else:
            status = 'any'
        properties = Property.objects.filter(is_available=True).filter(is_blocked=False)

        # user search properties logic
        try:
            if request.GET['price']:
                price = int(request.GET['price'])
                context['price'] = price
                if price == 100000:
                    properties = properties.filter(price__lte=100000)
                elif price == 1000000:
                    properties = properties.filter(price__gt=100000).filter(price__lte=1000000)
                elif price == 5000000:
                    properties = properties.filter(price__gt=1000000).filter(price__lte=5000000)
                elif price == 10000000:
                    properties = properties.filter(price__gt=5000000).filter(price__lte=10000000)
                elif price == 10000001:
                    properties = properties.filter(price__gt=10000000)
                else:
                    properties = properties.filter(price__lt=0)
        except:
            pass

        # searching through different criteria
        if state != 'any':
            properties = properties.filter(location_state__name=state)
        if category != 'any':
            properties = properties.filter(category__category=category)
        if status != 'any':
            properties = properties.filter(status__status=status)
        if properties.count() == 0:
            context['no_data'] = 'The Property is not available in this search Criteria'
        context['properties'] = properties
        context['p_state'] = state
        context['p_category'] = category
        context['p_status'] = status

        try:
            bookmarked = PropertyBookMark.objects.filter(user=request.user)
            bookmarked_properties = []
            for bookmark in bookmarked:
                bookmarked_properties.append(bookmark.property)
            context['bookmarked_properties'] = bookmarked_properties
        except:
            pass

    return render(request, 'home/property_search.html', context)


@is_admin_or_user()
def bookmark(request):
    if request.method == 'POST':
        try:
            PropertyBookMark.objects.create(
                user=request.user,
                property=Property.objects.get(pk=request.POST['property_id'])
            )
        except:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin_or_user()
def request_visit(request):
    if request.method == 'POST':
        try:
            property_bookmark = PropertyBookMark.objects.filter(user=request.user).filter(
                property__pk=request.POST['property_id'])
            if property_bookmark.exists():
                property_bookmark.update(is_vist_req=True)
            else:
                PropertyBookMark.objects.create(
                    user=request.user,
                    property=Property.objects.get(pk=request.POST['property_id']),
                    is_vist_req=True
                )
                
        except:
            print("error")
            pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin_or_user()
def comment(request):
    if request.method == 'POST':
        try:
            property_id = request.POST['property_id']
            comment = Comments.objects.filter(user=request.user).filter(property__pk=property_id).order_by(
                '-date_of_added').first()
            date1 = datetime.utcnow()
            date2 = comment.date_of_added.replace(tzinfo=None)
            difference = date1 - date2
            seconds = difference.seconds

            if seconds < 60:
                messages.success(request, 'Comment after sometime', extra_tags={'comment_error_message'})
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            Comments.objects.create(
                user=request.user,
                property=Property.objects.get(pk=request.POST['property_id']),
                comment=request.POST['comment']
            )
            messages.success(request, 'Comment Added Successfully', extra_tags={'comment_success_message'})
        except:
            messages.success(request, 'something went wrong', extra_tags={'comment_error_message'})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin_or_user()
def my_bookmark(request):
    context = {'bookmarks': PropertyBookMark.objects.filter(user=request.user).filter(is_vist_req=False)}
    return render(request, 'home/bookmark.html', context)


@is_admin_or_user()
def my_visit_req(request):
    context = {'bookmarks': PropertyBookMark.objects.filter(user=request.user).filter(is_vist_req=True)}
    return render(request, 'home/property_visit_req.html', context)


@is_admin_or_user()
def remove_watchlist(request):
    try:
        PropertyBookMark.objects.filter(Q(property__user=request.user) | Q(user=request.user)).filter(
            property=Property.objects.get(pk=request.POST['property_id'])).delete()
    except:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def contactus(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            context['message'] = 'Contact form submitted successfully'
        else:
            context['message'] = form.errors
    return render(request, 'home/contactus.html', context)
