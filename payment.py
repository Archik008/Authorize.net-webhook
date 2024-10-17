from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController

from config import *

from string import digits
from random import choice

def generate_id():
    return "".join(choice(digits) for _ in range(5))

def charge_credit_card(vin_code, card_number, exp_date, card_code, first_name, last_name, address, city, state, zip_code, email):
    """
    Charge a credit card with provided details
    """

    # Authentication with API credentials
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = api_login_id
    merchantAuth.transactionKey = transaction_key

    # Payment data (credit card details)
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = card_number
    creditCard.expirationDate = exp_date
    creditCard.cardCode = card_code

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    # Order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = generate_id()
    order.description = f"Carfax report {vin_code}"

    # Billing address
    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = first_name
    customerAddress.lastName = last_name
    customerAddress.address = address
    customerAddress.city = city
    customerAddress.state = state
    customerAddress.zip = zip_code
    customerAddress.country = "USA"  # Страну можно поменять

    # Customer data
    customerData = apicontractsv1.customerDataType()
    customerData.type = "individual"
    customerData.email = email

    # Create transaction request
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"  # Автоматическое списание средств
    transactionrequest.amount = amount
    transactionrequest.payment = payment
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData

    # Send the request to Authorize.Net
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.transactionRequest = transactionrequest

    # Create the controller
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    # Handle response
    if response is not None:
        if response.messages.resultCode == "Ok":
            if hasattr(response.transactionResponse, 'messages'):
                print(f"Transaction ID: {response.transactionResponse.transId}", flush=True)
                return True
            else:
                print("Transaction Failed.", flush=True)
                if hasattr(response.transactionResponse, 'errors'):
                    print(f"Error: {response.transactionResponse.errors.error[0].errorText}", flush=True)
        else:
            print("Transaction Failed.", flush=True)
            if hasattr(response.transactionResponse, 'errors'):
                print(f"Error Code: {response.transactionResponse.errors.error[0].errorCode}", flush=True)
                print(f"Error message: {response.transactionResponse.errors.error[0].errorText}", flush=True)
    else:
        print("Null Response.", flush=True)