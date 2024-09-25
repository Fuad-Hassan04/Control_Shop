from django.shortcuts import render , redirect , get_object_or_404 
from .models import *
from django.contrib.auth import authenticate , logout , login
from .forms import *
from django.http import JsonResponse , Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# customar create views
def add_customar(request):


    customer_type_choices = customar.CUSTOMER_TYPE_CHOICES

    if request.method == 'POST':
        form = CustomarForm(request.POST)
        if form.is_valid():
            customar1 = form.save(commit=False)
            customar1.user = request.user
            customar1.save()
            return redirect("index")
    else:
        form = CustomarForm()

    context = {
        'form': form,
        'types': customer_type_choices
    }

    return render(request, 'admin_panel/add_customar.html', context)


# HTMX GET request to load customer data in modal


     # POST request to update customer data
def update_customer(request , customer_id ):
    customar1 = get_object_or_404(customar, id=customer_id)

    try :
       customars = customar.objects.get(id=customer_id)
    except Exception as e :
      raise Http404(f"customar not found by your given id:{id}")
    
    if request.method == 'POST':
          name = request.POST.get('name')
          address = request.POST.get('address')
          fhone = request.POST.get('fhone')


          customars.name = name
          customars.address = address 
          customars.fhone = fhone

          customars.save()
          return redirect('customar_list')
    context = {
         'customar1':customar1
    }
    return render(request, 'admin_panel/update_customar.html',context)


     
   


def delete_customar(request):
    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')
        if delete_id:
            customar_to_delete = customar.objects.get(id=delete_id)
            customar_to_delete.delete()
            return JsonResponse({"success": True})
    return render(request, 'admin_panel/customar_list.html')

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

    name_mounth = mounth_name.objects.all()


    context = {
         'cost':cost,
         'total_hishab':total_hishab,
         'name_mounth':name_mounth
         
    }
    return render(request, 'admin_panel/user_profile.html',context) 
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

    costs = total_cost.objects.all()  # সমস্ত খরচের তালিকা নিয়ে আসা

    cost_with_hishab = []
    for cost in costs:
        total_cost_for_month = (
            cost.store_rent + cost.bill + cost.employs_sallary + cost.by_product_rate
        )
        cost_with_hishab.append({
            'cost': cost,
            'total_cost_for_month': total_cost_for_month
        })

    context = {
        'cost_with_hishab': cost_with_hishab
    }

    

    return render(request , 'admin_panel/total_cost.html' , context)



def customar_details(request , id ):

    customer = get_object_or_404(customar, id=id)
    detail = customar_ditail.objects.filter(customer=customer)
    context = {
         'detail':detail
    }
   
    

    return render(request , 'admin_panel/customar_detail.html',context)


def owed_details(request):
    owed = owed_detail.objects.all()
    context = {
        'owed':owed
    }
    return render(request , 'admin_panel/owed_dital.html'  , context)
def profit_details(request):
    detail = profit_detail.objects.all()
    context = {
        'detail':detail
    }
    return render(request , 'admin_panel/prfit_ditail.html' , context)

def create_owed_detail(request):
    customar_name = customar.objects.all()

    
    if request.method == 'POST':
          customer_id = request.POST.get('customar_name')
          customer_instance = customar.objects.get(pk=customer_id) 
          
          owed_money_for_product = request.POST.get('owed_money_for_product')
          given_money = request.POST.get('given_money')
          owed_money = request.POST.get('owed_money')
          
          if customer_instance and owed_money_for_product and given_money and owed_money:
              owed_detail.objects.create(
                owed_customer = customer_instance ,
                owed_money_for_product = owed_money_for_product,
                given_money = given_money , 
                owed_money = owed_money

                  
              )
              

          else : 
           massage = "please full all form "
          return redirect('owed_detail')
    context = {
        'customar_name':customar_name
    }
    return render(request , 'admin_panel/detail/create_owed.html' , context)

def create_customar_detail(request, id):
    customer = get_object_or_404(customar, id=id)
    
    if request.method == 'POST':
        form = AddDetailForm(request.POST)
        if form.is_valid():
            customar_detail = form.save(commit=False)
            customar_detail.customer = customer  # এখানে customer সঠিকভাবে সেট হচ্ছে
            customar_detail.save()
            return redirect("index")
        else:
            print(form.errors)  # ডিবাগ করার জন্য ফর্ম ত্রুটিগুলো দেখানো হচ্ছে
    else:
        form = AddDetailForm()

    return render(request, 'admin_panel/detail/create_customar_detail.html', {'form': form})


def update_customer_detail(request, id):
    customar1 = get_object_or_404(customar_ditail, id=id) # template e jate change korte na hoi tai customar1 dewa 

    try :
       details = customar_ditail.objects.get(id=id)
    except Exception as e :
      raise Http404(f"customar not found by your given id:{id}")
    
    if request.method == 'POST':
          buy_product = request.POST.get('buy_product')
          given_money = request.POST.get('taken_money')
          owed_money = request.POST.get('get_money')
          total_amount = request.POST.get('total_amount')


          details.buy_product = buy_product
          details.given_money = given_money 
          details.get_money = owed_money
          details.total_amount = total_amount

          details.save()
          return redirect('customar_detail', id=customar1.id)
    context = {
         'customar1':customar1
    }
    return render(request , 'admin_panel/detail/update_customer_detail.html' , context)


def add_cost(request):

    if request.method == 'POST':
       month1 = request.POST.get('month')
       store_rent = request.POST.get('store_rent')
       bill = request.POST.get('bill')
       employ_sallary = request.POST.get('employ_sallary')
       buy_product_list = request.POST.get('buy_product_list')
       buy_product_rate = request.POST.get('buy_product_rate')

       month1 = total_cost.name_mounth 
       if  month1 and store_rent and bill and employ_sallary and buy_product_list and buy_product_rate  :
            total_cost.objects.create(

                name_mounth = month1,
                store_rent = store_rent ,
                bill = bill ,
                employ_sallary = employ_sallary , 
                buy_product_list = buy_product_list,
                buy_product_rate = buy_product_rate

            )
            return  redirect("customar_list")
       
       else : 
           massage = "please full all form "

        
    return render(request , 'admin_panel/detail/add_cost.html')


def create_profit_detail(request): 

      

    if request.method == 'POST':

        product_name = request.POST.get('product_name')
        profit = request.POST.get('profit')
        extra = request.POST.get('extra')  or None 
        extra_profit = request.POST.get('extra_profit')  or None 
          
        if product_name and profit  :
              profit_detail.objects.create(
                product_name = product_name ,
                profit = profit,
                extra = extra , 
                extra_profit = extra_profit

                  
              )
              

        else : 
           return redirect('create_profit_detail')
        return redirect('profit_detail')

    return render(request , 'admin_panel/detail/add_profit_detail.html' )


def update_owed_detail(request , id ):
    customar1 = get_object_or_404(owed_detail, id=id) # template e jate change korte na hoi tai customar1 dewa 

    try :
       update_owed = owed_detail.objects.get(id=id)
    except Exception as e :
      raise Http404(f"customar not found by your given id:{id}")
    
    if request.method == 'POST':
          product_name = request.POST.get('product_name')
          given_money = request.POST.get('given_money')
          owed_money = request.POST.get('owed_money')
     


          update_owed.owed_money_for_product = product_name
          update_owed.given_money = given_money 
          update_owed.owed_money = owed_money
          

          update_owed.save()
          return redirect('owed_detail', id=customar1.id)
    context = {
         'customar1':customar1
    }

    return render(request , 'admin_panel/detail/update_owed.html' , context)



def update_profit_detail(request , id ):
    customar1 = get_object_or_404(profit_detail, id=id) # template e jate change korte na hoi tai customar1 dewa 

    try :
       update_profit = profit_detail.objects.get(id=id)
    except Exception as e :
      raise Http404(f"customar not found by your given id:{id}")
    
    if request.method == 'POST':
          product_name = request.POST.get('product_name')
          profit = request.POST.get('profit')
          extra = request.POST.get('extra') or None
          extra_profit = request.POST.get('extra_profit') or None
     


          update_profit.product_name = product_name
          update_profit.profit = profit 
          update_profit.extra = extra
          update_profit.extra_profit = extra_profit
          

          update_profit.save()
          return redirect('profit_detail')
    context = {
         'customar1':customar1
    }

    return render(request , 'admin_panel/detail/update_profit.html' , context)