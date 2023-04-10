from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(
        request,
        'single_pages/landing.html'
        #   templates/single_pages/landing/about_me
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )
