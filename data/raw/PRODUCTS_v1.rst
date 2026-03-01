========
Products
========

Products describe the specific goods or services you offer to your customers. 

------------------
The Product Object
------------------

* **id** (string): Unique identifier for the object.
* **object** (string): Always has the value ``product``.
* **is_active** (boolean): Whether the product is currently available for purchase.
* **created_at** (timestamp): Time at which the object was created.
* **product_name** (string): The product’s name.
* **description_text** (string, nullable): The product’s description.

---------
Endpoints
---------

Create a product
----------------
**POST /api/v1.0/products**

**Parameters:**

* **product_name** (string, required): The product’s name.
* **is_active** (boolean, optional): Whether the product is currently available. Defaults to ``true``.
* **description_text** (string, optional): The product’s description.

Retrieve a product
------------------
**GET /api/v1.0/products/:id**

**Example Response:**

.. code-block:: json

   {
     "status": "success",
     "api_version": "1.0",
     "data": {
       "id": "prod_12345",
       "object": "product",
       "is_active": true,
       "product_name": "Gold Plan",
       "description_text": "Premium access"
     }
   }

List all products
-----------------
**GET /api/v1.0/products**

**Parameters:**

* **is_active** (boolean, optional): Only return products that are active or inactive.
* **max_results** (integer, optional): A limit on the number of objects to be returned.
* **page_cursor** (string, optional): A cursor for use in pagination.