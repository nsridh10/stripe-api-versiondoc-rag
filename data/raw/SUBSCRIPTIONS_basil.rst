Subscriptions
=============

Subscriptions allow you to charge a customer on a recurring basis.

.. note::

   In v1, subscriptions use ``plan`` instead of ``price`` to reference recurring billing configurations. The ``pause_collection`` feature is not available. ``default_payment_method`` is replaced by ``default_source``.

Endpoints
---------

.. list-table::
   :header-rows: 1
   :widths: 15 45 40

   * - Method
     - Endpoint
     - Description
   * - POST
     - ``/v1/subscriptions``
     - Create a subscription
   * - POST
     - ``/v1/subscriptions/:id``
     - Update a subscription
   * - GET
     - ``/v1/subscriptions/:id``
     - Retrieve a subscription
   * - GET
     - ``/v1/subscriptions``
     - List all subscriptions
   * - DELETE
     - ``/v1/subscriptions/:id``
     - Cancel a subscription
   * - POST
     - ``/v1/subscriptions/:id/resume``
     - Resume a paused subscription


The Subscription Object
-----------------------

Status Lifecycle
~~~~~~~~~~~~~~~~

``trialing`` → ``active`` → ``past_due`` → ``canceled`` / ``unpaid``

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
     - Unique identifier (e.g. ``sub_1MowQVLkdIwHu7ixeRlqHVzs``)
   * - ``object``
     - string
     - Always ``"subscription"``
   * - ``customer``
     - string
     - ID of the Customer being billed
   * - ``status``
     - enum
     - ``trialing``, ``active``, ``past_due``, ``canceled``, or ``unpaid``
   * - ``items.data``
     - array
     - List of subscription items, each with a ``plan`` and ``quantity``
   * - ``items.data[].plan.id``
     - string
     - ID of the Plan for this item
   * - ``items.data[].plan.amount``
     - integer
     - Plan amount in smallest currency unit
   * - ``items.data[].plan.interval``
     - string
     - Billing interval: ``day``, ``week``, ``month``, or ``year``
   * - ``items.data[].quantity``
     - integer
     - Quantity of the plan
   * - ``currency``
     - string
     - Three-letter ISO currency code
   * - ``collection_method``
     - enum
     - ``charge_automatically`` or ``send_invoice``
   * - ``default_source``
     - string
     - ID of default Source for this subscription
   * - ``latest_invoice``
     - string
     - ID of the most recent invoice
   * - ``billing_cycle_anchor``
     - timestamp
     - Reference point for billing cycle
   * - ``current_period_start``
     - timestamp
     - Start of the current billing period
   * - ``current_period_end``
     - timestamp
     - End of the current billing period
   * - ``cancel_at_period_end``
     - boolean
     - If ``true``, cancels at end of current period
   * - ``cancel_at``
     - timestamp
     - Scheduled cancellation timestamp
   * - ``canceled_at``
     - timestamp
     - When the subscription was canceled
   * - ``ended_at``
     - timestamp
     - When the subscription ended
   * - ``start_date``
     - timestamp
     - When the subscription started
   * - ``trial_start``
     - timestamp
     - Start of trial period
   * - ``trial_end``
     - timestamp
     - End of trial period
   * - ``description``
     - string
     - Arbitrary description
   * - ``metadata``
     - object
     - Key-value pairs for storing extra info
   * - ``on_behalf_of``
     - string
     - Connected account ID on whose behalf charges are made
   * - ``transfer_data.destination``
     - string
     - Connected account to transfer funds to
   * - ``application_fee_percent``
     - float
     - Percentage of subscription amount to collect for the platform
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
     "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
     "object": "subscription",
     "customer": "cus_Na6dX7aXxi11N4",
     "status": "active",
     "currency": "usd",
     "collection_method": "charge_automatically",
     "default_source": null,
     "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
     "billing_cycle_anchor": 1679609767,
     "start_date": 1679609767,
     "cancel_at_period_end": false,
     "cancel_at": null,
     "canceled_at": null,
     "ended_at": null,
     "trial_start": null,
     "trial_end": null,
     "description": null,
     "metadata": {},
     "on_behalf_of": null,
     "transfer_data": null,
     "created": 1679609767,
     "livemode": false,
     "items": {
       "object": "list",
       "data": [
         {
           "id": "si_Na6dzxczY5fwHx",
           "object": "subscription_item",
           "quantity": 1,
           "plan": {
             "id": "plan_Na6dGcTsmU0I4R",
             "object": "plan",
             "currency": "usd",
             "amount": 1000,
             "interval": "month",
             "interval_count": 1,
             "product": "prod_Na6dGcTsmU0I4R",
             "active": true
           }
         }
       ],
       "has_more": false
     }
   }


Create a Subscription
---------------------

**POST** ``/v1/subscriptions``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 15 30

   * - Parameter
     - Type
     - Required
     - Description
   * - ``customer``
     - string
     - **required**
     - ID of the Customer to subscribe
   * - ``items``
     - array
     - **required**
     - List of items. Each item needs a ``plan`` (Plan ID) and optional ``quantity`` (default 1)
   * - ``items[].plan``
     - string
     - required per item
     - ID of the Plan to subscribe to
   * - ``items[].quantity``
     - integer
     - optional
     - Quantity for this plan (default 1)
   * - ``currency``
     - enum
     - optional
     - Three-letter ISO currency code. Defaults to the plan's currency
   * - ``default_source``
     - string
     - optional
     - ID of default Source for this subscription
   * - ``collection_method``
     - enum
     - optional
     - ``charge_automatically`` (default) or ``send_invoice``
   * - ``days_until_due``
     - integer
     - optional
     - Days until invoice is due (required when ``collection_method=send_invoice``)
   * - ``proration_behavior``
     - enum
     - optional
     - ``create_prorations`` (default), ``none``, or ``always_invoice``
   * - ``billing_cycle_anchor``
     - timestamp
     - optional
     - Sets the billing cycle anchor to a specific Unix timestamp
   * - ``cancel_at_period_end``
     - boolean
     - optional
     - If ``true``, cancels at end of current period
   * - ``cancel_at``
     - timestamp
     - optional
     - Schedules cancellation at this Unix timestamp
   * - ``trial_period_days``
     - integer
     - optional
     - Number of trial days before billing starts
   * - ``trial_end``
     - timestamp or ``now``
     - optional
     - Ends trial at this Unix timestamp
   * - ``description``
     - string
     - optional
     - Arbitrary description
   * - ``metadata``
     - object
     - optional
     - Key-value pairs for storing extra info
   * - ``on_behalf_of``
     - string
     - optional
     - Connected account ID on whose behalf charges are made
   * - ``transfer_data.destination``
     - string
     - optional
     - Connected account to transfer funds to after each payment
   * - ``application_fee_percent``
     - float
     - optional
     - Percentage of amount to collect for the platform

Returns
~~~~~~~

Returns the created Subscription object.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/subscriptions \
     -u "<<YOUR_SECRET_KEY>>" \
     -d customer=cus_Na6dX7aXxi11N4 \
     -d "items[0][plan]"=plan_Na6dGcTsmU0I4R

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
     "object": "subscription",
     "customer": "cus_Na6dX7aXxi11N4",
     "status": "active",
     "currency": "usd",
     "collection_method": "charge_automatically",
     "default_source": null,
     "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
     "billing_cycle_anchor": 1679609767,
     "cancel_at_period_end": false,
     "metadata": {},
     "created": 1679609767,
     "livemode": false,
     "items": {
       "data": [
         {
           "id": "si_Na6dzxczY5fwHx",
           "quantity": 1,
           "plan": {
             "id": "plan_Na6dGcTsmU0I4R",
             "amount": 1000,
             "currency": "usd",
             "interval": "month",
             "interval_count": 1
           }
         }
       ]
     }
   }


Update a Subscription
---------------------

**POST** ``/v1/subscriptions/:id``

Updates an existing subscription. Used for upgrading/downgrading plans, changing quantities, and more. Stripe optionally prorates charges when plans or quantities change.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Parameter
     - Type
     - Description
   * - ``items``
     - array
     - Updated list of items. Each can include ``id`` (existing item ID), ``plan``, ``quantity``, or ``deleted: true`` to remove
   * - ``items[].id``
     - string
     - ID of existing subscription item to modify
   * - ``items[].plan``
     - string
     - New Plan ID to switch to
   * - ``items[].quantity``
     - integer
     - Updated quantity
   * - ``items[].deleted``
     - boolean
     - Set ``true`` to remove this item
   * - ``default_source``
     - string
     - ID of new default Source
   * - ``collection_method``
     - enum
     - ``charge_automatically`` or ``send_invoice``
   * - ``days_until_due``
     - integer
     - Days until invoice is due (for ``send_invoice``)
   * - ``proration_behavior``
     - enum
     - ``create_prorations`` (default), ``none``, or ``always_invoice``
   * - ``proration_date``
     - timestamp
     - Calculate prorations as if change happened at this time
   * - ``billing_cycle_anchor``
     - ``now`` or ``unchanged``
     - Reset billing anchor to now, or keep unchanged
   * - ``cancel_at_period_end``
     - boolean
     - Set ``true`` to cancel at end of period
   * - ``cancel_at``
     - timestamp or ``""``
     - Schedule/unschedule cancellation
   * - ``trial_end``
     - timestamp or ``now``
     - End the trial at this time
   * - ``description``
     - string
     - Arbitrary description
   * - ``metadata``
     - object
     - Key-value pairs. Set key to ``""`` to unset

Returns
~~~~~~~

Returns the updated Subscription object.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
     -u "<<YOUR_SECRET_KEY>>" \
     -d "metadata[order_id]"=6735

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
     "object": "subscription",
     "customer": "cus_Na6dX7aXxi11N4",
     "status": "active",
     "currency": "usd",
     "default_source": null,
     "cancel_at_period_end": false,
     "metadata": { "order_id": "6735" },
     "created": 1679609767,
     "livemode": false,
     "items": {
       "data": [
         {
           "id": "si_Na6dzxczY5fwHx",
           "quantity": 1,
           "plan": {
             "id": "plan_Na6dGcTsmU0I4R",
             "amount": 1000,
             "currency": "usd",
             "interval": "month"
           }
         }
       ]
     }
   }


Retrieve a Subscription
-----------------------

**GET** ``/v1/subscriptions/:id``

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
     - The ID of the subscription to retrieve

Returns
~~~~~~~

Returns the Subscription object.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
     -u "<<YOUR_SECRET_KEY>>"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
     "object": "subscription",
     "customer": "cus_Na6dX7aXxi11N4",
     "status": "active",
     "currency": "usd",
     "collection_method": "charge_automatically",
     "default_source": null,
     "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
     "billing_cycle_anchor": 1679609767,
     "cancel_at_period_end": false,
     "trial_start": null,
     "trial_end": null,
     "metadata": {},
     "created": 1679609767,
     "livemode": false,
     "items": {
       "data": [
         {
           "id": "si_Na6dzxczY5fwHx",
           "quantity": 1,
           "plan": {
             "id": "plan_Na6dGcTsmU0I4R",
             "amount": 1000,
             "currency": "usd",
             "interval": "month",
             "interval_count": 1
           }
         }
       ]
     }
   }


List Subscriptions
------------------

**GET** ``/v1/subscriptions``

By default, returns subscriptions that have not been canceled. Use ``status=canceled`` to include canceled ones.

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
     - Filter by customer ID
   * - ``plan``
     - string
     - optional
     - Filter by Plan ID
   * - ``status``
     - enum
     - optional
     - Filter by status: ``active``, ``canceled``, ``past_due``, ``trialing``, ``unpaid``, or ``all``
   * - ``collection_method``
     - enum
     - optional
     - ``charge_automatically`` or ``send_invoice``
   * - ``limit``
     - integer
     - optional
     - Number of results (1–100, default 10)
   * - ``starting_after``
     - string
     - optional
     - Subscription ID cursor — fetch next page after this ID
   * - ``ending_before``
     - string
     - optional
     - Subscription ID cursor — fetch previous page before this ID
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

A dictionary with a ``data`` array of Subscription objects. Includes ``has_more`` for pagination.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl -G https://api.stripe.com/v1/subscriptions \
     -u "<<YOUR_SECRET_KEY>>" \
     -d limit=3

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "object": "list",
     "url": "/v1/subscriptions",
     "has_more": false,
     "data": [
       {
         "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
         "object": "subscription",
         "customer": "cus_Na6dX7aXxi11N4",
         "status": "active",
         "currency": "usd",
         "default_source": null,
         "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
         "cancel_at_period_end": false,
         "metadata": {},
         "created": 1679609767,
         "livemode": false,
         "items": {
           "data": [
             {
               "id": "si_Na6dzxczY5fwHx",
               "quantity": 1,
               "plan": {
                 "id": "plan_Na6dGcTsmU0I4R",
                 "amount": 1000,
                 "currency": "usd",
                 "interval": "month"
               }
             }
           ]
         }
       }
     ]
   }


Cancel a Subscription
---------------------

**DELETE** ``/v1/subscriptions/:id``

Cancels a subscription immediately. The customer won't be charged again.

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
     - The ID of the subscription to cancel
   * - ``invoice_now``
     - boolean
     - optional
     - If ``true``, generates a final invoice for un-invoiced usage. Default ``false``
   * - ``prorate``
     - boolean
     - optional
     - If ``true``, generates a proration credit for unused time. Default ``false``

Returns
~~~~~~~

Returns the canceled Subscription object with ``status: "canceled"``.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl -X DELETE https://api.stripe.com/v1/subscriptions/sub_1MlPf9LkdIwHu7ixB6VIYRyX \
     -u "<<YOUR_SECRET_KEY>>"

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "sub_1MlPf9LkdIwHu7ixB6VIYRyX",
     "object": "subscription",
     "customer": "cus_NWSaVkvdacCUi4",
     "status": "canceled",
     "currency": "usd",
     "canceled_at": 1678768842,
     "ended_at": 1678768842,
     "cancel_at_period_end": false,
     "metadata": {},
     "created": 1678768838,
     "livemode": false,
     "items": {
       "data": [
         {
           "id": "si_NWSaWTp80M123q",
           "quantity": 1,
           "plan": {
             "id": "plan_NWSaMgipulx8IQ",
             "amount": 1099,
             "currency": "usd",
             "interval": "month"
           }
         }
       ]
     }
   }


Resume a Subscription
---------------------

**POST** ``/v1/subscriptions/:id/resume``

Resumes a subscription that was canceled with ``cancel_at_period_end=true`` and has not yet reached the period end. Not applicable for immediately canceled subscriptions.

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
     - The ID of the subscription to resume
   * - ``billing_cycle_anchor``
     - enum
     - optional
     - ``now`` (default) resets billing cycle; ``unchanged`` keeps existing anchor
   * - ``proration_behavior``
     - enum
     - optional
     - ``create_prorations`` (default), ``none``, or ``always_invoice``

Returns
~~~~~~~

Returns the Subscription object with ``status: "active"``.

Example Request
~~~~~~~~~~~~~~~

.. code-block:: bash

   curl https://api.stripe.com/v1/subscriptions/sub_1MoGGtLkdIwHu7ixk5CfdiqC/resume \
     -u "<<YOUR_SECRET_KEY>>" \
     -d billing_cycle_anchor=now

Example Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",
     "object": "subscription",
     "customer": "cus_NZP5i1diUz55jp",
     "status": "active",
     "currency": "usd",
     "billing_cycle_anchor": 1679447726,
     "default_source": null,
     "latest_invoice": "in_1MoGGwLkdIwHu7ixHSrelo8X",
     "cancel_at_period_end": false,
     "metadata": {},
     "created": 1679447723,
     "livemode": false,
     "items": {
       "data": [
         {
           "id": "si_NZP5BhUIuWzXDG",
           "quantity": 1,
           "plan": {
             "id": "plan_NZP5rEATBlScM9",
             "amount": 1099,
             "currency": "usd",
             "interval": "month"
           }
         }
       ]
     }
   }
