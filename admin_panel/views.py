from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from django.contrib.auth import authenticate , logout , login
from .forms import CustomarForm
customar

# customar create views 

def add_customar(request):
    customer_type_choices = customar.CUSTOMER_TYPE_CHOICES

    if request.method == 'POST':
        form = CustomarForm(request.POST)
        if form.is_valid():
            customar1 = form.save(commit=False)
            customar1.user = request.user
            customar1.save()
            return redirect("add_or")
    else:
        form = CustomarForm()

    context = {
        'form': form,
        'types': customer_type_choices
    }

    return render(request, 'admin_panel/add_customar.html', context)


# add now or 
def add_or(request):
     return render(request , 'admin_panel/add_or.html' )


def index(request):
    total_customers = customar.objects.count()
    total_money = customar_ditail.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0      
    total_owed = customar_ditail.objects.aggregate(total=models.Sum('get_money'))['total'] or 0
    context = {
        'total_customers': total_customers,
        'total_money':total_money,
        'total_owed':total_owed
    }
    return render(request , 'admin_panel/index.html',context)

# sign up 
def sign_up(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_con = request.POST.get('conform_password')
            if password != password_con:
                return redirect('sign_up')   
            else:
                my_user = User.objects.create_user(name,email,password)
                my_user.save()
                return redirect('sign_up')

        return render(request , 'admin_panel/includes/signup.html')

def sign_in(request):
     if request.method == 'POST':
          name = request.POST.get('name')
          password = request.POST.get('password')
          user = authenticate(request,username=name,password=password) #$ note ekhane username e dewa lagbe 
          if user is not None:
               login(request,user)
               return redirect('index')
          else :
               return redirect('sign_in')
   
     return render(request, 'admin_panel/includes/sign_in.html') 
def sign_out(request):
     logout(request)
     return redirect('index') 

def user_profile(request):
    cost = total_cost.objects.all()
    cost_with_hishab = []
    for c in cost:
        total_hishab = c.store_rent + c.bill + c.employs_sallary + c.by_product_rate
        cost_with_hishab.append({
            'cost': c,
            'total_hishab': total_hishab
        })
    context = {
         'cost':cost,
         'total_hishab':total_hishab
         
    }
    return render(request, 'admin_panel/user_profile.html') 
def customar_list(request):

    customars = customar.objects.all()
    customer_type = request.GET.get('type')
    if customer_type in ['Regular', 'Non-Regular']:
          customars = customar.objects.filter(customer_type=customer_type)
    else:
          customars = customar.objects.all()

    context = {
        'customars': customars,
        
    }

    return render(request , 'admin_panel/customar_list.html', context)

def total_costs(request):
     cost = total_cost.objects.all()
     #if cost.exists():
        
       # first_cost = cost.first()
      #  store_rent = first_cost.store_rent
       # bill = first_cost.bill
       # employ_sallary = first_cost.employs_sallary
      #  product_rate = first_cost.by_product_rate
     cost_with_hishab = []
     for c in cost:
        total_hishab = c.store_rent + c.bill + c.employs_sallary + c.by_product_rate
        cost_with_hishab.append({
            'cost': c,
            'total_hishab': total_hishab
        })

    # else:
        
        #total_hishab = 0
     context={
          'cost':cost,
          'cost_with_hishab':cost_with_hishab
     }
     return render(request , 'admin_panel/total_cost.html' , context)

def test(request):

    return render(request , 'admin_panel/test.html')

def customar_detail_by_modal(request):
    detail = customar_ditail.objects.all()
    context = {
         'detail':detail
    }

    return render(request , 'admin_panel/htmx/customar_detail.html',context)