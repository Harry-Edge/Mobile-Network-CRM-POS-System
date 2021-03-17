# Mobile Network Upgrade CRM
Allows employees to upgrade a customer to a new handset or sim tariff. 

## General info
This is a mock CRM system that in theory would be used by a mobile network provider to retain and upgrade existing customers to a new plan. The system will let you build both sim-only and full handset contracts, after a tariff has been selected optional extras can also be added. Once the deal has been built, the customer needs then to confirm 3 separate validations to confirm their identity. After that, the connection can then be 'submitted'. Although nothing will change on the database, the user will just be redirected back to the dashboard. 

On the dashboard, the system will also dynamically recommend handset/sim-only products based on their current device and data usage. 

Build with Python, Django, HTML, CSS, Twilio, Javascript, Bootstrap.

## Dashboard
![](/sampleimages/Dashboard.jpeg?raw=true "Dashboard")

## Features
	- Customer can have multiple mobile numbers on one account
    - Dynamic recommendations 
	- Can add insurance/spend caps/upfront cost discount/friends and family discount
	- Ability for numbers to be early upgraded depending on the fee 
	- Detailed customer view of usage and current products
	- Colour changing information depending on mobile account data 
	- Stock control
	- Shows income/profitability for tariffs 
	- One-time pin functionality using Twilo
	- Contract information can be sent to the user's phone number 

## How to Start

Currently, the only way to create/add a customer is through the Django admin page, so after a superuser has been created, create a customer and fill out all relevant information. A mobile number will then need to be created with all the relevant information and linked to the customer. You can attach multiple phone numbers to one customer if you desire. 

Next, you will need to create the tariffs for both handsets and sim-only. Spend caps and insurance options are then the next objects that you create. Make sure each identifying code for the object is unique.

Once you have done that, you can then start creating 'Handsets'. Both the fields of 'Mrc' and upfront should be left as 0. Then make sure you select all the tariffs and insurance options available for the device. Upfront costs for the tariffs depending on the device are contained in the folder 'tariff_and_upfront_prices' in the root directory. There is already some sample handset tariffs and upfront cost there. Just made sure in the tag.py file that line 26 reflects the directory where you store it. After that, all the prices will auto-populate as long as a handset object of the same device has been created, and the tariff was made available to the device on the admin page. 

### A way to create/credit check a customer is coming in a future update along with a mock database meaning the above will no longer be needed to be performed

Once all the above has been done you should be able to start building upgrade options. If you wish to use the one-time pin and other SMS features, make sure 'account_sid' and 'auth_token' in the 'twilio_functions.py' file reflects your criteria, along with the 'from_number'.

## Handset Upgrade
![](/sampleimages/HandsetUpgrade.jpeg?raw=true "Handset Upgrade")

## Handset Tariffs
![](/sampleimages/HandsetTariffs.jpeg?raw=true "Handset Tariffs")

## Sim Upgrade
![](/sampleimages/SimUpgrade.jpeg?raw=true "Sim Upgrade")

## Add-Ons/Validation Page
![](/sampleimages/Add-OnsandValidation.jpeg?raw=true "Add-Ons/Validation")

## Login
![](/sampleimages/Login.jpeg?raw=true "Login")

## Menu 
![](/sampleimages/Menu.jpeg?raw=true "Menu")
