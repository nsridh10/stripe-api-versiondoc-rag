# The Account Object

A Stripe Account represents a connected account on your platform via Stripe Connect.

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g. `acct_1Nv0FGQ9RKHgCVdK`) |
| `object` | string | Always `"account"` |
| `email` | string | Account's email address |
| `country` | string | Two-letter ISO country code |
| `default_currency` | string | Three-letter ISO currency code |
| `type` | enum | Account type: `standard`, `express`, `custom`, or `none` |
| `business_type` | enum | `individual`, `company`, `non_profit`, or `government_entity` |
| `charges_enabled` | boolean | Whether the account can process charges |
| `payouts_enabled` | boolean | Whether the account can receive payouts |
| `details_submitted` | boolean | Whether required onboarding details have been submitted |
| `created` | timestamp | Unix timestamp of creation |
| `metadata` | object | Key-value pairs for storing extra info |
| `capabilities` | object | Hash of capability names to their status: `active`, `inactive`, or `pending` |
| `requirements.currently_due` | array | Fields that must be collected to keep the account enabled |
| `requirements.disabled_reason` | string | Reason the account is disabled, if applicable |
| `controller.type` | enum | Who controls the account: `application` or `account` |
| `controller.requirement_collection` | enum | Who collects requirements: `stripe` or `application` |
| `controller.stripe_dashboard.type` | enum | Dashboard access type: `express`, `full`, or `none` |

## Example Object

```json
{
  "id": "acct_1Nv0FGQ9RKHgCVdK",
  "object": "account",
  "email": "jenny.rosen@example.com",
  "country": "US",
  "default_currency": "usd",
  "type": "none",
  "business_type": null,
  "charges_enabled": false,
  "payouts_enabled": false,
  "details_submitted": false,
  "created": 1695830751,
  "metadata": {},
  "capabilities": {},
  "requirements": {
    "currently_due": ["business_profile.mcc", "business_profile.url", "business_type", "external_account"],
    "disabled_reason": "requirements.past_due",
    "errors": [],
    "eventually_due": [],
    "past_due": [],
    "pending_verification": []
  },
  "controller": {
    "type": "application",
    "is_controller": true,
    "requirement_collection": "stripe",
    "stripe_dashboard": { "type": "express" },
    "fees": { "payer": "application" },
    "losses": { "payments": "application" }
  }
}
```
# Accounts (Connect)

An Account represents a Stripe connected account on your platform. Use Stripe Connect to create and manage accounts for your users.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/accounts` | Create a connected account |
| GET | `/v1/accounts/:id` | Retrieve an account |
| GET | `/v1/accounts` | List all connected accounts |
# Create an Account

**POST** `/v1/accounts`

Creates a new connected account for a user on your platform via Stripe Connect.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | enum | optional | Account type: `standard`, `express`, or `custom` |
| `country` | string | optional | Two-letter ISO country code (defaults to platform country) |
| `email` | string | optional | Account's email address |
| `capabilities` | object | conditionally required | Required for Custom accounts (`controller.stripe_dashboard.type = none`). Each key is a capability name with `requested: true` to enable it |
| `business_type` | enum | optional | `individual`, `company`, `non_profit`, or `government_entity` |
| `business_profile.name` | string | optional | Customer-facing business name |
| `business_profile.url` | string | optional | Business's publicly available website |
| `business_profile.support_email` | string | optional | Public support email |
| `business_profile.support_phone` | string | optional | Public support phone |
| `business_profile.mcc` | string | optional | Merchant category code (4 chars) |
| `metadata` | object | optional | Key-value pairs for storing extra info |
| `controller.fees.payer` | enum | optional | Who pays Stripe fees: `application` or `account` |
| `controller.losses.payments` | enum | optional | Who bears payment losses: `application` or `stripe` |
| `controller.stripe_dashboard.type` | enum | optional | Dashboard access: `express`, `full`, or `none` |
| `tos_acceptance.date` | timestamp | optional | Unix timestamp when account rep accepted ToS |
| `tos_acceptance.ip` | string | optional | IP address from which ToS was accepted |

## Returns

Returns an Account object if the call succeeds.

## Example Request

```curl
curl https://api.stripe.com/v1/accounts \
  -u "<<YOUR_SECRET_KEY>>" \
  -d country=US \
  --data-urlencode email="jenny.rosen@example.com" \
  -d "controller[fees][payer]"=application \
  -d "controller[losses][payments]"=application \
  -d "controller[stripe_dashboard][type]"=express
```

## Example Response

```json
{
  "id": "acct_1Nv0FGQ9RKHgCVdK",
  "object": "account",
  "email": "jenny.rosen@example.com",
  "country": "US",
  "default_currency": "usd",
  "type": "none",
  "charges_enabled": false,
  "payouts_enabled": false,
  "details_submitted": false,
  "created": 1695830751,
  "metadata": {},
  "capabilities": {},
  "controller": {
    "type": "application",
    "requirement_collection": "stripe",
    "stripe_dashboard": { "type": "express" },
    "fees": { "payer": "application" },
    "losses": { "payments": "application" }
  },
  "requirements": {
    "currently_due": ["business_profile.mcc", "business_profile.url", "business_type", "external_account"],
    "disabled_reason": "requirements.past_due"
  }
}
```
# Retrieve an Account

**GET** `/v1/accounts/:id`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string (path) | The ID of the account to retrieve |

## Returns

Returns an Account object if the call succeeds. Raises an error if the account ID does not exist.

## Example Request

```curl
curl https://api.stripe.com/v1/accounts/acct_1Nv0FGQ9RKHgCVdK \
  -u "<<YOUR_SECRET_KEY>>"
```

## Example Response

```json
{
  "id": "acct_1Nv0FGQ9RKHgCVdK",
  "object": "account",
  "email": "jenny.rosen@example.com",
  "country": "US",
  "default_currency": "usd",
  "type": "none",
  "charges_enabled": false,
  "payouts_enabled": false,
  "details_submitted": false,
  "created": 1695830751,
  "metadata": {},
  "capabilities": {},
  "controller": {
    "type": "application",
    "requirement_collection": "stripe",
    "stripe_dashboard": { "type": "express" },
    "fees": { "payer": "application" },
    "losses": { "payments": "application" }
  },
  "requirements": {
    "currently_due": ["business_profile.mcc", "business_profile.url", "business_type", "external_account"],
    "disabled_reason": "requirements.past_due",
    "errors": [],
    "past_due": [],
    "pending_verification": []
  }
}
```
# List All Connected Accounts

**GET** `/v1/accounts`

Returns a list of accounts connected to your platform via Connect. If you're not a platform, the list is empty.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | optional | Number of results to return (1–100, default 10) |
| `starting_after` | string | optional | Account ID cursor — fetch the next page after this ID |
| `ending_before` | string | optional | Account ID cursor — fetch the previous page before this ID |
| `created.gt` | integer | optional | Return accounts created after this Unix timestamp (exclusive) |
| `created.gte` | integer | optional | Return accounts created at or after this Unix timestamp (inclusive) |
| `created.lt` | integer | optional | Return accounts created before this Unix timestamp (exclusive) |
| `created.lte` | integer | optional | Return accounts created at or before this Unix timestamp (inclusive) |

## Returns

A dictionary with a `data` array of Account objects. Includes `has_more` for pagination.

## Example Request

```curl
curl -G https://api.stripe.com/v1/accounts \
  -u "<<YOUR_SECRET_KEY>>" \
  -d limit=3
```

## Example Response

```json
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
      "type": "none",
      "charges_enabled": false,
      "payouts_enabled": false,
      "details_submitted": false,
      "created": 1695830751,
      "metadata": {},
      "capabilities": {},
      "requirements": {
        "currently_due": ["business_profile.mcc", "business_type", "external_account"],
        "disabled_reason": "requirements.past_due"
      }
    }
  ]
}
```
