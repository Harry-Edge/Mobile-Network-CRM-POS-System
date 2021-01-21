from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    employee_username = models.CharField(max_length=7, null=True)
    employee_number = models.CharField(max_length=7, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Customer(models.Model):
    ADD_LINE_OPTIONS = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]


    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    dob = models.IntegerField(null=True)
    email = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    first_line_address = models.CharField(max_length=200, null=True)
    credit_class = models.IntegerField(null=True)
    date_tenure = models.CharField(max_length=200, null=True)
    add_lines_available = models.CharField(max_length=200, null=True, choices=ADD_LINE_OPTIONS)

    def __str__(self):

        return f"{self.last_name} {self.first_name}"

class Insurance(models.Model):

    INSURANCE_NAME = [('Full Cover £14 ', 'Full Cover £14'), ('Damage Cover £12.32', 'Damage Cover £12.32'),
                      ('Full Cover £12.32', 'Full Cover £12.32'), ('Damage Cover 7.84', 'Damage Cover 7.84'),
                      ('No Insurance', 'No Insurance')]

    EXCESS_FEES = [('120', '120'), ('100', '100')]

    insurance_name = models.CharField(max_length=200, null=True, choices=INSURANCE_NAME)
    upfront = models.IntegerField(null=True)
    mrc = models.FloatField(null=True)
    excess_fee = models.CharField(max_length=200, null=True, choices=EXCESS_FEES)
    ins_code = models.CharField(max_length=100, null=True)

    def __str__(self):

        return self.insurance_name


    class Meta:
        verbose_name_plural = "Insurance"

class MobileNumber(models.Model):

    SPEND_CAPS = [('None', 'None'), ('0', '0'), ('5', '5'), ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'),
                  ('50', '50'), ('60', '60'), ('70', '70'), ('80', '80'), ('90', '90'), ('100', '100')]

    CONTRACT_LENGTH = [('1', '1'), ('12', '12'), ('18', '18'), ('24', '24')]

    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)

    user = models.CharField(max_length=11, null=True)

    """PRODUCTS"""
    number = models.CharField(max_length=11, null=True)
    plan = models.CharField(max_length=100, null=True)
    mrc = models.FloatField(null=True)
    device = models.CharField(max_length=100, null=True)
    insurance = models.BooleanField(default=False)
    insurance_option = models.ForeignKey(Insurance, on_delete=models.SET_NULL, null=True)
    average_bill = models.FloatField(max_length=6)
    data_allowance = models.FloatField(max_length=6, null=True)

    """USAGE"""
    spend_cap = models.CharField(max_length=100, null=True, choices=SPEND_CAPS)
    data_usage_3m = models.FloatField(max_length=10)
    data_gifted_3m = models.FloatField(max_length=10)
    texts_sent_3m = models.IntegerField(null=True)
    call_mins = models.IntegerField(null=True)
    mms_sent = models.IntegerField(null=True)

    """Eligibility"""
    contract_start = models.DateField()
    contract_end = models.DateField(null=True)
    contract_length_months = models.CharField(max_length=10, null=True, choices=CONTRACT_LENGTH)
    early_upgrade_fee = models.FloatField(null=True)

    """DISCOUNT/S"""
    friends_and_family = models.BooleanField(null=True)
    perk = models.BooleanField(null=True)

    def __str__(self):

        return f"{self.number} {self.customer}"

class HandsetTariffs(models.Model):

    CONTRACT_LENGTH = [('24', '24')]
    DATA_ALLOWANCE = [('0.25', '0.25'), ('1', '1'), ('4', '4'), ('10', '10'), ('40', '40'),
                      ('100', '100'), ('1000', '1000')]

    PLAN_TYPE = [('Essential', 'Essential')]

    contract_length = models.CharField(max_length=10, null=True, choices=CONTRACT_LENGTH)
    plan_name = models.CharField(max_length=100, null=True)
    mrc = models.FloatField(null=True)
    upfront = models.FloatField(null=True)
    data_allowance = models.CharField(max_length=10, null=True, choices=DATA_ALLOWANCE)
    plan_type = models.CharField(max_length=10, null=True, choices=PLAN_TYPE)
    tariff_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.plan_name} £{self.mrc} -- {self.tariff_code}"

    class Meta:
        verbose_name_plural = "Handset Tariffs"
        ordering = ['tariff_code']


class Handsets(models.Model):

    MANUFACTURES = [('Pear', 'Pear'), ('Soulsung', 'Soulsung')]

    SPEED_TYPES = [('5G', '5G'), ('4G', '4G')]

    manufacture = models.CharField(max_length=30, null=True, choices=MANUFACTURES)
    model = models.CharField(max_length=100, null=True)
    storage = models.IntegerField(null=True)
    speed_type = models.CharField(max_length=30, null=True, choices=SPEED_TYPES)
    colour = models.CharField(max_length=100, null=True)
    cost_price = models.FloatField(max_length=10)
    mrc = models.FloatField(null=True)
    upfront = models.FloatField(null=True)
    product_code = models.IntegerField(null=True)

    tariffs_availible = models.ManyToManyField(HandsetTariffs)
    insurance_available = models.ManyToManyField(Insurance)

    class Meta:
        verbose_name_plural = "Handsets"
        ordering = ['manufacture', 'model']


    def __str__(self):

        return f"{self.manufacture} {self.model} {self.storage} {self.colour}"


class SimOnlyTariffs(models.Model):

    CONTRACT_LENGTH = [('1', '1'), ('12', '12'), ('18', '18'), ('24', '24')]

    DATA_ALLOWANCE = [('0.25', '0.25'), ('1', '1'), ('3', '3'), ('20', '20'), ('60', '60'), ('100', '100'),
                      ('200', '200'), ('1000', '1000')]

    PLAN_TYPE = [('Standard', 'Standard')]

    contract_length = models.CharField(max_length=10, null=True, choices=CONTRACT_LENGTH)
    plan_name = models.CharField(max_length=100, null=True)
    mrc = models.FloatField(null=True)
    upfront = models.FloatField(null=True)
    data_allowance = models.CharField(max_length=10, null=True, choices=DATA_ALLOWANCE)
    plan_type = models.CharField(max_length=10, null=True, choices=PLAN_TYPE)
    tariff_code = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "Sim Only Tariffs"


    def __str__(self):

        return f"{self.plan_name} {self.data_allowance}GB {self.contract_length} £{self.mrc}pm"

class SpendCaps(models.Model):

    CAP_AMOUNTS = [('None', 'None'), ('0', '0'), ('5', '5'), ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'),
                  ('50', '50'), ('60', '60'), ('70', '70'), ('80', '80'), ('90', '90'), ('100', '100')]

    cap_amount = models.CharField(max_length=100, null=True, choices=CAP_AMOUNTS)
    cap_name = models.CharField(max_length=200, null=True)
    mrc = models.IntegerField(null=True)
    upfront = models.IntegerField(null=True)
    cap_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.cap_name

    class Meta:
        verbose_name_plural = "Spend Caps"

class SimOnlyOrder(models.Model):
    CONTRACT_LENGTH = [('1', '1'), ('12', '12'), ('18', '18'), ('24', '24')]

    transaction_id = models.CharField(max_length=10, null=True)
    cus = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    ctn = models.CharField(null=True, max_length=11)
    is_ordered = models.BooleanField(default=False)

    contract_length = models.CharField(null=True, choices=CONTRACT_LENGTH, max_length=2)
    contract_type = models.CharField(null=True, max_length=30)
    tariff = models.OneToOneField(SimOnlyTariffs, on_delete=models.SET_NULL, null=True)
    cap = models.OneToOneField(SpendCaps, on_delete=models.SET_NULL, null=True)
    existing_insurance = models.OneToOneField(Insurance, on_delete=models.SET_NULL, null=True)
    friends_and_family = models.BooleanField(default=False, null=True)

    # Customer Validations on Order
    postcode_validated = models.BooleanField(null=True)
    mob_validated = models.BooleanField(null=True)
    otp = models.IntegerField(null=True)
    otp_validated = models.BooleanField(null=True)

    date_ordered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cus} {self.tariff}"

class HandsetOrder(models.Model):

    transaction_id = models.CharField(max_length=10, null=True)
    cus = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    ctn = models.CharField(null=True, max_length=11)
    is_ordered = models.BooleanField(default=False)

    contract_length = models.CharField(null=True, max_length=2)
    contract_type = models.CharField(null=True, default="EE Handset Sale", max_length=30)
    early_upgrade_fee = models.FloatField(default=0, null=True)
    handset = models.OneToOneField(Handsets, on_delete=models.SET_NULL, null=True)
    handset_tariff = models.OneToOneField(HandsetTariffs, on_delete=models.SET_NULL, null=True)
    cap = models.OneToOneField(SpendCaps, on_delete=models.SET_NULL, null=True)
    insurance = models.OneToOneField(Insurance, on_delete=models.SET_NULL, null=True)
    upfront = models.FloatField(default=float(0), null=True)
    handset_imei = models.CharField(null=True, max_length=15)
    friends_and_family = models.BooleanField(default=False, null=True)
    handset_credit = models.IntegerField(default=0, null=True)
    one_hundred_day_promo = models.BooleanField(default=False, null=True)

    # Customer Validations on Order
    handset_imei_validated = models.BooleanField(null=True)
    postcode_validated = models.BooleanField(null=True)
    mob_validated = models.BooleanField(null=True)
    otp = models.IntegerField(null=True)
    otp_validated = models.BooleanField(null=True)

    date_ordered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cus)

class HandsetStock(models.Model):

    handset = models.ForeignKey(Handsets, on_delete=models.SET_NULL, null=True)
    imei = models.CharField(max_length=15, null=True)

    def __str__(self):

        return f"{self.handset} {self.imei}"

    class Meta:
        verbose_name_plural = "Handset Stock"




