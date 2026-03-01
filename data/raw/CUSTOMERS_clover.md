# The Customer Object

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g. `cus_NffrFeUfNV2Hib`) |
| `object` | string | Always `"customer"` |
| `name` | string | Full name or business name |
| `email` | string | Customer's email address |
| `phone` | string | Customer's phone number |
| `description` | string | Arbitrary string for display/notes |
| `metadata` | object | Key-value pairs for storing extra info |
| `address` | object | Address: city, country, line1, line2, postal_code, state |
| `balance` | integer | Current balance in cents. Negative = credit, positive = amount owed |
| `currency` | string | Three-letter ISO currency code for recurring billing |
| `delinquent` | boolean | True if customer has a past-due invoice |
| `created` | timestamp | Unix timestamp of creation |
| `livemode` | boolean | True if live mode, false if test mode |
| `default_source` | string | ID of default payment source |
| `invoice_settings.default_payment_method` | string | ID of default PaymentMethod for subscriptions/invoices |

## Example

```json
{
  "id": "cus_NffrFeUfNV2Hib",
  "object": "customer",
  "name": "Jenny Rosen",
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
    "default_payment_method": null,
    "custom_fields": null,
    "footer": null,
    "rendering_options": null
  },
  "invoice_prefix": "0759376C",
  "next_invoice_sequence": 1,
  "preferred_locales": [],
  "shipping": null,
  "tax_exempt": "none",
  "test_clock": null
}
```
# Customers

A Customer object represents a customer of your business. Use it to save payment and contact information and track payments.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/customers` | Create a customer |
| POST | `/v1/customers/:id` | Update a customer |
| GET | `/v1/customers/:id` | Retrieve a customer |
| GET | `/v1/customers` | List all customers |
# Create a Customer

**POST** `/v1/customers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | optional | Full name or business name (max 256 chars) |
| `email` | string | optional | Email address (max 512 chars) |
| `phone` | string | optional | Phone number (max 20 chars) |
| `description` | string | optional | Arbitrary string for display/notes |
| `metadata` | object | optional | Key-value pairs for storing extra info |
| `address` | object | optional | Address: city, country, line1, line2, postal_code, state |
| `balance` | integer | optional | Starting balance in cents |
| `payment_method` | string | optional | ID of a PaymentMethod to attach |
| `invoice_settings.default_payment_method` | string | optional | Default PaymentMethod ID for invoices/subscriptions |

## Returns

Returns the Customer object after successful creation. Raises an error if parameters are invalid.

## Example Request

```curl
curl https://api.stripe.com/v1/customers \
  -u "<<YOUR_SECRET_KEY>>" \
  -d name="Jenny Rosen" \
  --data-urlencode email="jennyrosen@example.com"
```

## Example Response

```json
{
  "id": "cus_NffrFeUfNV2Hib",
  "object": "customer",
  "name": "Jenny Rosen",
  "email": "jennyrosen@example.com",
  "phone": null,
  "description": null,
  "metadata": {},
  "address": null,
  "balance": 0,
  "created": 1680893993,
  "livemode": false,
  "default_source": null,
  "invoice_settings": {
    "default_payment_method": null,
    "custom_fields": null,
    "footer": null,
    "rendering_options": null
  }
}
```
# Update a Customer

**POST** `/v1/customers/:id`

## Parameters

Any subset of fields can be updated. Pass an empty string to clear a field.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Full name or business name |
| `email` | string | Email address |
| `phone` | string | Phone number |
| `description` | string | Arbitrary string for display/notes |
| `metadata` | object | Key-value pairs. Set a key to empty string to unset it |
| `address` | object | Address: city, country, line1, line2, postal_code, state |
| `balance` | integer | Balance in cents. Negative = credit, positive = amount owed |
| `invoice_settings.default_payment_method` | string | Default PaymentMethod ID for invoices/subscriptions |

## Returns

Returns the updated Customer object. Raises an error if parameters are invalid.

## Example Request

```curl
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
  -u "<<YOUR_SECRET_KEY>>" \
  --data-urlencode email="alice@new.com"
```

## Example Response

```json
{
  "id": "cus_NffrFeUfNV2Hib",
  "object": "customer",
  "name": "Jenny Rosen",
  "email": "alice@new.com",
  "phone": null,
  "description": null,
  "metadata": {},
  "balance": 0,
  "created": 1680893993,
  "livemode": false
}
```
# Retrieve a Customer

**GET** `/v1/customers/:id`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string (path) | The ID of the customer to retrieve |

## Returns

Returns the Customer object for a valid identifier. If the customer was deleted, returns a subset of fields with `deleted: true`.

## Example Request

```curl
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
  -u "<<YOUR_SECRET_KEY>>"
```

## Example Response

```json
{
  "id": "cus_NffrFeUfNV2Hib",
  "object": "customer",
  "name": "Jenny Rosen",
  "email": "jennyrosen@example.com",
  "phone": null,
  "description": null,
  "metadata": {},
  "address": null,
  "balance": 0,
  "created": 1680893993,
  "livemode": false,
  "default_source": null,
  "delinquent": false,
  "invoice_settings": {
    "default_payment_method": null,
    "custom_fields": null,
    "footer": null,
    "rendering_options": null
  }
}
```
# List All Customers

**GET** `/v1/customers`

Returns a list of customers sorted by creation date, newest first.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | optional | Filter by exact email address (case-sensitive) |
| `limit` | integer | optional | Number of results to return (1–100, default 10) |
| `starting_after` | string | optional | Customer ID cursor — fetch the next page after this ID |
| `ending_before` | string | optional | Customer ID cursor — fetch the previous page before this ID |
| `created.gt` | integer | optional | Return customers created after this Unix timestamp (exclusive) |
| `created.gte` | integer | optional | Return customers created at or after this Unix timestamp (inclusive) |
| `created.lt` | integer | optional | Return customers created before this Unix timestamp (exclusive) |
| `created.lte` | integer | optional | Return customers created at or before this Unix timestamp (inclusive) |

## Returns

A dictionary with a `data` array of Customer objects. Includes `has_more` to indicate if another page exists.

## Example Request

```curl
curl -G https://api.stripe.com/v1/customers \
  -u "<<YOUR_SECRET_KEY>>" \
  -d limit=3
```

## Example Response

```json
{
  "object": "list",
  "url": "/v1/customers",
  "has_more": false,
  "data": [
    {
      "id": "cus_NffrFeUfNV2Hib",
      "object": "customer",
      "name": "Jenny Rosen",
      "email": "jennyrosen@example.com",
      "phone": null,
      "balance": 0,
      "created": 1680893993,
      "livemode": false,
      "metadata": {}
    }
  ]
}
```
