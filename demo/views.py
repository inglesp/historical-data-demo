from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from demo.models import Practice


def index(request):
    # This ORM code is a bit hairy -- don't worry about understanding it!
    # It finds all practice records with the latest release_date for each code.
    #
    # So if our practice table has:
    #
    #  id | code | release_date
    # ----+------+--------------
    #   1 | A001 |   2024-01-01
    #   2 | A001 |   2024-02-01
    #   3 | A002 |   2024-01-01
    #   4 | A002 |   2024-02-01
    #
    # then it will return records 2 and 4.

    subquery = (
        Practice.objects.filter(code=OuterRef("code"))
        .order_by("-release_date")
        .values("release_date")[:1]
    )
    practices = Practice.objects.filter(release_date=Subquery(subquery)).order_by("name")
    ctx = {"practices": practices}
    return render(request, "index.html", ctx)


def practice(request, code):
    if "release_date" in request.GET:
        # Find the practice with the given date
        practice = Practice.objects.get(code=code, release_date=request.GET["release_date"])
    else:
        practice = Practice.objects.filter(code=code).order_by("release_date").last()

    earlier_version = (
        Practice.objects.filter(code=code, release_date__lt=practice.release_date)
        .order_by("release_date")
        .last()
    )
    earlier_release_date = earlier_version.release_date if earlier_version else None

    later_version = (
        Practice.objects.filter(code=code, release_date__gt=practice.release_date)
        .order_by("release_date")
        .first()
    )
    later_release_date = later_version.release_date if later_version else None

    ctx = {
        "practice": practice,
        "earlier_release_date": earlier_release_date,
        "later_release_date": later_release_date,
    }

    return render(request, "practice.html", ctx)
