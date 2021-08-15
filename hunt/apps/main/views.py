from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Challenge, Class


@login_required
def index(request):
    if request.user.is_participant():
        """
        Challenges fall into one of three statuses with respect to the user:
            - available (user can complete)
            - completed (completed by users's class)
            - locked (can only be completed by one class and has been completed)
        """
        challenges_completed_by_class = set(Class.objects.get(year=str(request.user.graduation_year)).challenges_completed.all())
        challenges_dict = dict()
        for c in Challenge.objects.all():
            if c in challenges_completed_by_class:
                challenges_dict[c.id] = [c, "completed"]
            elif c.locked:
                challenges_dict[c.id] = [c, "locked"]
            else:
                challenges_dict[c.id] = [c, "available"]
        return render(request, 'main/index.html', context={"challenges_dict": challenges_dict})
    else:
        return redirect(reverse("main:overview"))

@login_required
def overview(request):
    data = sorted([(c.year, c.get_points()) for c in Class.objects.all()])
    return render(request, 'main/overview.html', context={'data': data})
    
@login_required
def validate_flag(request):
    if request.is_ajax() and request.user.is_participant():
        challenge = get_object_or_404(Challenge, id=int(request.POST.get("challenge_id")))
        flag = request.POST.get("flag")
        if flag == challenge.flag:
            if not challenge.locked:
                request.user.challenges_done.add(challenge)
                if challenge.exclusive:
                    challenge.locked = True
                challenge.save()
                hoco_class = Class.objects.get(year=str(request.user.graduation_year))
                hoco_class.challenges_completed.add(challenge)
                hoco_class.save()
            response = {"result": "success"}
        else:
            response = {"result": "failure"}
        return JsonResponse(response)
    else:
        return PermissionDenied