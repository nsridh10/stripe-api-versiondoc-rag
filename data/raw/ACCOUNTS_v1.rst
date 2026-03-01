Accounts
========

An Account represents a Stripe connected account on your platform. Use Stripe Connect to create and manage accounts for your users.

Endpoints
---------

.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - POST
     - ``/v1/accounts``
     - Create a connected account
   * - GET
     - ``/v1/accounts/:id``
     - Retrieve an account
   * - GET
     - ``/v1/accounts``
     - List all connected accounts


The Account Object
------------------

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
     - Unique identifier (e.g. ``acct_1Nv0FGQ9RKHgCVdK``)
   * - ``object``
     - string
     - Always ``"account"``
   * - ``email``
     - string
     - Account's email address
   * - ``country``
     - string
     - Two-letter ISO country code
   * - ``default_currency``
     - string
     - Three-letter ISO currency code
   * - ``type``
     - enum
     - Account type: ``standard``, ``express``, or ``custom``
   * - ``business_name``
     - string
     - The business's display name
   * - ``business_url``
     - string
     - The business's publicly available website
   * - ``charges_enabled``
     - boolean
     - Whether the account can process charges
   * - ``payouts_enabled``
     - boolean
     - Whether the account can receive payouts
   * - ``details_submitted``
     - boolean
     - Whether required onboarding details have been submitted
   * - ``created``
     - timestamp
     - Unix timestamp of creation
   * - ``metadata``
     - object
     - Key-value pairs for storing extra info
   * - ``verification.disabled_reason``
     - string
     - Reason the account is disabled, if applicable
   * - ``verification.fields_needed``
     - array
     - Fields that must be collected to keep the account enabled

Example Object
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "acct_1Nv0FGQ9RKHgCVdK",
     "object": "account",
     "email": "jenny.rosen@example.com",
     "country": "US",
     "default_currency": "usd",
     "type": "express",
     "business_name": null,
     "business_url": null,
     "charges_enabled": false,
     "payouts_enabled": false,
     "details_submitted": false,
     "created": 1695830751,
     "metadata": {},
     "verification": {
       "disabled_reason": "fields_needed",
       "fields_needed": ["business_url", "external_account", "tos_acceptance.date"]
     }
   }


Create an Account
-----------------

**POST** ``/v1/accounts``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 15 30

   * - Parameter
     - Type
     - Required
     - Description
   * - ``type``
     - enum
     - optional
     - Account type: ``standard``, ``express``, or ``custom``
   * - ``country``
     - string
     - optional
     - Two-letter ISO country code (defaults to platform country)
   * - ``email``
     - string
     - optional
     - Account's email address
   * - ``business_name``
     - string
     - optional
     - The business's display name
   * - ``business_url``
     - string
     - optional
     - The business's publicly available website
   * - ``support_email``
     - string
     - optional
     - Public support email
   * - ``support_phone``
     - string
     - optional
     - Public support phone
   * - ``metadata``
     - object
     - optional
     - Key-value pairs for storing extra info
   * - ``tos_acceptance.date``
     - timestamp
     - optional
     - Unix timestamp when account rep accepted ToS
   * - ``tos_acceptance.ip``
     - string
     - optional
     - IP address from which ToS was accepted

Returns
~~~~~~~

Returns an Account object if the call succeeds.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/accounts \
     -u "<<YOUR_SECRET_KEY>>" \
     -d type=express \
     -d country=US \
     --data-urlencode email="jenny.rosen@example.com"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "acct_1Nv0FGQ9RKHgCVdK",
     "object": "account",
     "email": "jenny.rosen@example.com",
     "country": "US",
     "default_currency": "usd",
     "type": "express",
     "charges_enabled": false,
     "payouts_enabled": false,
     "details_submitted": false,
     "created": 1695830751,
     "metadata": {},
     "verification": {
       "disabled_reason": "fields_needed",
       "fields_needed": ["business_url", "external_account"]
     }
   }


Retrieve an Account
-------------------

**GET** ``/v1/accounts/:id``

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
     - The ID of the account to retrieve

Returns
~~~~~~~

Returns an Account object if the call succeeds. Raises an error if the account ID does not exist.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/accounts/acct_1Nv0FGQ9RKHgCVdK \
     -u "<<YOUR_SECRET_KEY>>"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "acct_1Nv0FGQ9RKHgCVdK",
     "object": "account",
     "email": "jenny.rosen@example.com",
     "country": "US",
     "default_currency": "usd",
     "type": "express",
     "charges_enabled": false,
     "payouts_enabled": false,
     "details_submitted": false,
     "created": 1695830751,
     "metadata": {},
     "verification": {
       "disabled_reason": "fields_needed",
       "fields_needed": ["business_url", "external_account", "tos_acceptance.date"]
     }
   }


List All Connected Accounts
---------------------------

**GET** ``/v1/accounts``

Returns a list of accounts connected to your platform via Connect. If you're not a platform, the list is empty.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Parameter
     - Type
     - Required
     - Description
   * - ``limit``
     - integer
     - optional
     - Number of results to return (1–100, default 10)
   * - ``starting_after``
     - string
     - optional
     - Account ID cursor — fetch the next page after this ID
   * - ``ending_before``
     - string
     - optional
     - Account ID cursor — fetch the previous page before this ID
   * - ``created.gt``
     - integer
     - optional
     - Return accounts created after this Unix timestamp (exclusive)
   * - ``created.gte``
     - integer
     - optional
     - Return accounts created at or after this Unix timestamp (inclusive)
   * - ``created.lt``
     - integer
     - optional
     - Return accounts created before this Unix timestamp (exclusive)
   * - ``created.lte``
     - integer
     - optional
     - Return accounts created at or before this Unix timestamp (inclusive)

Returns
~~~~~~~

A dictionary with a ``data`` array of Account objects. Includes ``has_more`` for pagination.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl -G https://api.stripe.com/v1/accounts \
     -u "<<YOUR_SECRET_KEY>>" \
     -d limit=3

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "object": "list",
     "url": "/v1/accounts",
     "has_more": false,
     "data": [
       {
         "id": "acct_1Nv0FGQ9RKHgCVdK",
         "object": "account",
         "email": "jenny.rosen@example.com",
         "country": "US",
         "default_currency": "usd",
         "type": "express",
         "charges_enabled": false,
         "payouts_enabled": false,
         "details_submitted": false,
         "created": 1695830751,
         "metadata": {},
         "verification": {
           "disabled_reason": "fields_needed",
           "fields_needed": ["business_url", "external_account"]
         }
       }
     ]
   }
