# Python MBills

Python implementation of the Hal MBills APIs.

Detailed API documentation: http://docs.mbills.apiary.io
For dev access you should contact Hal MBills sales team. 


**NOTE:** This library only partially implements the APIs. If you'd like to see full support, you are free to contribute. 
Current support only provides what's absolutely necessary to process online payments.

## Installation

    $ pip install python_mbills
    
## Usage

### API Initialization

```python

public_key = "...public RSA key string..."

api = MBillsAPI(api_key='my_api_key',
                shared_secret='my_secret_key',
                mbills_rsa_pub_key=pub_key)
```


### Test API Parameters

You can test your **api_key**, **shared_secret** and **mbills_rsa_pub_key** by calling 
*test_api_parameters_and_signature_verification* function.

```python
try:
    success = api.test_api_parameters_and_signature_verification()
    print("Success: %s" % success)
except SignatureValidationException:
    print("Failed to verify signature")
```

### Test Webhook

To trigger webhook call, you can issue a *test_webhook* call. The API will also
verify the RSA keys and your access credentials.

```python
try:
    success = api.test_webhook()
    print("Success: %s" % success)
except SignatureValidationException:
    print("Failed to verify signature")
```

### Create new Sale

You can create a new sale request by simply calling *create_new_sale* with appropriate parameters.

Response:
 - Transaction ID
 - Payment Token Number
 - Status of the payment (please refer to the official documentation)

```python
try:
    tx_id, payment_token_number, status = api.create_new_sale(amount=100,
                                                              purpose='Purpose of the payment',
                                                              payment_reference=None,
                                                              order_id=None,
                                                              channel_id=None,
                                                              capture=True)
    print("Payment token number: %s" % payment_token_number)
except SignatureValidationException:
    print("Failed to verify signature")
```

### Fetch Transaction Status

You can issue a call to check the transaction status. 

```python
try:
    response_dict = api.create_new_sale(transaction_id=tx_id)
except SignatureValidationException:
    print("Failed to verify signature")
```

## Not yet supported APIs

List of currently not supported APIs:
 - Capture Sale
 - Void Preauth
 - Attach Document - ZOI
 - Last 24 
 - Get Your Wallet Balance
 - FURS Bill Status


