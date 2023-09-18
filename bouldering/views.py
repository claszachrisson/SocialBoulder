from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import WallSection, Route
from .forms import WallSectionForm

def room(request):
    # if p=-1 no parent, sx sy starting position. x y lengths
    walls = {1 : {'p':-1,'sx':35,'sy':5,'x':-25,'y':50},
             2 : {'p':1,'x':0,'y':50},
             3 : {'p':2,'x':50,'y':0},
             4 : {'p':3,'x':0,'y':50},
             5 : {'p':4,'x':-50,'y':0},
             6 : {'p':5,'x':0,'y':50},
             7 : {'p':6,'x':50,'y':0},
             8 : {'p':7,'x':0,'y':50},
             9 : {'p':8,'x':-50,'y':25},
             10 : {'p':9,'x':0,'y':50},
             11 : {'p':10,'x':25,'y':50},
             12 : {'p':11,'x':0,'y':50},
             13 : {'p':12,'x':50,'y':0},
             14 : {'p':-1,'sx':150,'sy':125,'x':-25,'y':-50},
             15 : {'p':14,'x':0,'y':-50},
             16 : {'p':15,'x':70,'y':20},
             17 : {'p':16,'x':0,'y':70},
             18 : {'p':-1,'sx':230,'sy':5,'x':50,'y':0},
             19 : {'p':18,'x':0,'y':50},
             20 : {'p':19,'x':0,'y':50},
             21 : {'p':20,'x':0,'y':50},
             22 : {'p':21,'x':-40,'y':50},
             23 : {'p':22,'x':0,'y':50},
             24 : {'p':23,'x':25,'y':50},
             25 : {'p':24,'x':0,'y':50},
             26 : {'p':25,'x':-50,'y':0},
             27 : {'p':26,'x':0,'y':50},
             28 : {'p':27,'x':50,'y':0}}
    
    # set starting positions for children and end positions
    for ~, w in walls.items():
        if w['p'] != -1:
            p = walls[w['p']]
            w['sx'] = p['x']
            w['sy'] = p['y']
        w['x'] += w['sx']
        w['y'] += w['sy']
    
    context = {
        'welcome_message' : ["Great day", "for a send?"],
        'walls' : walls
    }
    return render(request, "bouldering/room.html", context)

def wall_section(request, wall_id):
    try:
        wall_section = WallSection.objects.get(pk=wall_id)
    except WallSection.DoesNotExist:
        raise Http404("This wall does not exist")

    context = {
        'wall_section' : wall_section
    }
    return render(request, "bouldering/wallsection.html", context)

def add_send(request, route_id, user_id):
    nxt = request.GET.get("next", None)
    try:
        route = Route.objects.get(pk=route_id)
        user = User.objects.get(pk=user_id)
        route.users.add(user)
        route.save()
    except Route.DoesNotExist:
        raise Http404("This route does not exist")
    return redirect(nxt)

def remove_send(request, route_id, user_id):
    nxt = request.GET.get("next", None)
    try:
        route = Route.objects.get(pk=route_id)
        user = User.objects.get(pk=user_id)
        route.users.remove(user)
        route.save()
    except Route.DoesNotExist:
        raise Http404("This route does not exist")
    return redirect(nxt)

def upload_image(request, wall_id):
    wall_section = WallSection.objects.get(pk=wall_id)

    if request.method == "POST":
        form = WallSectionForm(request.POST, request.FILES, instance=wall_section, extra=request.POST.get('extra_field_count'))
        if form.is_valid():
            form.save()
            context = {
                'wall_section' : wall_section
            }
            return render(request, "bouldering/wallsection.html", context)
        else:
            raise Http404(form.errors)
    form = WallSectionForm(instance=wall_section)
    return render(request=request, template_name="bouldering/uploadimage.html", context={"form":form})
