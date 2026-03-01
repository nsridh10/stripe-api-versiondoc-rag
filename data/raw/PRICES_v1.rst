======
Prices
======

Prices define the unit cost, currency, and (optional) billing cycle for products.

----------------
The Price Object
----------------

* **id** (string): Unique identifier for the object.
* **object** (string): Always has the value ``price``.
* **is_active** (boolean): Whether the price can be used for new purchases.
* **currency_code** (enum): Three-letter ISO currency code.
* **product_reference_id** (string): The ID of the product this price is associated with.
* **billing_cycle** (object, nullable): The recurring components of a price.
* **price_in_cents** (integer, nullable): The unit amount in cents to be charged.

---------
Endpoints
---------

Create a price
--------------
**POST /api/v1.0/prices**

**Parameters:**

* **currency_code** (enum, required): Three-letter ISO currency code.
* **price_in_cents** (integer, required): A positive integer in cents.
* **product_reference_id** (string, required): The ID of the Product that this Price will belong to.
* **billing_cycle** (object, optional): The recurring components of a price.

Retrieve a price
----------------
**GET /api/v1.0/prices/:id**

**Example Response:**

.. code-block:: json

   {
     "status": "success",
     "api_version": "1.0",
     "data": {
       "id": "price_12345",
       "object": "price",
       "is_active": true,
       "currency_code": "usd",
       "price_in_cents": 1000,
       "product_reference_id": "prod_12345",
       "billing_cycle": null
     }
   }

List all prices
---------------
**GET /api/v1.0/prices**

**Parameters:**

* **is_active** (boolean, optional): Only return prices that are active or inactive.
* **product_reference_id** (string, optional): Only return prices for the given product.
* **max_results** (integer, optional): A limit on the number of objects to be returned.