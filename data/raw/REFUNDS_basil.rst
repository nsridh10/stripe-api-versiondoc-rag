=======
Refunds
=======

Refund objects allow you to refund a previously created charge that isn’t refunded yet.

-----------------
The Refund Object
-----------------

* **id** (string): Unique identifier for the object.
* **object** (string): Always has the value ``refund``.
* **refund_amount_cents** (integer): Amount, in cents.
* **charge_id** (string, nullable): ID of the charge that’s refunded.
* **transaction_id** (string, nullable): ID of the PaymentIntent that’s refunded.
* **refund_reason** (enum, nullable): Reason for the refund (``duplicate``, ``fraudulent``, ``requested_by_customer``).
* **refund_status** (string, nullable): Status of the refund (``pending``, ``succeeded``, ``failed``).

---------
Endpoints
---------

Create a refund
---------------
**POST /api/v1.0/refunds**

**Parameters:**

* **charge_id** (string, optional): The identifier of the charge to refund.
* **transaction_id** (string, optional): The identifier of the PaymentIntent to refund.
* **refund_amount_cents** (integer, optional): A positive integer representing how much of this charge to refund.
* **refund_reason** (string, optional): String indicating the reason for the refund.

Retrieve a refund
-----------------
**GET /api/v1.0/refunds/:id**

**Example Response:**

.. code-block:: json

   {
     "status": "success",
     "api_version": "1.0",
     "data": {
       "id": "re_12345",
       "object": "refund",
       "refund_amount_cents": 1000,
       "charge_id": "ch_9876",
       "transaction_id": null,
       "refund_status": "succeeded"
     }
   }

List all refunds
----------------
**GET /api/v1.0/refunds**

**Parameters:**

* **charge_id** (string, optional): Only return refunds for the charge specified by this charge ID.
* **transaction_id** (string, optional): Only return refunds for the PaymentIntent specified by this ID.
* **max_results** (integer, optional): A limit on the number of objects to be returned.