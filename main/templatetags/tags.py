from django import template
from main import models
from main import date_calculations
import csv

register = template.Library()


@register.simple_tag
def filter_colours(model):

    filter = models.Handsets.objects.filter(model=model)

    return filter


@register.simple_tag
def get_upfront(mrc, model, data_allowance):

    """ This tag get all the upfront costs for the relevant tariffs for a specific handset """

    mrc_correct_format = (str(mrc)[:-2])

    def get_handset_upfront(handset, mrc, data_csv):

        location = f'/Users/harry/Desktop/Git Projects/Mobile Network Upgrade CRM/tariff_and_upfront_prices/{data_csv}.csv'

        reader = csv.DictReader(open(location))

        for tariffs in reader:
            if tariffs['Handset'] == handset.upper():
                return tariffs[mrc]

    if data_allowance == '1000':
        return get_handset_upfront(model, mrc_correct_format, 'ultd_tariffs')

    elif data_allowance == '100':
        return get_handset_upfront(model, mrc_correct_format, '100gb_tariffs')

    elif data_allowance == '10':
        return get_handset_upfront(model, mrc_correct_format, '10gb_tariffs')

    elif data_allowance == '4':
        return get_handset_upfront(model, mrc_correct_format, '4gb_tariffs')


@register.simple_tag
def get_total_stock(handset):

    list = []

    for hand in models.HandsetStock.objects.all():

        try:
            if hand.handset.model == handset.model:
                list.append(hand.handset.model)
        except Exception:
            pass

    return len(list)


@register.simple_tag
def get_individual_colour_stock(handset):

    list = []

    for hand in models.HandsetStock.objects.all():
        try:
            if hand.handset.product_code == handset.product_code:
                list.append(hand)
        except Exception:
            pass

    return len(list)


@register.simple_tag
def calculate_value(mrc, contract_length, model):

    if model != 0:
        mrc = mrc*24

        return mrc - model.cost_price

    else:
        if contract_length == '1':
            return mrc * float(3)
        else:
            return mrc * float(contract_length)


@register.simple_tag
def calculate_f_and_f_discount_amount(mrc):
    try:
        return round(mrc * 0.3, 2)
    except TypeError:
        pass


@register.simple_tag
def calculate_if_number_is_eligible(ctn):
    calculate = date_calculations.DateTimeCalculations(ctn)

    return calculate.calculate_if_eligible()


@register.simple_tag
def return_tariff_object(tariffs, index):
    try:
        return tariffs[index]
    except Exception:
        return None