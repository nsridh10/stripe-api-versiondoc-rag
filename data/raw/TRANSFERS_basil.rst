=========
Transfers
=========

A Transfer object is created when you move funds between accounts.

-------------------
The Transfer Object
-------------------

* **id** (string): Unique identifier for the object.
* **object** (string): Always has the value ``transfer``.
* **amount_in_cents** (integer): Amount in cents to be transferred.
* **currency_code** (enum): Three-letter ISO currency code, in lowercase.
* **recipient_id** (string): ID of the account the transfer was sent to.
* **is_reversed** (boolean): Whether the transfer has been fully reversed.

---------
Endpoints
---------

Create a transfer
-----------------
**POST /api/v1.0/transfers**

**Parameters:**

* **amount_in_cents** (integer, required): A positive integer in cents representing how much to transfer.
* **currency_code** (enum, required): Three-letter ISO code for currency.
* **recipient_id** (string, required): The ID of the connected account.

Retrieve a transfer
-------------------
**GET /api/v1.0/transfers/:id**

**Example Response:**

.. code-block:: json

   {
     "status": "success",
     "api_version": "1.0",
     "data": {
       "id": "tr_12345",
       "object": "transfer",
       "amount_in_cents": 400,
       "currency_code": "usd",
       "recipient_id": "acct_9876",
       "is_reversed": false
     }
   }

List all transfers
------------------
**GET /api/v1.0/transfers**

**Parameters:**

* **recipient_id** (string, optional): Only return transfers for the destination specified by this account ID.
* **max_results** (integer, optional): A limit on the number of objects to be returned. Default is 10.