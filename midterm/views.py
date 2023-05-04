from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from midterm.models import Staff

def index(request):
    return render(
        request,
        'midterm/index.html',
        {}, #  추가 데이터는 여기에 보내면 됨
        #   templates/single_pages/landing/about_me
    )

def list(request):
    return render(
        request,
        'midterm/list.html',
    )

#   staff_list.html찾음 -> list.html으로 지정
class StaffList(ListView):
    model = Staff
    template_name = 'midterm/list.html'

class StaffCard(DetailView):
    model = Staff
    template_name = 'midterm/name_card.html'

class StaffCard2(DetailView):
    model = Staff
    template_name = 'midterm/name_card2.html'


'''
class name_card(DetailView):
    model = Staff
    template_name = 'midterm/name_card.html'

class name_card2(DetailView):
    model = Staff
    template_name = 'midterm/name_card2.html'
'''
