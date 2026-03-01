PaymentIntents
==============

A PaymentIntent guides you through collecting a payment from a customer. Create exactly one per order or session.

.. note::

   In v1, ``automatic_payment_methods`` is not supported. Payment method types must be explicitly specified via ``payment_method_types``. The ``confirmation_method`` field is also not available; all confirmations are manual by default.

Endpoints
---------

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Method
     - Endpoint
     - Description
   * - POST
     - ``/v1/payment_intents``
     - Create a PaymentIntent
   * - POST
     - ``/v1/payment_intents/:id/confirm``
     - Confirm a PaymentIntent
   * - GET
     - ``/v1/payment_intents/:id``
     - Retrieve a PaymentIntent
   * - GET
     - ``/v1/payment_intents``
     - List all PaymentIntents
   * - POST
     - ``/v1/payment_intents/:id/cancel``
     - Cancel a PaymentIntent


The PaymentIntent Object
------------------------

Status Lifecycle
~~~~~~~~~~~~~~~~

``requires_payment_method`` → ``requires_confirmation`` → ``requires_action`` → ``processing`` → ``succeeded``

Or: → ``requires_capture`` (if ``capture_method=manual``) | ``canceled``

Key Fields
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Field
     - Type
     - Description
   * - ``id``
     - string
     - Unique identifier (e.g. ``pi_3MtwBwLkdIwHu7ix28a3tqPa``)
   * - ``object``
     - string
     - Always ``"payment_intent"``
   * - ``amount``
     - integer
     - Amount in smallest currency unit (e.g. cents)
   * - ``currency``
     - string
     - Three-letter ISO currency code (e.g. ``"usd"``)
   * - ``status``
     - enum
     - Current status (see lifecycle above)
   * - ``customer``
     - string
     - ID of the Customer this PaymentIntent belongs to
   * - ``source``
     - string
     - ID of the Source or card token to charge
   * - ``payment_method_types``
     - array
     - Explicit list of allowed payment method types (e.g. ``["card"]``)
   * - ``capture_method``
     - enum
     - ``automatic`` or ``manual``
   * - ``amount_received``
     - integer
     - Amount successfully received, in smallest currency unit
   * - ``amount_capturable``
     - integer
     - Amount that can still be captured (manual capture only)
   * - ``client_secret``
     - string
     - Secret used client-side to confirm the PaymentIntent
   * - ``latest_charge``
     - string
     - ID of the latest Charge created
   * - ``last_payment_error``
     - object
     - Error from the last payment attempt, if any
   * - ``next_action``
     - object
     - Actions required to complete the payment (e.g. 3D Secure redirect)
   * - ``canceled_at``
     - timestamp
     - When the PaymentIntent was canceled
   * - ``cancellation_reason``
     - string
     - Reason for cancellation
   * - ``description``
     - string
     - Arbitrary description
   * - ``metadata``
     - object
     - Key-value pairs for storing extra info
   * - ``receipt_email``
     - string
     - Email to send receipt to after successful payment
   * - ``statement_descriptor``
     - string
     - Text on customer's bank statement (max 22 chars)
   * - ``on_behalf_of``
     - string
     - Connected account ID on whose behalf the charge is made
   * - ``transfer_data.destination``
     - string
     - Connected account to transfer funds to after success
   * - ``application_fee_amount``
     - integer
     - Fee in cents to be collected for the platform
   * - ``created``
     - timestamp
     - Unix timestamp of creation
   * - ``livemode``
     - boolean
     - True if live mode, false if test mode

Example Object
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
     "object": "payment_intent",
     "amount": 2000,
     "currency": "usd",
     "status": "requires_source",
     "customer": null,
     "source": null,
     "payment_method_types": ["card"],
     "capture_method": "automatic",
     "amount_received": 0,
     "amount_capturable": 0,
     "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
     "latest_charge": null,
     "last_payment_error": null,
     "next_action": null,
     "canceled_at": null,
     "cancellation_reason": null,
     "description": null,
     "metadata": {},
     "receipt_email": null,
     "statement_descriptor": null,
     "on_behalf_of": null,
     "transfer_data": null,
     "application_fee_amount": null,
     "created": 1680800504,
     "livemode": false
   }


Create a PaymentIntent
----------------------

**POST** ``/v1/payment_intents``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 15 30

   * - Parameter
     - Type
     - Required
     - Description
   * - ``amount``
     - integer
     - **required**
     - Amount in smallest currency unit (e.g. 2000 = $20.00 USD)
   * - ``currency``
     - enum
     - **required**
     - Three-letter ISO currency code (e.g. ``usd``)
   * - ``payment_method_types``
     - array
     - **required**
     - List of payment method types (e.g. ``["card"]``). No default in v1
   * - ``customer``
     - string
     - optional
     - ID of the Customer to attach this PaymentIntent to
   * - ``source``
     - string
     - optional
     - ID of a Source or card token to attach
   * - ``capture_method``
     - enum
     - optional
     - ``automatic`` (default) charges immediately; ``manual`` requires a separate capture step
   * - ``confirm``
     - boolean
     - optional
     - If ``true``, confirm immediately upon creation
   * - ``description``
     - string
     - optional
     - Arbitrary description
   * - ``metadata``
     - object
     - optional
     - Key-value pairs for storing extra info
   * - ``receipt_email``
     - string
     - optional
     - Email to send receipt to after successful payment
   * - ``statement_descriptor``
     - string
     - optional
     - Text on customer's bank statement (max 22 chars)
   * - ``on_behalf_of``
     - string
     - optional
     - Connected account ID on whose behalf the charge is made
   * - ``transfer_data.destination``
     - string
     - optional
     - Connected account to transfer funds to after success
   * - ``application_fee_amount``
     - integer
     - optional
     - Fee in cents to collect for the platform (requires ``on_behalf_of``)
   * - ``return_url``
     - string
     - optional
     - URL to redirect to after actions (e.g. 3D Secure) are completed

Returns
~~~~~~~

Returns a PaymentIntent object.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/payment_intents \
     -u "<<YOUR_SECRET_KEY>>" \
     -d amount=2000 \
     -d currency=usd \
     -d "payment_method_types[0]"=card

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
     "object": "payment_intent",
     "amount": 2000,
     "currency": "usd",
     "status": "requires_source",
     "customer": null,
     "source": null,
     "payment_method_types": ["card"],
     "capture_method": "automatic",
     "amount_received": 0,
     "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
     "latest_charge": null,
     "next_action": null,
     "description": null,
     "metadata": {},
     "created": 1680800504,
     "livemode": false
   }


Confirm a PaymentIntent
-----------------------

**POST** ``/v1/payment_intents/:id/confirm``

Confirms that the customer intends to pay. Upon confirmation, the PaymentIntent will attempt to initiate a payment.

- If additional auth is needed (e.g. 3D Secure), status moves to ``requires_action`` with ``next_action`` populated.
- If payment fails, status moves to ``requires_source``.
- If payment succeeds, status moves to ``succeeded`` (or ``requires_capture`` if ``capture_method=manual``).

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 15 35

   * - Parameter
     - Type
     - Required
     - Description
   * - ``source``
     - string
     - optional
     - ID of the Source or card token to use for this confirmation
   * - ``return_url``
     - string
     - optional
     - URL to redirect to after any required actions (e.g. 3D Secure)
   * - ``capture_method``
     - enum
     - optional
     - Override capture method: ``automatic`` or ``manual``
   * - ``receipt_email``
     - string
     - optional
     - Email to send receipt to after successful payment

Returns
~~~~~~~

Returns the resulting PaymentIntent after all possible transitions are applied.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/payment_intents/pi_3MtweELkdIwHu7ix0Dt0gF2H/confirm \
     -u "<<YOUR_SECRET_KEY>>" \
     -d source=tok_visa \
     --data-urlencode return_url="https://www.example.com"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "pi_3MtweELkdIwHu7ix0Dt0gF2H",
     "object": "payment_intent",
     "amount": 2000,
     "currency": "usd",
     "status": "succeeded",
     "source": "src_1MtweELkdIwHu7ixxrsejPtG",
     "payment_method_types": ["card"],
     "capture_method": "automatic",
     "amount_received": 2000,
     "amount_capturable": 0,
     "client_secret": "pi_3MtweELkdIwHu7ix0Dt0gF2H_secret_ALlpPMIZse0ac8YzPxkMkFgGC",
     "latest_charge": "ch_3MtweELkdIwHu7ix05lnLAFd",
     "next_action": null,
     "metadata": {},
     "created": 1680802258,
     "livemode": false
   }


Retrieve a PaymentIntent
------------------------

**GET** ``/v1/payment_intents/:id``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Type
     - Description
   * - ``id``
     - string (path)
     - The ID of the PaymentIntent to retrieve

Returns
~~~~~~~

Returns a PaymentIntent if a valid identifier was provided.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \
     -u "<<YOUR_SECRET_KEY>>"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
     "object": "payment_intent",
     "amount": 2000,
     "currency": "usd",
     "status": "requires_source",
     "source": null,
     "payment_method_types": ["card"],
     "capture_method": "automatic",
     "amount_received": 0,
     "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
     "latest_charge": null,
     "canceled_at": null,
     "description": null,
     "metadata": {},
     "created": 1680800504,
     "livemode": false
   }


List All PaymentIntents
-----------------------

**GET** ``/v1/payment_intents``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - Parameter
     - Type
     - Required
     - Description
   * - ``customer``
     - string
     - optional
     - Only return PaymentIntents for this customer ID
   * - ``limit``
     - integer
     - optional
     - Number of results to return (1–100, default 10)
   * - ``starting_after``
     - string
     - optional
     - PaymentIntent ID cursor — fetch the next page after this ID
   * - ``ending_before``
     - string
     - optional
     - PaymentIntent ID cursor — fetch the previous page before this ID
   * - ``created.gt``
     - integer
     - optional
     - Created after this Unix timestamp (exclusive)
   * - ``created.gte``
     - integer
     - optional
     - Created at or after this Unix timestamp (inclusive)
   * - ``created.lt``
     - integer
     - optional
     - Created before this Unix timestamp (exclusive)
   * - ``created.lte``
     - integer
     - optional
     - Created at or before this Unix timestamp (inclusive)

Returns
~~~~~~~

A dictionary with a ``data`` array of PaymentIntent objects. Includes ``has_more`` for pagination.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl -G https://api.stripe.com/v1/payment_intents \
     -u "<<YOUR_SECRET_KEY>>" \
     -d limit=3

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "object": "list",
     "url": "/v1/payment_intents",
     "has_more": false,
     "data": [
       {
         "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
         "object": "payment_intent",
         "amount": 2000,
         "currency": "usd",
         "status": "requires_source",
         "source": null,
         "payment_method_types": ["card"],
         "capture_method": "automatic",
         "amount_received": 0,
         "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
         "description": null,
         "metadata": {},
         "created": 1680800504,
         "livemode": false
       }
     ]
   }


Cancel a PaymentIntent
----------------------

**POST** ``/v1/payment_intents/:id/cancel``

Cancels a PaymentIntent. Cancelable when status is: ``requires_source``, ``requires_capture``, ``requires_confirmation``, ``requires_action``, or (rarely) ``processing``.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 15 35

   * - Parameter
     - Type
     - Required
     - Description
   * - ``id``
     - string (path)
     - **required**
     - The ID of the PaymentIntent to cancel
   * - ``cancellation_reason``
     - string
     - optional
     - Reason: ``duplicate``, ``fraudulent``, ``requested_by_customer``, or ``abandoned``

Returns
~~~~~~~

Returns the canceled PaymentIntent object. Returns an error if already canceled or not in a cancelable state.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/cancel \
     -u "<<YOUR_SECRET_KEY>>"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
     "object": "payment_intent",
     "amount": 2000,
     "currency": "usd",
     "status": "canceled",
     "source": null,
     "payment_method_types": ["card"],
     "amount_received": 0,
     "canceled_at": 1680801569,
     "cancellation_reason": null,
     "metadata": {},
     "created": 1680800504,
     "livemode": false
   }
