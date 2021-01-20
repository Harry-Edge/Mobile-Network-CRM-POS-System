from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from . import process_upgrade
from . import date_calculations
from . import twillo_functions


@login_required(login_url='login')
def dashboard(request, pk):

    # Search Bar Function at top of Webpage
    new_search_customer_number = request.POST.get('number')
    if new_search_customer_number is not None:
        if process_upgrade.check_if_search_is_valid(new_search_customer_number) is True:
            return redirect('/upgrade/dashboard/' + new_search_customer_number)
        else:
            messages.error(request, 'Invalid CTN!')

    # Deletes Order when redirecting to the home page is there is one
    SimOnlyOrder.objects.filter().delete()
    HandsetOrder.objects.filter().delete()

    # Gets the customers/employees data
    employee = request.user
    mobile_number, customer, total_lines = process_upgrade.get_account(pk)
    date_cal = date_calculations.DateTimeCalculations(mobile_number)

    context = {'customer': customer, 'mobile_number': mobile_number, "employee": employee, "total_lines": total_lines,
               'date_cal': date_cal}

    return render(request, 'main/dashboard.html', context)


@login_required(login_url='login')
def build_sim_only_upgrade(request, pk):

    # Search Bar Function at top of Webpage
    new_search_customer_number = request.POST.get('number')
    if new_search_customer_number is not None:
        if process_upgrade.check_if_search_is_valid(new_search_customer_number) is True:
            return redirect('/upgrade/dashboard/' + new_search_customer_number)
        else:
            messages.error(request, 'Invalid CTN!')

    # Gets the customers/employees data
    employee = request.user
    mobile_number, customer, total_lines = process_upgrade.get_account(pk)
    date_cal = date_calculations.DateTimeCalculations(mobile_number)

    sim_only_tariffs = SimOnlyTariffs.objects.order_by('-mrc')

    # Sim-Only Button Filter
    if '1' in request.POST:
        sim_only_tariffs = sim_only_tariffs.filter(contract_length='1')
    elif '12' in request.POST:
        sim_only_tariffs = sim_only_tariffs.filter(contract_length='12')
    elif '18' in request.POST:
        sim_only_tariffs = sim_only_tariffs.filter(contract_length='18')
    elif '24' in request.POST:
        sim_only_tariffs = sim_only_tariffs.filter(contract_length='24')
    elif 'smart' in request.POST:
        sim_only_tariffs = sim_only_tariffs.filter(plan_type='Smart')

    # Check if a tariff has been selected and processes
    tariff_selected = request.POST.get('mrc')
    if tariff_selected is not None and process_upgrade.get_user_pending_order(customer, 'sim') is None:
        process_upgrade.add_to_tariff_to_basket(tariff_selected, customer, pk)

    # Gets a current existing order and basket if there is one and current basket totals
    existing_order = process_upgrade.get_user_pending_order(customer, 'sim')
    basket = process_upgrade.GetBasketTotals(existing_order, 'sim')

    context = {'customer': customer, 'mobile_number': mobile_number, "employee": employee, "total_lines": total_lines,
               'sim_only_tariffs': sim_only_tariffs, "order": existing_order, 'basket_total': basket,
               'date_cal': date_cal}

    return render(request, 'main/build-sim-upgrade.html', context)


@login_required(login_url='login')
def finalise_sim_only_upgrade(request, pk):

    # Search Bar Function at top of Webpage
    new_search_customer_number = request.POST.get('number')
    if new_search_customer_number is not None:
        if process_upgrade.check_if_search_is_valid(new_search_customer_number) is True:
            return redirect('/upgrade/dashboard/' + new_search_customer_number)
        else:
            messages.error(request, 'Invalid CTN!')

    # Gets the customers/employees data
    employee = request.user
    mobile_number, customer, total_lines = process_upgrade.get_account(pk)
    date_cal = date_calculations.DateTimeCalculations(mobile_number)

    spend_caps = SpendCaps.objects.all()

    # Gets customer order before any changes are made
    cus_order = SimOnlyOrder.objects.get(cus=customer)

    # Checks if a spend cap has been selected
    try:
        cap_selected = request.POST.get('cap_selected')
        if cap_selected is not None:
            process_upgrade.add_spend_cap_to_basket(cap_selected, cus_order)
    except Exception:
        messages.info(request, 'Invalid option, Please choose a valid amount')

    # Checks if an insurance option has been selected
    if 'cancel-insurance' in request.POST:
        process_upgrade.add_or_cancel_existing_insurance('cancel', cus_order, mobile_number)
    elif 'keep-insurance' in request.POST:
        process_upgrade.add_or_cancel_existing_insurance('keep', cus_order, mobile_number)

    # Checks if friends and family discount has been selected
    if 'add_f_and_f' in request.POST:
        process_upgrade.add_friends_or_family(cus_order)

    # Customer Postcode/Birthday validations
    postcode_input = request.POST.get('postcode')
    if postcode_input is not None:
        process_upgrade.validate_postcode(postcode_input, customer, cus_order)
    month_selected = request.POST.get('month')
    if month_selected is not None:
        process_upgrade.validate_mob(month_selected, customer, cus_order)

    # One time pin validations
    send_pin = request.POST.get('sendpin')
    if send_pin is not None:
        process_upgrade.send_one_time_pin(cus_order)
    input_pin = request.POST.get('inputpin')
    if input_pin is not None:
        process_upgrade.validate_one_time_pin(input_pin, cus_order)

    # Sends contract information to the phone number
    if "send_contract" in request.POST:
        twillo_functions.send_sim_only_order_information(cus_order)

    # Checks if all mandatory items has been added to bast and 'submits' the connection
    if 'submit_connection' in request.POST:
        if process_upgrade.validate_order_for_submission(cus_order, 'sim') is True:
            return redirect('/upgrade/dashboard/' + pk)
        else:
            messages.error(request, 'Order criteria for submission has not been met!!')

    # Get current existing order and current basket totals
    existing_order = process_upgrade.get_user_pending_order(customer, 'sim')
    basket = process_upgrade.GetBasketTotals(existing_order, 'sim')

    context = {'customer': customer, 'mobile_number': mobile_number, "employee": employee, "total_lines": total_lines,
               "order": existing_order, 'spend_caps': spend_caps, 'basket_total': basket, 'date_cal': date_cal}

    return render(request, 'main/finalise-sim-upgrade.html', context)


@login_required(login_url='login')
def build_handset_upgrade(request, pk):

    # Search Bar Function at top of Webpage
    new_search_customer_number = request.POST.get('number')
    if new_search_customer_number is not None:
        if process_upgrade.check_if_search_is_valid(new_search_customer_number) is True:
            return redirect('/upgrade/dashboard/' + new_search_customer_number)
        else:
            messages.error(request, 'Invalid CTN!')

    # Gets the customers/employees data
    employee = request.user
    handsets = Handsets.objects.order_by('manufacture')
    mobile_number, customer, total_lines = process_upgrade.get_account(pk)
    date_cal = date_calculations.DateTimeCalculations(mobile_number)

    # Checks if search box has been used
    handset_search = request.POST.get('handset_search')
    if handset_search is not None:
        handsets = handsets.filter(model__icontains=handset_search)

    # Handset Filter Buttons
    if 'pear' in request.POST:
        handsets = handsets.filter(manufacture='Pear')
    elif 'soulsung' in request.POST:
        handsets = handsets.filter(manufacture='Soulsung')

    # Check if a handset has been selected
    handset_selected = request.POST.get('handset_choice')
    if handset_selected is not None and process_upgrade.get_user_pending_order(customer, 'handset') is None:
        process_upgrade.add_handset_to_basket(handset_selected, customer, pk)

    # Gets existing order
    existing_order = process_upgrade.get_user_pending_order(customer, 'handset')

    # Adds early upgrade fee to the basket if applicable
    if date_cal.calculate_early_upgrade_fee() != 0:
        process_upgrade.add_early_upgrade_fee_to_basket(existing_order, date_cal.calculate_early_upgrade_fee())

    # Filters repeating models due to colour variations
    check_repeating_models_list = []
    new_handset_list = []
    for handset in handsets:
        if handset.model not in check_repeating_models_list:
            check_repeating_models_list.append(handset.model)
            new_handset_list.append(handset)

    basket = process_upgrade.GetBasketTotals(existing_order, 'handset')

    context = {'customer': customer, 'mobile_number': mobile_number, "employee": employee, "total_lines": total_lines,
               'date_cal': date_cal, 'handsets': new_handset_list,  "order": existing_order,
               'basket_total': basket}

    return render(request, 'main/build-handset-upgrade.html', context)


def choose_handset_tariff(request, pk):

    # Search Bar Function at top of Webpage
    new_search_customer_number = request.POST.get('number')
    if new_search_customer_number is not None:
        if process_upgrade.check_if_search_is_valid(new_search_customer_number) is True:
            return redirect('/upgrade/dashboard/' + new_search_customer_number)
        else:
            messages.error(request, 'Invalid CTN!')

    # Gets the customers/employees data
    employee = request.user
    mobile_number, customer, total_lines = process_upgrade.get_account(pk)
    date_cal = date_calculations.DateTimeCalculations(mobile_number)
    cus_order = process_upgrade.get_user_pending_order(customer, 'handset')

    # Check if a tariff has been selected
    tariff_selected = request.POST.get('tariff_code')
    if tariff_selected is not None:
        upfront = request.POST.get('tariff_upfront')
        process_upgrade.add_handset_tariff_to_basket(tariff_selected, cus_order, upfront)

    chosen_handset_tariffs_available = cus_order.handset.tariffs_availible.order_by('-mrc')

    # Changes the order of tariffs by mrc
    if 'sort_by_mrc' in request.POST:
        chosen_handset_tariffs_available = cus_order.handset.tariffs_availible.order_by('mrc')

    # Checks if any discount has been selected and applies, also check is an invalid option has been seleceted
    try:
        handset_credit_amount = request.POST.get('handset_credit')
        if handset_credit_amount is not None:
            process_upgrade.add_handset_credit(cus_order, handset_credit_amount)
    except ValueError:
        messages.error(request, 'Invalid option, Please choose a valid amount')

    if 'add_f_and_f' in request.POST:
        process_upgrade.add_friends_or_family(cus_order)
    if '100_day_early' in request.POST:
        cus_order.early_upgrade_fee = 0
        cus_order.one_hundred_day_promo = True
        cus_order.save()

    # Get current existing order and current basket totals
    existing_order = process_upgrade.get_user_pending_order(customer, 'handset')
    basket = process_upgrade.GetBasketTotals(existing_order, 'handset')

    context = {'customer': customer, 'mobile_number': mobile_number, "employee": employee, "total_lines": total_lines,
               'date_cal': date_cal, "handset_tariffs": chosen_handset_tariffs_available,
               "order": existing_order, 'basket_total': basket}

    return render(request, 'main/choose-handset-tariff.html', context)


def finalise_handset_upgrade(request, pk):

    # Search Bar Function at top of Webpage
    new_search_customer_number = request.POST.get('number')
    if new_search_customer_number is not None:
        if process_upgrade.check_if_search_is_valid(new_search_customer_number) is True:
            return redirect('/upgrade/dashboard/' + new_search_customer_number)
        else:
            messages.error(request, 'Invalid CTN!')

    # Gets the customers/employees data
    employee = request.user
    mobile_number, customer, total_lines = process_upgrade.get_account(pk)
    date_cal = date_calculations.DateTimeCalculations(mobile_number)
    cus_order = process_upgrade.get_user_pending_order(customer, 'handset')

    # Get the spend caps and insurance options
    spend_caps = SpendCaps.objects.all()
    insurance_available = cus_order.handset.insurance_available.all()

    # Checks if spend caps/insurance has been selected and checks if it's valid
    try:
        cap_selected = request.POST.get('cap_selected')
        if cap_selected is not None:
            process_upgrade.add_spend_cap_to_basket(cap_selected, cus_order)
    except Exception:
        messages.error(request, 'Invalid option, Please choose a valid amount')

    ins_selected = request.POST.get('add_insurance')
    if ins_selected is not None:
        process_upgrade.add_new_insurance(cus_order, ins_selected)

    # Customer Postcode/Birthday validations
    postcode_input = request.POST.get('postcode')
    if postcode_input is not None:
        process_upgrade.validate_postcode(postcode_input, customer, cus_order)
    month_selected = request.POST.get('month')
    if month_selected is not None:
        process_upgrade.validate_mob(month_selected, customer, cus_order)

    # One time pin validations
    send_pin = request.POST.get('sendpin')
    if send_pin is not None:
        process_upgrade.send_one_time_pin(cus_order)
    input_pin = request.POST.get('inputpin')
    if input_pin is not None:
        process_upgrade.validate_one_time_pin(input_pin, cus_order)

    # Checks if stock has been inputted and adds it to the order
    input_imei = request.POST.get('input_imei')
    if input_imei is not None:
        if process_upgrade.stock_control(cus_order, input_imei) is False:
            messages.error(request, 'Invalid IMEI')

    # Sends contract information to the phone number
    if "send_contract" in request.POST:
        twillo_functions.send_handset_order_information(cus_order)

    # Checks if all mandatory items has been added to bast and 'submits' the connection
    if 'submit_connection' in request.POST:
        if process_upgrade.validate_order_for_submission(cus_order, 'handset') is True:
            return redirect('/upgrade/dashboard/' + pk)
        else:
            messages.error(request, 'Order criteria for submission has not been met!!')

    # Get current existing order and current basket totals
    existing_order = process_upgrade.get_user_pending_order(customer, 'handset')
    basket = process_upgrade.GetBasketTotals(existing_order, 'handset')

    context = {'customer': customer, 'mobile_number': mobile_number, "employee": employee, "total_lines": total_lines,
               "order": existing_order, 'spend_caps': spend_caps, 'insurance': insurance_available,
               'basket_total': basket, 'date_cal': date_cal}

    return render(request, 'main/finalise-handset-upgrade.html', context)
