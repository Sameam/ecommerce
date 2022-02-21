from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='hhtcdg9ftbjhf6mv',
    public_key='j5rrpn8sgn8gsrjp',
    private_key='8937792c361e5cba409c450e78749b0e'
  )
)

def validate_user_session(id,token):
  UserModel = get_user_model()
  
  try:
    user = UserModel.objects.get(pk=id)
    if user.session_token == token:
      return True
    return False
  except UserModel.DoesNotExist:
    return False
  
@csrf_exempt
def generate_token(request,id,token):
  if not validate_user_session(id,token):
    return JsonResponse({error:"Invalid Session"})
  
  return JsonResponse({"ClientToken": gateway.client_token.generate(), "Success": True})

@csrf_exempt 
def process_payment(request,id, token):
  if not validate_user_session(id,token):
    return JsonResponse({error:"Invalid Session"})
  
  nonce_from_the_client = request.POST['paymentMethodNonce']
  amount_from_client = request.POST['amount']
  
  result = result = gateway.transaction.sale({
    "amount": amount_from_client,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
  })
  
  if result.is_success:
    return JsonResponse({"success":result.is_success,
                         "transaction":{"id":result.transaction.id, 
                                        "amount":result.transaction.amount
    }})
  else:
    return JsonResponse({"success":False})