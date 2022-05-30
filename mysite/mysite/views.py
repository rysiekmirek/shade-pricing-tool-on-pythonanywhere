from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse,  HttpResponseRedirect
from .models import Shade, ShadeData, Pricing, PricingName
from django.views.generic import View
import requests
import math
import uuid
from .utils import render_to_pdf
from django.template.loader import get_template
from .forms import CustomUserCreationForm
from django.db.models import Q


@login_required(login_url='/login/')
def pricing(request, pk, selected_shade_type=''):


    shade_types = ('Grupa_A_Vegas', 'Grupa_A_DN_plus_50', 'Grupa_A_DN_plus_100',
    'Grupa_B_Żaluzje_białe', 'Grupa_B_Żaluzje_kolorowe', 'Grupa_B_Żaluzje_perforowane',
    'Grupa_C_Plisy', 'Grupa_C_Plisy_gumowane', 'Grupa_C_Rolety_zaciągane_od_dołu',
    'Grupa_C_Rolety_zaciągane_od_dołu plus 100', 'Grupa_D_Bambus_listwa_25mm', 'Grupa_D_Bambus_listwa_50mm',
    'Grupa_D_Drewno_listwa_25mm', 'Grupa_D_Drewno_listwa_50mm', 'Grupa_E_Wolnowiszące' )


    if request.method == 'POST':
        selected_shade_type=''
        r = request.POST
        if 'f_adjustment' in r:
            pricing_adjustment = r['f_adjustment']
            PricingName.objects.filter(id=pk).update(adjustment=pricing_adjustment)
            pricings_list = Pricing.objects.filter(pricingName_id=pk)
            for pricing in pricings_list:
                shade_price_adjusted = round(((pricing.shadePrice * float(pricing_adjustment))/100),2)
                Pricing.objects.filter(pricingName_id=pk, shadePrice=pricing.shadePrice).update(shadePriceAdjusted=shade_price_adjusted)

        elif 'f_pricing_comment' in r:
            comment = r['f_pricing_comment']
            PricingName.objects.filter(id=pk).update(comment=comment)

        else:
            session_id = request.session._get_or_create_session_key()
            window_name = r["f_window_name"]
            shade_type = r["f_shade"]
            shade_color = r["f_color"]
            shade_width = float(r["f_width"].replace(",", "."))
            shade_height = float(r["f_height"].replace(",", "."))

            shade_type_id = str(Shade.objects.get(name=shade_type).id)
            shade_type_id_corrected = shade_type_id.replace("-", "")

            shade_width_rounded = math.ceil(shade_width / 10) * 10 # price is calculated for dimension rounded up to every 10 cm
            shade_height_rounded = math.ceil(shade_height/10) * 10 # price is calculated for dimension rounded up to every 10 cm

            if shade_type == 'Grupa_E_Wolnowiszące':
                price_from_db = ShadeData.objects.get(width=shade_width_rounded, height=shade_height, shade_id=shade_type_id_corrected).price
            else:
                price_from_db = ShadeData.objects.get(width=shade_width_rounded, height=shade_height_rounded, shade_id=shade_type_id_corrected).price

            if price_from_db == 0:
                messages.warning(request, 'Nie ma możliwości dodania rolety o wybranych wymiarach, wybierz inne wartości')
                return HttpResponseRedirect('/pricing/'+ str(pk))


            pricing_name = PricingName.objects.get(id=pk)
            shade_price_adjusted = round(((pricing_name.adjustment * price_from_db) / 100),2)

            Pricing.objects.create(windowName= window_name , shadeType=shade_type, shadeColor=shade_color ,
                shadeWidth=shade_width, shadeHeight=shade_height ,  shadePrice=price_from_db , shadePriceAdjusted=shade_price_adjusted , sessionId=session_id, pricingName_id=pk)

    pricings_list = Pricing.objects.filter(pricingName_id = pk)
    pricing_name = PricingName.objects.get(id=pk)

    sum_of_prices = 0
    sum_of_prices_adjusted = 0
    for pricing in pricings_list:
        sum_of_prices += pricing.shadePrice
        sum_of_prices_adjusted += pricing.shadePriceAdjusted

    sum_of_prices_adjusted = round(sum_of_prices_adjusted,2)
    sum_of_prices = round(sum_of_prices, 2)

    if selected_shade_type != '':
        shade = Shade.objects.get(name= selected_shade_type)
        my_context = {
        'pricings_list': pricings_list,
        'sum_of_prices': sum_of_prices,
        'sum_of_prices_adjusted': sum_of_prices_adjusted,
        'pricing_name_id': pk,
        'pricing_name': pricing_name.name,
        'pricing_username': pricing_name.username,
        'pricing_adjustment': pricing_name.adjustment,
        'colors': shade.colors.split(','),
        'selected_shade_type': selected_shade_type,
        'shade_types': shade_types,
        'pricing_comment': pricing_name.comment,
        'min_width' : shade.min_width,
        'max_width' : shade.max_width,
        'min_height' : shade.min_height,
        'max_height' : shade.max_height,
        }
        return render(request, "pricing.html", my_context)


    my_context = {
        'pricings_list': pricings_list,
        'sum_of_prices': sum_of_prices,
        'sum_of_prices_adjusted': sum_of_prices_adjusted,
        'pricing_name_id': pk,
        'pricing_name': pricing_name.name,
        'pricing_username': pricing_name.username,
        'pricing_adjustment': pricing_name.adjustment,
        'colors': '',
        'shade_types': shade_types,
        'pricing_comment': pricing_name.comment,
    }

    return render(request, "pricing.html", my_context)


def login_user(request):

    page='login'

    if request.user.is_authenticated:
        return redirect ('/pricing-start/')

    if request.method == 'POST':
        username = request.POST['f_username']
        password = request.POST['f_password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Nie znaleziono użytkownika')
            return render(request, 'login-register.html', {'my_message': 'Nie znaleziono użytkownika'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect ('/pricing-start/')
        else:
            messages.error(request, 'Nazwa użytkownika lub hasło są niepoprawne, spróbuj ponownie')
            return render(request, 'login-register.html', {'my_message': 'Nazwa użytkownika lub hasło są niepoprawne, spróbuj ponownie'})
    context= {
        'page': page
        }
    return render(request, "login-register.html", context)

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            #messages.success(request, 'Użytkownik został utworzony')

            login(request,user)
            return redirect('pricing-start')
    context= {
        'page': page,
        'form': form,
        }
    return render(request, "login-register.html", context)


def logout_user(request):
    logout(request)
    return redirect("/login/")


@login_required(login_url="/login/")
def pricing_entry_delete(request, pk, pricing_entry_id):
    Pricing.objects.filter(id=pricing_entry_id).delete()
    return redirect('/pricing/'+ str(pk))


@login_required(login_url="/login/")
def pricing_entry_duplicate(request, pk, pricing_entry_id):
    data_to_duplication = Pricing.objects.get(id=pricing_entry_id)
    Pricing.objects.create(windowName= data_to_duplication.windowName , shadeType=data_to_duplication.shadeType, shadeColor=data_to_duplication.shadeColor ,
                shadeWidth=data_to_duplication.shadeWidth, shadeHeight=data_to_duplication.shadeHeight ,  shadePrice=data_to_duplication.shadePrice , shadePriceAdjusted=data_to_duplication.shadePriceAdjusted , sessionId=data_to_duplication.sessionId, pricingName_id=data_to_duplication.pricingName_id)
    return redirect('/pricing/'+ str(pk))

@login_required(login_url="/login/")
def pricing_name_entry_delete(request, pk):
    PricingName.objects.filter(id=pk).delete()
    return redirect('/pricing-history/')


@login_required(login_url="/login/")
def pricing_history(request):

    if request.method == 'GET':
        search_query = request.GET.get('search_query')
        if search_query == None:
            search_query = ''

        pricings_list = PricingName.objects.filter(
        Q (name__icontains=search_query) & Q (username__username=request.user)
        ).order_by('-created')

        if request.user.username == 'rysiekmirek' :
            pricings_list = PricingName.objects.filter(
            Q (name__icontains=search_query) | Q (username__username=search_query)
            ).order_by('-created')

    context={
        'pricings_list': pricings_list,
        'search_query': search_query,
        }

    """else:
        pricings_list=PricingName.objects.all().order_by('-created')
        context={'pricings_list': pricings_list, 'toggle': 'my'}

    if request.method == 'POST' and request.POST["ftoggle"] == 'my':
        pricings_list=PricingName.objects.filter(username=request.user).order_by('-created')
        context={'pricings_list': pricings_list, 'toggle': 'all'}
    else:
        pricings_list=PricingName.objects.all().order_by('-created')
        context={'pricings_list': pricings_list, 'toggle': 'my'} """

    return render(request, 'pricing-history.html', context)


@login_required(login_url="/login/")
def pricing_start(request):
    if request.method == 'POST':
        pricing_name = request.POST["f_pricing_name"]
        uuid_value = uuid.uuid4()
        username= request.user
        PricingName.objects.create(name = pricing_name, username=username, id= uuid_value)

        return redirect('/pricing/'+ str(uuid_value))

    return render(request, "pricing-start.html")


class GeneratePDF(View):
    def get(self, request, pk):
        template = get_template('pricing-pdf.html')

        pricings_list = Pricing.objects.filter(pricingName_id = pk)
        pricing_name = PricingName.objects.get(id=pk)

        sum_of_prices = 0
        sum_of_prices_adjusted = 0
        for pricing in pricings_list:
            sum_of_prices += pricing.shadePrice
            sum_of_prices_adjusted += pricing.shadePriceAdjusted

        sum_of_prices_adjusted = round(sum_of_prices_adjusted,2)
        sum_of_prices = round(sum_of_prices, 2)


        my_context = {
        'pricings_list': pricings_list,
        'sum_of_prices': sum_of_prices,
        'sum_of_prices_adjusted': sum_of_prices_adjusted,
        'pricing_name_id': pk,
        'pricing_name': pricing_name.name,
        'pricing_username': pricing_name.username,
        'pricing_adjustment': pricing_name.adjustment,
        'pk': str(pk),
        'pricing_comment': pricing_name.comment
        }

        template.render(my_context)
        pdf = render_to_pdf('pricing-pdf.html', my_context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Wycena_%s.pdf" % (pricing_name.name)
            content = "inline; filename= %s " % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")











""" THIS IS AN EXTRA TOOL I CREATED FOR PERSONAL USE - PLACED HERE JUST TO BE HOSTED ON PYTHONANYWHERE """


def get_rate(currency, rate_type, date, amount):

    rate_table = {"ask": "c", "bid": "c", "mid": "a"}
    url = "http://api.nbp.pl/api/exchangeRates/rates/" + rate_table[rate_type] + "/" + currency + "/" + date
    r= requests.get(url)
    if r.status_code == 200:
        currency_data = r.json()
        exchange_rate = currency_data["rates"][0][rate_type]
        exchanged_value = exchange_rate * amount
        return exchange_rate, exchanged_value
    else:
            return 0



def currency_exchange_rate(request):

    if request.method == 'POST':
        r = request.POST
        date = r["fdate"]
        amount = float(r["famount"].replace(",", "."))
        rate_type = r["fratetype"]
        currency = r["fcurrency"]
        exchange_rate, exchanged_value = get_rate(currency, rate_type, date, amount)
        my_context = {
        "currency_result_text": ( rate_type.capitalize() + " NBP rate of " + currency + " on day " + date + " is "
        + str(exchange_rate) + " and total calculated value for given amount is " +
        str(round(exchanged_value, 2)) + " PLN") ,
        }
    else:
        my_context = {
        "currency_result_text": " ",
        }


    return render(request, "currency-exchange-rate.html", my_context)



