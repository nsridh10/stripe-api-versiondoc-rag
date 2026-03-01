# The Subscription Object

A Subscription charges a customer on a recurring basis using a Price attached to a Product.

## Status Lifecycle

`incomplete` → `active` → `past_due` → `canceled` / `unpaid`  
Or: `trialing` → `active` | `paused` (when `pause_collection` is set)

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g. `sub_1MowQVLkdIwHu7ixeRlqHVzs`) |
| `object` | string | Always `"subscription"` |
| `customer` | string | ID of the Customer being billed |
| `status` | enum | `incomplete`, `incomplete_expired`, `trialing`, `active`, `past_due`, `canceled`, `unpaid`, or `paused` |
| `items.data` | array | List of subscription items, each with a `price` and `quantity` |
| `items.data[].price.id` | string | ID of the Price for this item |
| `items.data[].price.unit_amount` | integer | Price amount in smallest currency unit |
| `items.data[].price.recurring.interval` | string | Billing interval: `day`, `week`, `month`, or `year` |
| `items.data[].quantity` | integer | Quantity of the price |
| `currency` | string | Three-letter ISO currency code |
| `collection_method` | enum | `charge_automatically` or `send_invoice` |
| `default_payment_method` | string | ID of default PaymentMethod for this subscription |
| `latest_invoice` | string | ID of the most recent invoice |
| `current_period_start` | timestamp | Start of the current billing period |
| `current_period_end` | timestamp | End of the current billing period |
| `billing_cycle_anchor` | timestamp | Reference point for billing cycle |
| `cancel_at_period_end` | boolean | If `true`, cancels at end of current period |
| `cancel_at` | timestamp | Scheduled cancellation timestamp |
| `canceled_at` | timestamp | When the subscription was canceled |
| `ended_at` | timestamp | When the subscription ended |
| `start_date` | timestamp | When the subscription started |
| `trial_start` | timestamp | Start of trial period |
| `trial_end` | timestamp | End of trial period |
| `pause_collection` | object | If set, collection is paused. Contains `behavior` and optional `resumes_at` |
| `description` | string | Arbitrary description |
| `metadata` | object | Key-value pairs for storing extra info |
| `on_behalf_of` | string | Connected account ID on whose behalf charges are made |
| `transfer_data.destination` | string | Connected account to transfer funds to |
| `application_fee_percent` | float | Percentage of subscription amount to collect for the platform |
| `proration_behavior` | enum | How prorations are handled on updates: `create_prorations`, `none`, or `always_invoice` |
| `created` | timestamp | Unix timestamp of creation |
| `livemode` | boolean | True if live mode, false if test mode |

## Example Object

```json
{
  "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
  "object": "subscription",
  "customer": "cus_Na6dX7aXxi11N4",
  "status": "active",
  "currency": "usd",
  "collection_method": "charge_automatically",
  "default_payment_method": null,
  "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
  "billing_cycle_anchor": 1679609767,
  "start_date": 1679609767,
  "cancel_at_period_end": false,
  "cancel_at": null,
  "canceled_at": null,
  "ended_at": null,
  "trial_start": null,
  "trial_end": null,
  "pause_collection": null,
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
        "price": {
          "id": "price_1MowQULkdIwHu7ixraBm864M",
          "object": "price",
          "currency": "usd",
          "unit_amount": 1000,
          "type": "recurring",
          "recurring": {
            "interval": "month",
            "interval_count": 1
          },
          "product": "prod_Na6dGcTsmU0I4R",
          "active": true
        }
      }
    ],
    "has_more": false
  }
}
```
# Subscriptions

Subscriptions allow you to charge a customer on a recurring basis.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/subscriptions` | Create a subscription |
| POST | `/v1/subscriptions/:id` | Update a subscription |
| GET | `/v1/subscriptions/:id` | Retrieve a subscription |
| GET | `/v1/subscriptions` | List all subscriptions |
| DELETE | `/v1/subscriptions/:id` | Cancel a subscription |
| POST | `/v1/subscriptions/:id/resume` | Resume a paused subscription |
# Create a Subscription

**POST** `/v1/subscriptions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `customer` | string | **required** | ID of the Customer to subscribe |
| `items` | array | **required** | List of items. Each item needs a `price` (Price ID) and optional `quantity` (default 1) |
| `items[].price` | string | required per item | ID of the Price to subscribe to |
| `items[].quantity` | integer | optional | Quantity for this price (default 1) |
| `currency` | enum | optional | Three-letter ISO currency code. Defaults to the price's currency |
| `default_payment_method` | string | optional | ID of default PaymentMethod for this subscription |
| `collection_method` | enum | optional | `charge_automatically` (default) or `send_invoice` |
| `days_until_due` | integer | optional | Days until invoice is due (required when `collection_method=send_invoice`) |
| `payment_behavior` | enum | optional | `allow_incomplete`, `error_if_incomplete` (default), or `default_incomplete` |
| `proration_behavior` | enum | optional | `create_prorations` (default), `none`, or `always_invoice` |
| `billing_cycle_anchor` | timestamp | optional | Sets the billing cycle anchor to a specific Unix timestamp |
| `cancel_at_period_end` | boolean | optional | If `true`, cancels at end of current period |
| `cancel_at` | timestamp | optional | Schedules cancellation at this Unix timestamp |
| `trial_period_days` | integer | optional | Number of trial days before billing starts |
| `trial_end` | timestamp or `now` | optional | Ends trial at this Unix timestamp |
| `description` | string | optional | Arbitrary description |
| `metadata` | object | optional | Key-value pairs for storing extra info |
| `on_behalf_of` | string | optional | Connected account ID on whose behalf charges are made |
| `transfer_data.destination` | string | optional | Connected account to transfer funds to after each payment |
| `application_fee_percent` | float | optional | Percentage of amount to collect for the platform |
| `off_session` | boolean | optional | Set `true` if customer is not actively in your checkout flow |

## Returns

Returns the created Subscription object.

## Example Request

```curl
curl https://api.stripe.com/v1/subscriptions \
  -u "<<YOUR_SECRET_KEY>>" \
  -d customer=cus_Na6dX7aXxi11N4 \
  -d "items[0][price]"=price_1MowQULkdIwHu7ixraBm864M
```

## Example Response

```json
{
  "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
  "object": "subscription",
  "customer": "cus_Na6dX7aXxi11N4",
  "status": "active",
  "currency": "usd",
  "collection_method": "charge_automatically",
  "default_payment_method": null,
  "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
  "billing_cycle_anchor": 1679609767,
  "start_date": 1679609767,
  "cancel_at_period_end": false,
  "trial_start": null,
  "trial_end": null,
  "metadata": {},
  "created": 1679609767,
  "livemode": false,
  "items": {
    "object": "list",
    "data": [
      {
        "id": "si_Na6dzxczY5fwHx",
        "quantity": 1,
        "price": {
          "id": "price_1MowQULkdIwHu7ixraBm864M",
          "currency": "usd",
          "unit_amount": 1000,
          "recurring": { "interval": "month", "interval_count": 1 }
        }
      }
    ]
  }
}
```
# Update a Subscription

**POST** `/v1/subscriptions/:id`

Updates an existing subscription. Used for upgrading/downgrading plans, changing quantities, pausing collection, and more. Stripe optionally prorates charges when prices or quantities change.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `items` | array | optional | Updated list of items. Each can include `id` (existing item ID), `price`, `quantity`, or `deleted: true` to remove |
| `items[].id` | string | optional | ID of existing subscription item to modify |
| `items[].price` | string | optional | New Price ID to switch to |
| `items[].quantity` | integer | optional | Updated quantity |
| `items[].deleted` | boolean | optional | Set `true` to remove this item |
| `default_payment_method` | string | optional | ID of new default PaymentMethod |
| `collection_method` | enum | optional | `charge_automatically` or `send_invoice` |
| `days_until_due` | integer | optional | Days until invoice is due (for `send_invoice`) |
| `proration_behavior` | enum | optional | `create_prorations` (default), `none`, or `always_invoice` |
| `proration_date` | timestamp | optional | Calculate prorations as if change happened at this time |
| `billing_cycle_anchor` | `now` or `unchanged` | optional | Reset billing anchor to now, or keep unchanged |
| `cancel_at_period_end` | boolean | optional | Set `true` to cancel at end of period, `false` to undo |
| `cancel_at` | timestamp or `""` | optional | Schedule/unschedule cancellation |
| `trial_end` | timestamp or `now` | optional | End the trial at this time |
| `pause_collection` | object | optional | Pause billing. Set `behavior` to `keep_as_draft`, `mark_uncollectible`, or `void`. Set to `""` to resume |
| `pause_collection.behavior` | enum | optional | What to do with invoices while paused |
| `pause_collection.resumes_at` | timestamp | optional | Auto-resume at this timestamp |
| `payment_behavior` | enum | optional | `allow_incomplete`, `error_if_incomplete`, or `default_incomplete` |
| `description` | string | optional | Arbitrary description |
| `metadata` | object | optional | Key-value pairs. Set key to `""` to unset |
| `on_behalf_of` | string | optional | Connected account ID |
| `transfer_data` | object | optional | Set destination for fund transfers, or `""` to remove |
| `cancellation_details.comment` | string | optional | Comment about why subscription is being changed |
| `cancellation_details.feedback` | enum | optional | Customer feedback reason |

## Returns

Returns the updated Subscription object.

## Example Request

```curl
curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
  -u "<<YOUR_SECRET_KEY>>" \
  -d "metadata[order_id]"=6735
```

## Example Response

```json
{
  "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
  "object": "subscription",
  "customer": "cus_Na6dX7aXxi11N4",
  "status": "active",
  "currency": "usd",
  "collection_method": "charge_automatically",
  "default_payment_method": null,
  "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
  "cancel_at_period_end": false,
  "pause_collection": null,
  "metadata": { "order_id": "6735" },
  "created": 1679609767,
  "livemode": false,
  "items": {
    "object": "list",
    "data": [
      {
        "id": "si_Na6dzxczY5fwHx",
        "quantity": 1,
        "price": {
          "id": "price_1MowQULkdIwHu7ixraBm864M",
          "currency": "usd",
          "unit_amount": 1000,
          "recurring": { "interval": "month", "interval_count": 1 }
        }
      }
    ]
  }
}
```
# Retrieve a Subscription

**GET** `/v1/subscriptions/:id`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string (path) | The ID of the subscription to retrieve |

## Returns

Returns the Subscription object.

## Example Request

```curl
curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
  -u "<<YOUR_SECRET_KEY>>"
```

## Example Response

```json
{
  "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
  "object": "subscription",
  "customer": "cus_Na6dX7aXxi11N4",
  "status": "active",
  "currency": "usd",
  "collection_method": "charge_automatically",
  "default_payment_method": null,
  "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
  "billing_cycle_anchor": 1679609767,
  "start_date": 1679609767,
  "cancel_at_period_end": false,
  "cancel_at": null,
  "canceled_at": null,
  "ended_at": null,
  "trial_start": null,
  "trial_end": null,
  "pause_collection": null,
  "description": null,
  "metadata": {},
  "created": 1679609767,
  "livemode": false,
  "items": {
    "object": "list",
    "data": [
      {
        "id": "si_Na6dzxczY5fwHx",
        "quantity": 1,
        "price": {
          "id": "price_1MowQULkdIwHu7ixraBm864M",
          "currency": "usd",
          "unit_amount": 1000,
          "recurring": { "interval": "month", "interval_count": 1 }
        }
      }
    ]
  }
}
```
# List Subscriptions

**GET** `/v1/subscriptions`

By default, returns subscriptions that have not been canceled. Use `status=canceled` to include canceled ones.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `customer` | string | optional | Filter by customer ID |
| `status` | enum | optional | Filter by status: `active`, `canceled`, `incomplete`, `incomplete_expired`, `past_due`, `paused`, `trialing`, `unpaid`, or `all` |
| `price` | string | optional | Filter by Price ID |
| `collection_method` | enum | optional | `charge_automatically` or `send_invoice` |
| `limit` | integer | optional | Number of results (1–100, default 10) |
| `starting_after` | string | optional | Subscription ID cursor — fetch next page after this ID |
| `ending_before` | string | optional | Subscription ID cursor — fetch previous page before this ID |
| `created.gt` | integer | optional | Created after this Unix timestamp (exclusive) |
| `created.gte` | integer | optional | Created at or after this Unix timestamp (inclusive) |
| `created.lt` | integer | optional | Created before this Unix timestamp (exclusive) |
| `created.lte` | integer | optional | Created at or before this Unix timestamp (inclusive) |

## Returns

A dictionary with a `data` array of Subscription objects. Includes `has_more` for pagination.

## Example Request

```curl
curl -G https://api.stripe.com/v1/subscriptions \
  -u "<<YOUR_SECRET_KEY>>" \
  -d limit=3
```

## Example Response

```json
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
      "collection_method": "charge_automatically",
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
            "price": {
              "id": "price_1MowQULkdIwHu7ixraBm864M",
              "unit_amount": 1000,
              "currency": "usd",
              "recurring": { "interval": "month", "interval_count": 1 }
            }
          }
        ]
      }
    }
  ]
}
```
# Cancel a Subscription

**DELETE** `/v1/subscriptions/:id`

Cancels a subscription immediately. The customer won't be charged again. After cancellation, the subscription can no longer be updated.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string (path) | **required** | The ID of the subscription to cancel |
| `invoice_now` | boolean | optional | If `true`, generates a final invoice for any un-invoiced usage. Default `false` |
| `prorate` | boolean | optional | If `true`, generates a proration credit for unused time. Default `false` |
| `cancellation_details.comment` | string | optional | Internal comment about the cancellation |
| `cancellation_details.feedback` | enum | optional | Customer reason: `customer_service`, `low_quality`, `missing_features`, `other`, `switched_service`, `too_complex`, `too_expensive`, or `unused` |

## Returns

Returns the canceled Subscription object with `status: "canceled"`.

## Example Request

```curl
curl -X DELETE https://api.stripe.com/v1/subscriptions/sub_1MlPf9LkdIwHu7ixB6VIYRyX \
  -u "<<YOUR_SECRET_KEY>>"
```

## Example Response

```json
{
  "id": "sub_1MlPf9LkdIwHu7ixB6VIYRyX",
  "object": "subscription",
  "customer": "cus_NWSaVkvdacCUi4",
  "status": "canceled",
  "currency": "usd",
  "canceled_at": 1678768842,
  "ended_at": 1678768842,
  "cancel_at_period_end": false,
  "cancellation_details": {
    "comment": null,
    "feedback": null,
    "reason": "cancellation_requested"
  },
  "latest_invoice": "in_1MlPf9LkdIwHu7ixEo6hdgCw",
  "metadata": {},
  "created": 1678768838,
  "livemode": false,
  "items": {
    "data": [
      {
        "id": "si_NWSaWTp80M123q",
        "quantity": 1,
        "price": {
          "id": "price_1MlPf7LkdIwHu7ixgcbP7cwE",
          "unit_amount": 1099,
          "currency": "usd",
          "recurring": { "interval": "month", "interval_count": 1 }
        }
      }
    ]
  }
}
```
# Resume a Subscription

**POST** `/v1/subscriptions/:id/resume`

Resumes a paused subscription. If no resumption invoice is generated, the subscription becomes `active` immediately. If a resumption invoice is generated, the subscription stays `paused` until it's paid.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string (path) | **required** | The ID of the subscription to resume |
| `billing_cycle_anchor` | enum | optional | `now` (default) resets billing cycle; `unchanged` keeps existing anchor |
| `proration_behavior` | enum | optional | Only applies when `billing_cycle_anchor=unchanged`. `create_prorations` (default), `none`, or `always_invoice` |

## Returns

Returns the Subscription object with updated status.

## Example Request

```curl
curl https://api.stripe.com/v1/subscriptions/sub_1MoGGtLkdIwHu7ixk5CfdiqC/resume \
  -u "<<YOUR_SECRET_KEY>>" \
  -d billing_cycle_anchor=now
```

## Example Response

```json
{
  "id": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",
  "object": "subscription",
  "customer": "cus_NZP5i1diUz55jp",
  "status": "active",
  "currency": "usd",
  "collection_method": "charge_automatically",
  "billing_cycle_anchor": 1679447726,
  "pause_collection": null,
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
        "price": {
          "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",
          "unit_amount": 1099,
          "currency": "usd",
          "recurring": { "interval": "month", "interval_count": 1 }
        }
      }
    ]
  }
}
```
