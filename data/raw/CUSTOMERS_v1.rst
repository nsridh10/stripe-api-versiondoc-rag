Customers
=========

A Customer object represents a customer of your business. Use it to save payment and contact information and track payments.

Endpoints
---------

.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - POST
     - ``/v1/customers``
     - Create a customer
   * - POST
     - ``/v1/customers/:id``
     - Update a customer
   * - GET
     - ``/v1/customers/:id``
     - Retrieve a customer
   * - GET
     - ``/v1/customers``
     - List all customers


The Customer Object
-------------------

Key Fields
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Field
     - Type
     - Description
   * - ``id``
     - string
     - Unique identifier (e.g. ``cus_NffrFeUfNV2Hib``)
   * - ``object``
     - string
     - Always ``"customer"``
   * - ``full_name``
     - string
     - Customer's full name or business name
   * - ``email``
     - string
     - Customer's email address
   * - ``phone``
     - string
     - Customer's phone number
   * - ``description``
     - string
     - Arbitrary string for display/notes
   * - ``metadata``
     - object
     - Key-value pairs for storing extra info
   * - ``address``
     - object
     - Address: city, country, line1, line2, postal_code, state
   * - ``balance``
     - integer
     - Current balance in cents. Negative = credit, positive = amount owed
   * - ``currency``
     - string
     - Three-letter ISO currency code for recurring billing
   * - ``delinquent``
     - boolean
     - True if customer has a past-due invoice
   * - ``created``
     - timestamp
     - Unix timestamp of creation
   * - ``livemode``
     - boolean
     - True if live mode, false if test mode
   * - ``default_source``
     - string
     - ID of default payment source attached to this customer
   * - ``invoice_settings.default_source``
     - string
     - ID of default source for subscriptions/invoices

Example Object
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "cus_NffrFeUfNV2Hib",
     "object": "customer",
     "full_name": "Jenny Rosen",
     "email": "jennyrosen@example.com",
     "phone": null,
     "description": null,
     "metadata": {},
     "address": null,
     "balance": 0,
     "currency": null,
     "delinquent": false,
     "created": 1680893993,
     "livemode": false,
     "default_source": null,
     "invoice_settings": {
       "default_source": null,
       "custom_fields": null,
       "footer": null
     }
   }


Create a Customer
-----------------

**POST** ``/v1/customers``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 15 30

   * - Parameter
     - Type
     - Required
     - Description
   * - ``full_name``
     - string
     - optional
     - Full name or business name (max 256 chars)
   * - ``email``
     - string
     - optional
     - Email address (max 512 chars)
   * - ``phone``
     - string
     - optional
     - Phone number (max 20 chars)
   * - ``description``
     - string
     - optional
     - Arbitrary string for display/notes
   * - ``metadata``
     - object
     - optional
     - Key-value pairs for storing extra info
   * - ``address``
     - object
     - optional
     - Address fields: city, country, line1, line2, postal_code, state
   * - ``balance``
     - integer
     - optional
     - Starting balance in cents
   * - ``source``
     - string
     - optional
     - Token or source ID to attach as the customer's default payment source
   * - ``invoice_settings.default_source``
     - string
     - optional
     - Default source ID for invoices/subscriptions

Returns
~~~~~~~

Returns the Customer object after successful creation. Raises an error if parameters are invalid.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/customers \
     -u "<<YOUR_SECRET_KEY>>" \
     -d full_name="Jenny Rosen" \
     --data-urlencode email="jennyrosen@example.com"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "cus_NffrFeUfNV2Hib",
     "object": "customer",
     "full_name": "Jenny Rosen",
     "email": "jennyrosen@example.com",
     "balance": 0,
     "created": 1680893993,
     "livemode": false,
     "default_source": null,
     "metadata": {}
   }


Update a Customer
-----------------

**POST** ``/v1/customers/:id``

Parameters
~~~~~~~~~~

Any subset of fields can be updated. Pass an empty string to clear a field.

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Parameter
     - Type
     - Description
   * - ``full_name``
     - string
     - Full name or business name
   * - ``email``
     - string
     - Email address
   * - ``phone``
     - string
     - Phone number
   * - ``description``
     - string
     - Arbitrary string for display/notes
   * - ``metadata``
     - object
     - Key-value pairs. Set a key to empty string to unset it
   * - ``address``
     - object
     - Address: city, country, line1, line2, postal_code, state
   * - ``balance``
     - integer
     - Balance in cents. Negative = credit, positive = amount owed
   * - ``source``
     - string
     - New default payment source token or ID
   * - ``invoice_settings.default_source``
     - string
     - Default source ID for invoices/subscriptions

Returns
~~~~~~~

Returns the updated Customer object. Raises an error if parameters are invalid.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
     -u "<<YOUR_SECRET_KEY>>" \
     --data-urlencode email="alice@new.com"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "cus_NffrFeUfNV2Hib",
     "object": "customer",
     "full_name": "Jenny Rosen",
     "email": "alice@new.com",
     "balance": 0,
     "created": 1680893993,
     "livemode": false,
     "default_source": null,
     "metadata": {}
   }


Retrieve a Customer
-------------------

**GET** ``/v1/customers/:id``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``id``
     - string (path)
     - The ID of the customer to retrieve

Returns
~~~~~~~

Returns the Customer object for a valid identifier. If the customer was deleted, returns a subset with ``deleted: true``.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
     -u "<<YOUR_SECRET_KEY>>"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "cus_NffrFeUfNV2Hib",
     "object": "customer",
     "full_name": "Jenny Rosen",
     "email": "jennyrosen@example.com",
     "balance": 0,
     "delinquent": false,
     "created": 1680893993,
     "livemode": false,
     "default_source": null,
     "metadata": {}
   }


List All Customers
------------------

**GET** ``/v1/customers``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Parameter
     - Type
     - Required
     - Description
   * - ``email``
     - string
     - optional
     - Filter by exact email address (case-sensitive)
   * - ``limit``
     - integer
     - optional
     - Number of results to return (1–100, default 10)
   * - ``starting_after``
     - string
     - optional
     - Customer ID cursor — fetch the next page after this ID
   * - ``ending_before``
     - string
     - optional
     - Customer ID cursor — fetch the previous page before this ID
   * - ``created.gt``
     - integer
     - optional
     - Return customers created after this Unix timestamp (exclusive)
   * - ``created.gte``
     - integer
     - optional
     - Return customers created at or after this Unix timestamp (inclusive)
   * - ``created.lt``
     - integer
     - optional
     - Return customers created before this Unix timestamp (exclusive)
   * - ``created.lte``
     - integer
     - optional
     - Return customers created at or before this Unix timestamp (inclusive)

Returns
~~~~~~~

A dictionary with a ``data`` array of Customer objects, sorted newest first. Includes ``has_more`` boolean for pagination.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl -G https://api.stripe.com/v1/customers \
     -u "<<YOUR_SECRET_KEY>>" \
     -d limit=3

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "object": "list",
     "url": "/v1/customers",
     "has_more": false,
     "data": [
       {
         "id": "cus_NffrFeUfNV2Hib",
         "object": "customer",
         "full_name": "Jenny Rosen",
         "email": "jennyrosen@example.com",
         "balance": 0,
         "created": 1680893993,
         "livemode": false,
         "default_source": null,
         "metadata": {}
       }
     ]
   }
