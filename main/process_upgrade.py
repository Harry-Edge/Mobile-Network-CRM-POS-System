from django.shortcuts import redirect
from .models import *
from .twillo_functions import send_otp


class GetBasketTotals:

    def __init__(self, customer_order, order_type):
        self.customer_order = customer_order
        self.order_type = order_type

    def get_total_mrc(self):

        if self.order_type == 'sim':
            tariff_mrc = self.customer_order.tariff.mrc

            if self.customer_order.friends_and_family is True:
                try:
                    insurance_mrc = self.customer_order.existing_insurance.mrc

                    new_total = (tariff_mrc * 0.7) + insurance_mrc
                    return round(new_total, 2)

                except AttributeError:
                    return round(tariff_mrc * 0.7, 2)

            else:
                try:
                    insurance_mrc = self.customer_order.existing_insurance.mrc
                    return tariff_mrc + insurance_mrc

                except AttributeError:
                    return tariff_mrc

        elif self.order_type == 'handset':

            handset_mrc = self.customer_order.handset.mrc

            try:
                handset_tariff_mrc = self.customer_order.handset_tariff.mrc

                if self.customer_order.friends_and_family is True:
                    total = (handset_mrc + handset_tariff_mrc) * 0.7

                    try:
                        insurance = self.customer_order.insurance.mrc
                        return round(total, 2) + insurance
                    except AttributeError:
                        return round(total, 2)

                try:
                    insurance = self.customer_order.insurance.mrc
                    return handset_mrc + handset_tariff_mrc + insurance
                except AttributeError:
                    return handset_mrc + handset_tariff_mrc

            except AttributeError:
                return handset_mrc

    def get_total_upfront(self):

        if self.order_type == 'sim':
            return float(0.0)

        elif self.order_type == 'handset':

            try:
                handset_upfront = self.customer_order.upfront

                if self.customer_order.handset_credit != 0:

                    handset_upfront = handset_upfront - self.customer_order.handset_credit

                    try:
                        return handset_upfront + self.customer_order.early_upgrade_fee
                    except AttributeError:
                        return handset_upfront
                try:
                    return handset_upfront + self.customer_order.early_upgrade_fee
                except AttributeError:
                    return handset_upfront

            except AttributeError:
                return float(0)


def get_account(ctn):
    mobile_number = MobileNumber.objects.get(number=ctn)
    customer = mobile_number.customer
    total_lines = customer.mobilenumber_set.all().count()

    return mobile_number, customer, total_lines


def check_if_search_is_valid(ctn):

    try:
        MobileNumber.objects.get(number=ctn)
        return True
    except Exception:
        return False


def delete_cart(request, pk, option):

    if option == "1":
        sim_order = SimOnlyOrder.objects.filter()
        sim_order.delete()
        return redirect('buildsimoupgrade', pk=pk)

    else:
        handset_order = HandsetOrder.objects.filter()
        handset_order.delete()
        return redirect('buildhandsetupgrade', pk=pk)


def get_user_pending_order(customer, order_type):

    if order_type == 'sim':
        order = SimOnlyOrder.objects.filter(cus=customer, is_ordered=False)
    elif order_type == 'handset':
        order = HandsetOrder.objects.filter(cus=customer, is_ordered=False)

    if order.exists():
        return order[0]
    return None


# Add Items to Basket
def add_to_tariff_to_basket(tariff_selected, customer, ctn):
    """SPELLING ISSUE """

    tariff_selected = tariff_selected[1:]
    tariff_object = SimOnlyTariffs.objects.get(tariff_code=tariff_selected)

    customer_order, status = SimOnlyOrder.objects.get_or_create(cus=customer, is_ordered=False)
    customer_order.tariff = tariff_object
    customer_order.contract_length = tariff_object.contract_length
    customer_order.contract_type = "EE Sim-Only Sale"
    customer_order.ctn = ctn
    customer_order.save()


def add_handset_tariff_to_basket(tariff_selected, customer_order, upfront):

    tariff_object = HandsetTariffs.objects.get(tariff_code=tariff_selected)

    customer_order.handset_tariff = tariff_object
    customer_order.upfront = upfront

    customer_order.save()


def add_handset_to_basket(handset_selected, customer, ctn):

    handset_object = Handsets.objects.get(product_code=handset_selected)

    customer_order, status = HandsetOrder.objects.get_or_create(cus=customer, is_ordered=False)
    customer_order.handset = handset_object
    customer_order.contract_length = '24'
    customer_order.contract_type = "EE Handset Sale"
    customer_order.ctn = ctn
    customer_order.save()


def add_early_upgrade_fee_to_basket(customer_order, upgrade_fee):

    try:
        customer_order.early_upgrade_fee = upgrade_fee
        customer_order.save()
    except AttributeError:
        pass


def add_spend_cap_to_basket(cap_selected, cus_order):

    cap_object = SpendCaps.objects.get(cap_code=cap_selected)

    cus_order.cap = cap_object
    cus_order.save()


def add_or_cancel_existing_insurance(option, customer_order, mobile_number):

    if option == 'cancel':
        cancel_insurance_object = Insurance.objects.get(ins_code="INSNI")
        customer_order.existing_insurance = cancel_insurance_object
        customer_order.save()

    elif option == 'keep':
        current_insurance = mobile_number.insurance_option

        customer_order.existing_insurance = current_insurance
        customer_order.save()


def add_new_insurance(customer_order, insurance_selected):

    insurance_object = Insurance.objects.get(ins_code=insurance_selected)

    customer_order.insurance = insurance_object
    customer_order.save()


def add_friends_or_family(customer_order):

    customer_order.friends_and_family = True
    customer_order.save()


def add_handset_credit(customer_order, credit_amount):

    if float(credit_amount) > customer_order.upfront:
        credit_amount = customer_order.upfront

    customer_order.handset_credit = credit_amount
    customer_order.save()


def stock_control(cus_order, input_imei):

    try:
        handset = HandsetStock.objects.get(imei=input_imei)
        if handset.handset == cus_order.handset:
            cus_order.handset_imei = input_imei
            cus_order.handset_imei_validated = True
            cus_order.save()
            return True
        else:
            cus_order.handset_imei_validated = False
            cus_order.save()
            return False

    except Exception:
        cus_order.handset_imei_validated = False
        cus_order.save()
        return False


# Customer Validation Functions
def validate_postcode(postcode_input, customer, cus_order):

    if postcode_input.upper() == customer.postcode[3:]:
        cus_order.postcode_validated = True
        cus_order.save()
    else:
        cus_order.postcode_validated = False
        cus_order.save()


def validate_mob(month_selected, customer, cus_order):

    if month_selected == str(customer.dob)[2:4]:
        cus_order.mob_validated = True
        cus_order.save()
    else:
        cus_order.mob_validated = False
        cus_order.save()


def send_one_time_pin(cus_order):

    pin = send_otp()
    cus_order.otp = pin
    cus_order.save()


def validate_one_time_pin(input_pin, cus_order):

    if str(input_pin) == str(cus_order.otp):
        cus_order.otp_validated = True
        cus_order.save()
    else:
        cus_order.otp_validated = False
        cus_order.save()


def validate_order_for_submission(cus_order, order_type):

    if order_type == 'handset':
        if cus_order.cap is not None and \
            cus_order.insurance is not None and \
            cus_order.handset_imei_validated is not None and \
            cus_order.handset_imei_validated is not False and\
            cus_order.postcode_validated is not None and \
            cus_order.postcode_validated is not False and \
            cus_order.mob_validated is not None and\
            cus_order.mob_validated is not False and\
            cus_order.otp_validated is not None and \
            cus_order.otp_validated is not False: return True
        else:
            return False

    elif order_type == 'sim':
        if cus_order.cap is not None and \
            cus_order.postcode_validated is not None and \
            cus_order.postcode_validated is not False and \
            cus_order.mob_validated is not None and\
            cus_order.mob_validated is not False and\
            cus_order.otp_validated is not None and \
            cus_order.otp_validated is not False:
            return True
        else:
            return False