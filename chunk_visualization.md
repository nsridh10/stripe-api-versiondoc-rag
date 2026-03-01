# ChromaDB Chunk Dump
**Total Chunks:** 314

---

### Chunk 1 | ID: `651911f0-acfa-4b54-bcce-09d0384f6bf1`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "version": "v1",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> Accounts
> 
> An Account represents a Stripe connected account on your platform. Use Stripe Connect to create and manage accounts for your users.

---

### Chunk 2 | ID: `160cf493-1ac5-45fb-886c-92597fa2fda7`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Endpoints",
  "api_class": "ACCOUNTS",
  "Header 1": "Accounts"
}
```

**Content:**
> Endpoints
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 15 40 45
> 
>    * - Method
>      - Endpoint
>      - Description
>    * - POST
>      - ``/v1/accounts``
>      - Create a connected account
>    * - GET
>      - ``/v1/accounts/:id``
>      - Retrieve an account
>    * - GET
>      - ``/v1/accounts``
>      - List all connected accounts

---

### Chunk 3 | ID: `cbffa4af-bbc0-4e5d-9485-000b6eaec1f6`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "api_class": "ACCOUNTS",
  "Header 2": "The Account Object",
  "version": "v1"
}
```

**Content:**
> The Account Object

---

### Chunk 4 | ID: `9b05fc67-a2ac-4af8-82de-b0a6e7f4ebe9`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 2": "The Account Object",
  "Header 1": "Accounts",
  "version": "v1",
  "Header 3": "Key Fields"
}
```

**Content:**
> Key Fields
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 30 20 50

---

### Chunk 5 | ID: `8ef367d9-5a9c-48a5-9bd0-5d9fc5008add`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "Header 2": "The Account Object",
  "version": "v1",
  "api_class": "ACCOUNTS",
  "Header 3": "Key Fields"
}
```

**Content:**
> * - Field
>      - Type
>      - Description
>    * - ``id``
>      - string
>      - Unique identifier (e.g. ``acct_1Nv0FGQ9RKHgCVdK``)
>    * - ``object``
>      - string
>      - Always ``"account"``
>    * - ``email``
>      - string
>      - Account's email address
>    * - ``country``
>      - string
>      - Two-letter ISO country code
>    * - ``default_currency``
>      - string
>      - Three-letter ISO currency code
>    * - ``type``
>      - enum
>      - Account type: ``standard``, ``express``, or ``custom``
>    * - ``business_name``
>      - string
>      - The business's display name
>    * - ``business_url``
>      - string
>      - The business's publicly available website
>    * - ``charges_enabled``
>      - boolean
>      - Whether the account can process charges
>    * - ``payouts_enabled``
>      - boolean
>      - Whether the account can receive payouts
>    * - ``details_submitted``
>      - boolean
>      - Whether required onboarding details have been submitted
>    * - ``created``
>      - timestamp

---

### Chunk 6 | ID: `a6b3174f-c389-4bd1-b05c-a3e448651c94`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 3": "Key Fields",
  "Header 1": "Accounts",
  "Header 2": "The Account Object",
  "version": "v1"
}
```

**Content:**
> - Whether required onboarding details have been submitted
>    * - ``created``
>      - timestamp
>      - Unix timestamp of creation
>    * - ``metadata``
>      - object
>      - Key-value pairs for storing extra info
>    * - ``verification.disabled_reason``
>      - string
>      - Reason the account is disabled, if applicable
>    * - ``verification.fields_needed``
>      - array
>      - Fields that must be collected to keep the account enabled

---

### Chunk 7 | ID: `acfebfb7-6f8b-47ab-9364-f0c73c5e8f47`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Accounts",
  "Header 3": "Example Object",
  "api_class": "ACCOUNTS",
  "Header 2": "The Account Object"
}
```

**Content:**
> Example Object
> 
> .. code-block:: json
> 
>    {
>      "id": "acct_1Nv0FGQ9RKHgCVdK",
>      "object": "account",
>      "email": "jenny.rosen@example.com",
>      "country": "US",
>      "default_currency": "usd",
>      "type": "express",
>      "business_name": null,
>      "business_url": null,
>      "charges_enabled": false,
>      "payouts_enabled": false,
>      "details_submitted": false,
>      "created": 1695830751,
>      "metadata": {},
>      "verification": {
>        "disabled_reason": "fields_needed",
>        "fields_needed": ["business_url", "external_account", "tos_acceptance.date"]
>      }
>    }

---

### Chunk 8 | ID: `bf0fdd33-45e0-4cff-93b7-556c74c655f2`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 1": "Accounts",
  "Header 2": "Create an Account",
  "version": "v1"
}
```

**Content:**
> Create an Account
> 
> **POST** ``/v1/accounts``

---

### Chunk 9 | ID: `0824e358-c38d-4683-bc54-7e11af5c33b5`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "Header 1": "Accounts",
  "api_class": "ACCOUNTS",
  "Header 2": "Create an Account",
  "version": "v1"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 15 30

---

### Chunk 10 | ID: `180f888c-ef4d-4089-a957-4d9d344837c9`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "Header 3": "Parameters",
  "version": "v1",
  "api_class": "ACCOUNTS",
  "Header 2": "Create an Account"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``type``
>      - enum
>      - optional
>      - Account type: ``standard``, ``express``, or ``custom``
>    * - ``country``
>      - string
>      - optional
>      - Two-letter ISO country code (defaults to platform country)
>    * - ``email``
>      - string
>      - optional
>      - Account's email address
>    * - ``business_name``
>      - string
>      - optional
>      - The business's display name
>    * - ``business_url``
>      - string
>      - optional
>      - The business's publicly available website
>    * - ``support_email``
>      - string
>      - optional
>      - Public support email
>    * - ``support_phone``
>      - string
>      - optional
>      - Public support phone
>    * - ``metadata``
>      - object
>      - optional
>      - Key-value pairs for storing extra info
>    * - ``tos_acceptance.date``
>      - timestamp
>      - optional
>      - Unix timestamp when account rep accepted ToS
>    * - ``tos_acceptance.ip``
>      - string
>      - optional

---

### Chunk 11 | ID: `ea4dd8b3-95f8-42e1-a96e-cdc0cd53e41d`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "Header 2": "Create an Account",
  "version": "v1",
  "Header 1": "Accounts",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> * - ``tos_acceptance.ip``
>      - string
>      - optional
>      - IP address from which ToS was accepted

---

### Chunk 12 | ID: `410a6bd9-fcf9-49ea-ba5b-788b82b72778`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Accounts",
  "Header 3": "Returns",
  "Header 2": "Create an Account",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> Returns
> 
> Returns an Account object if the call succeeds.

---

### Chunk 13 | ID: `e9a0e4b2-e4c2-4fba-b04e-cb7b53070827`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "version": "v1",
  "Header 1": "Accounts",
  "Header 3": "Example Request",
  "Header 2": "Create an Account"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/accounts \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d type=express \
>      -d country=US \
>      --data-urlencode email="jenny.rosen@example.com"

---

### Chunk 14 | ID: `e3955f6e-0ed3-452b-8750-96b142fe44bc`

**Metadata:**
```json
{
  "version": "v1",
  "Header 3": "Example Response",
  "api_class": "ACCOUNTS",
  "Header 2": "Create an Account",
  "Header 1": "Accounts"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "acct_1Nv0FGQ9RKHgCVdK",
>      "object": "account",
>      "email": "jenny.rosen@example.com",
>      "country": "US",
>      "default_currency": "usd",
>      "type": "express",
>      "charges_enabled": false,
>      "payouts_enabled": false,
>      "details_submitted": false,
>      "created": 1695830751,
>      "metadata": {},
>      "verification": {
>        "disabled_reason": "fields_needed",
>        "fields_needed": ["business_url", "external_account"]
>      }
>    }

---

### Chunk 15 | ID: `052e8c42-4157-4860-a8ab-320f181bc7a5`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 1": "Accounts",
  "version": "v1",
  "Header 2": "Retrieve an Account"
}
```

**Content:**
> Retrieve an Account
> 
> **GET** ``/v1/accounts/:id``

---

### Chunk 16 | ID: `a638b347-d02c-4e00-9b82-1a7277bd71eb`

**Metadata:**
```json
{
  "version": "v1",
  "Header 3": "Parameters",
  "api_class": "ACCOUNTS",
  "Header 1": "Accounts",
  "Header 2": "Retrieve an Account"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 20 20 60
> 
>    * - Parameter
>      - Type
>      - Description
>    * - ``id``
>      - string (path)
>      - The ID of the account to retrieve

---

### Chunk 17 | ID: `54336052-1b75-4620-8577-baedc26559c6`

**Metadata:**
```json
{
  "Header 3": "Returns",
  "api_class": "ACCOUNTS",
  "Header 2": "Retrieve an Account",
  "version": "v1",
  "Header 1": "Accounts"
}
```

**Content:**
> Returns
> 
> Returns an Account object if the call succeeds. Raises an error if the account ID does not exist.

---

### Chunk 18 | ID: `5f86e93f-4fec-493e-bd24-0346b189d39b`

**Metadata:**
```json
{
  "Header 2": "Retrieve an Account",
  "Header 3": "Example Request",
  "Header 1": "Accounts",
  "api_class": "ACCOUNTS",
  "version": "v1"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/accounts/acct_1Nv0FGQ9RKHgCVdK \
>      -u "<<YOUR_SECRET_KEY>>"

---

### Chunk 19 | ID: `671fe1e1-538f-4567-81e4-567ce46f3e02`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "Header 2": "Retrieve an Account",
  "version": "v1",
  "api_class": "ACCOUNTS",
  "Header 3": "Example Response"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "acct_1Nv0FGQ9RKHgCVdK",
>      "object": "account",
>      "email": "jenny.rosen@example.com",
>      "country": "US",
>      "default_currency": "usd",
>      "type": "express",
>      "charges_enabled": false,
>      "payouts_enabled": false,
>      "details_submitted": false,
>      "created": 1695830751,
>      "metadata": {},
>      "verification": {
>        "disabled_reason": "fields_needed",
>        "fields_needed": ["business_url", "external_account", "tos_acceptance.date"]
>      }
>    }

---

### Chunk 20 | ID: `ddf37ee5-99c0-45d8-939f-c2d41c0a8c2f`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "version": "v1",
  "Header 2": "List All Connected Accounts",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> List All Connected Accounts
> 
> **GET** ``/v1/accounts``
> 
> Returns a list of accounts connected to your platform via Connect. If you're not a platform, the list is empty.

---

### Chunk 21 | ID: `3eec33d0-e906-44ec-a7a4-e1765636aac3`

**Metadata:**
```json
{
  "Header 2": "List All Connected Accounts",
  "Header 3": "Parameters",
  "Header 1": "Accounts",
  "version": "v1",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 25 20 15 40
> 
>    * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``limit``
>      - integer
>      - optional
>      - Number of results to return (1–100, default 10)
>    * - ``starting_after``
>      - string
>      - optional
>      - Account ID cursor — fetch the next page after this ID
>    * - ``ending_before``
>      - string
>      - optional
>      - Account ID cursor — fetch the previous page before this ID
>    * - ``created.gt``
>      - integer
>      - optional
>      - Return accounts created after this Unix timestamp (exclusive)
>    * - ``created.gte``
>      - integer
>      - optional
>      - Return accounts created at or after this Unix timestamp (inclusive)
>    * - ``created.lt``
>      - integer
>      - optional
>      - Return accounts created before this Unix timestamp (exclusive)
>    * - ``created.lte``
>      - integer
>      - optional
>      - Return accounts created at or before this Unix timestamp (inclusive)

---

### Chunk 22 | ID: `fc0f48fd-5ba5-48e8-bf47-ffbb5788b2b9`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Accounts",
  "Header 3": "Returns",
  "api_class": "ACCOUNTS",
  "Header 2": "List All Connected Accounts"
}
```

**Content:**
> Returns
> 
> A dictionary with a ``data`` array of Account objects. Includes ``has_more`` for pagination.

---

### Chunk 23 | ID: `ee4ef109-5cf8-48ed-83bb-58331497edf1`

**Metadata:**
```json
{
  "Header 2": "List All Connected Accounts",
  "version": "v1",
  "Header 3": "Example Request",
  "api_class": "ACCOUNTS",
  "Header 1": "Accounts"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl -G https://api.stripe.com/v1/accounts \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d limit=3

---

### Chunk 24 | ID: `80467794-dd89-44a9-b409-d791cc6295a9`

**Metadata:**
```json
{
  "Header 1": "Accounts",
  "Header 2": "List All Connected Accounts",
  "api_class": "ACCOUNTS",
  "version": "v1",
  "Header 3": "Example Response"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "object": "list",
>      "url": "/v1/accounts",
>      "has_more": false,
>      "data": [
>        {
>          "id": "acct_1Nv0FGQ9RKHgCVdK",
>          "object": "account",
>          "email": "jenny.rosen@example.com",
>          "country": "US",
>          "default_currency": "usd",
>          "type": "express",
>          "charges_enabled": false,
>          "payouts_enabled": false,
>          "details_submitted": false,
>          "created": 1695830751,
>          "metadata": {},
>          "verification": {
>            "disabled_reason": "fields_needed",
>            "fields_needed": ["business_url", "external_account"]
>          }
>        }
>      ]
>    }

---

### Chunk 25 | ID: `d292ff2a-c8d9-4e1e-be13-afb30e723b3e`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 1": "The Account Object",
  "version": "v2"
}
```

**Content:**
> A Stripe Account represents a connected account on your platform via Stripe Connect.

---

### Chunk 26 | ID: `b6dbdd45-37e3-4d3e-9377-e7bc0425ae14`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 1": "The Account Object",
  "version": "v2",
  "Header 2": "Key Fields"
}
```

**Content:**
> | Field | Type | Description |
> |-------|------|-------------|
> | `id` | string | Unique identifier (e.g. `acct_1Nv0FGQ9RKHgCVdK`) |
> | `object` | string | Always `"account"` |
> | `email` | string | Account's email address |
> | `country` | string | Two-letter ISO country code |
> | `default_currency` | string | Three-letter ISO currency code |
> | `type` | enum | Account type: `standard`, `express`, `custom`, or `none` |
> | `business_type` | enum | `individual`, `company`, `non_profit`, or `government_entity` |
> | `charges_enabled` | boolean | Whether the account can process charges |
> | `payouts_enabled` | boolean | Whether the account can receive payouts |
> | `details_submitted` | boolean | Whether required onboarding details have been submitted |
> | `created` | timestamp | Unix timestamp of creation |
> | `metadata` | object | Key-value pairs for storing extra info |
> | `capabilities` | object | Hash of capability names to their status: `active`, `inactive`, or `pending` |

---

### Chunk 27 | ID: `bd6c0855-3f7a-4105-b7c5-a074a2bc498b`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 2": "Key Fields",
  "Header 1": "The Account Object",
  "version": "v2"
}
```

**Content:**
> | `requirements.currently_due` | array | Fields that must be collected to keep the account enabled |
> | `requirements.disabled_reason` | string | Reason the account is disabled, if applicable |
> | `controller.type` | enum | Who controls the account: `application` or `account` |
> | `controller.requirement_collection` | enum | Who collects requirements: `stripe` or `application` |
> | `controller.stripe_dashboard.type` | enum | Dashboard access type: `express`, `full`, or `none` |

---

### Chunk 28 | ID: `409f23ab-4f9e-4825-9502-3799a23d0231`

**Metadata:**
```json
{
  "Header 2": "Example Object",
  "version": "v2",
  "api_class": "ACCOUNTS",
  "Header 1": "The Account Object"
}
```

**Content:**
> ```json
> {
> "id": "acct_1Nv0FGQ9RKHgCVdK",
> "object": "account",
> "email": "jenny.rosen@example.com",
> "country": "US",
> "default_currency": "usd",
> "type": "none",
> "business_type": null,
> "charges_enabled": false,
> "payouts_enabled": false,
> "details_submitted": false,
> "created": 1695830751,
> "metadata": {},
> "capabilities": {},
> "requirements": {
> "currently_due": ["business_profile.mcc", "business_profile.url", "business_type", "external_account"],
> "disabled_reason": "requirements.past_due",
> "errors": [],
> "eventually_due": [],
> "past_due": [],
> "pending_verification": []
> },
> "controller": {
> "type": "application",
> "is_controller": true,
> "requirement_collection": "stripe",
> "stripe_dashboard": { "type": "express" },
> "fees": { "payer": "application" },
> "losses": { "payments": "application" }
> }
> }
> ```

---

### Chunk 29 | ID: `2340e734-7473-4454-a80d-2c4e010b9f2d`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "version": "v2",
  "Header 1": "Accounts (Connect)"
}
```

**Content:**
> An Account represents a Stripe connected account on your platform. Use Stripe Connect to create and manage accounts for your users.

---

### Chunk 30 | ID: `d3a8656a-c10c-4ade-849a-58594fd793e2`

**Metadata:**
```json
{
  "Header 2": "Endpoints",
  "version": "v2",
  "Header 1": "Accounts (Connect)",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> | Method | Endpoint | Description |
> |--------|----------|-------------|
> | POST | `/v1/accounts` | Create a connected account |
> | GET | `/v1/accounts/:id` | Retrieve an account |
> | GET | `/v1/accounts` | List all connected accounts |

---

### Chunk 31 | ID: `8409fd6d-e3be-42ac-815b-66d9d5e5d33e`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Create an Account",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> **POST** `/v1/accounts`  
> Creates a new connected account for a user on your platform via Stripe Connect.

---

### Chunk 32 | ID: `0120447f-e92a-436b-8b4a-0369559ae4c9`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 1": "Create an Account",
  "Header 2": "Parameters",
  "version": "v2"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `type` | enum | optional | Account type: `standard`, `express`, or `custom` |
> | `country` | string | optional | Two-letter ISO country code (defaults to platform country) |
> | `email` | string | optional | Account's email address |
> | `capabilities` | object | conditionally required | Required for Custom accounts (`controller.stripe_dashboard.type = none`). Each key is a capability name with `requested: true` to enable it |
> | `business_type` | enum | optional | `individual`, `company`, `non_profit`, or `government_entity` |
> | `business_profile.name` | string | optional | Customer-facing business name |
> | `business_profile.url` | string | optional | Business's publicly available website |
> | `business_profile.support_email` | string | optional | Public support email |
> | `business_profile.support_phone` | string | optional | Public support phone |

---

### Chunk 33 | ID: `ea7b4b04-cfd6-4aeb-8c54-5b5442bbdbaa`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Parameters",
  "Header 1": "Create an Account",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> | `business_profile.support_phone` | string | optional | Public support phone |
> | `business_profile.mcc` | string | optional | Merchant category code (4 chars) |
> | `metadata` | object | optional | Key-value pairs for storing extra info |
> | `controller.fees.payer` | enum | optional | Who pays Stripe fees: `application` or `account` |
> | `controller.losses.payments` | enum | optional | Who bears payment losses: `application` or `stripe` |
> | `controller.stripe_dashboard.type` | enum | optional | Dashboard access: `express`, `full`, or `none` |
> | `tos_acceptance.date` | timestamp | optional | Unix timestamp when account rep accepted ToS |
> | `tos_acceptance.ip` | string | optional | IP address from which ToS was accepted |

---

### Chunk 34 | ID: `a9544ee7-4f6e-45f1-8250-62b899b023fc`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "ACCOUNTS",
  "Header 1": "Create an Account",
  "Header 2": "Returns"
}
```

**Content:**
> Returns an Account object if the call succeeds.

---

### Chunk 35 | ID: `f171f7a8-082a-478b-b982-56dee21e5104`

**Metadata:**
```json
{
  "Header 2": "Example Request",
  "version": "v2",
  "api_class": "ACCOUNTS",
  "Header 1": "Create an Account"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/accounts \
> -u "<<YOUR_SECRET_KEY>>" \
> -d country=US \
> --data-urlencode email="jenny.rosen@example.com" \
> -d "controller[fees][payer]"=application \
> -d "controller[losses][payments]"=application \
> -d "controller[stripe_dashboard][type]"=express
> ```

---

### Chunk 36 | ID: `44ec5f80-ff13-41cc-81f3-5b9ded492964`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "version": "v2",
  "Header 1": "Create an Account",
  "Header 2": "Example Response"
}
```

**Content:**
> ```json
> {
> "id": "acct_1Nv0FGQ9RKHgCVdK",
> "object": "account",
> "email": "jenny.rosen@example.com",
> "country": "US",
> "default_currency": "usd",
> "type": "none",
> "charges_enabled": false,
> "payouts_enabled": false,
> "details_submitted": false,
> "created": 1695830751,
> "metadata": {},
> "capabilities": {},
> "controller": {
> "type": "application",
> "requirement_collection": "stripe",
> "stripe_dashboard": { "type": "express" },
> "fees": { "payer": "application" },
> "losses": { "payments": "application" }
> },
> "requirements": {
> "currently_due": ["business_profile.mcc", "business_profile.url", "business_type", "external_account"],
> "disabled_reason": "requirements.past_due"
> }
> }
> ```

---

### Chunk 37 | ID: `3ff11e7e-03bd-41bc-80b0-f1e7b0656ac9`

**Metadata:**
```json
{
  "api_class": "ACCOUNTS",
  "Header 1": "Retrieve an Account",
  "version": "v2"
}
```

**Content:**
> **GET** `/v1/accounts/:id`

---

### Chunk 38 | ID: `82fd4420-4129-4f56-b2a6-c14e5b66be1d`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "ACCOUNTS",
  "Header 2": "Parameters",
  "Header 1": "Retrieve an Account"
}
```

**Content:**
> | Parameter | Type | Description |
> |-----------|------|-------------|
> | `id` | string (path) | The ID of the account to retrieve |

---

### Chunk 39 | ID: `3689abc9-1c69-4386-aa9a-553522d765f5`

**Metadata:**
```json
{
  "Header 1": "Retrieve an Account",
  "api_class": "ACCOUNTS",
  "version": "v2",
  "Header 2": "Returns"
}
```

**Content:**
> Returns an Account object if the call succeeds. Raises an error if the account ID does not exist.

---

### Chunk 40 | ID: `6139a916-a1a5-4b9a-b03b-40eb4df4e22b`

**Metadata:**
```json
{
  "Header 2": "Example Request",
  "Header 1": "Retrieve an Account",
  "version": "v2",
  "api_class": "ACCOUNTS"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/accounts/acct_1Nv0FGQ9RKHgCVdK \
> -u "<<YOUR_SECRET_KEY>>"
> ```

---

### Chunk 41 | ID: `e920a667-5858-46fd-ad0a-574e25e7ab13`

**Metadata:**
```json
{
  "Header 1": "Retrieve an Account",
  "version": "v2",
  "api_class": "ACCOUNTS",
  "Header 2": "Example Response"
}
```

**Content:**
> ```json
> {
> "id": "acct_1Nv0FGQ9RKHgCVdK",
> "object": "account",
> "email": "jenny.rosen@example.com",
> "country": "US",
> "default_currency": "usd",
> "type": "none",
> "charges_enabled": false,
> "payouts_enabled": false,
> "details_submitted": false,
> "created": 1695830751,
> "metadata": {},
> "capabilities": {},
> "controller": {
> "type": "application",
> "requirement_collection": "stripe",
> "stripe_dashboard": { "type": "express" },
> "fees": { "payer": "application" },
> "losses": { "payments": "application" }
> },
> "requirements": {
> "currently_due": ["business_profile.mcc", "business_profile.url", "business_type", "external_account"],
> "disabled_reason": "requirements.past_due",
> "errors": [],
> "past_due": [],
> "pending_verification": []
> }
> }
> ```

---

### Chunk 42 | ID: `af759e84-4217-4f60-8518-61cad279249a`

**Metadata:**
```json
{
  "Header 1": "List All Connected Accounts",
  "api_class": "ACCOUNTS",
  "version": "v2"
}
```

**Content:**
> **GET** `/v1/accounts`  
> Returns a list of accounts connected to your platform via Connect. If you're not a platform, the list is empty.

---

### Chunk 43 | ID: `0fac04e9-9159-44f8-acbb-d626d45d3f0f`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Parameters",
  "api_class": "ACCOUNTS",
  "Header 1": "List All Connected Accounts"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `limit` | integer | optional | Number of results to return (1–100, default 10) |
> | `starting_after` | string | optional | Account ID cursor — fetch the next page after this ID |
> | `ending_before` | string | optional | Account ID cursor — fetch the previous page before this ID |
> | `created.gt` | integer | optional | Return accounts created after this Unix timestamp (exclusive) |
> | `created.gte` | integer | optional | Return accounts created at or after this Unix timestamp (inclusive) |
> | `created.lt` | integer | optional | Return accounts created before this Unix timestamp (exclusive) |
> | `created.lte` | integer | optional | Return accounts created at or before this Unix timestamp (inclusive) |

---

### Chunk 44 | ID: `14d423c2-d43e-4e94-97a6-e25ae1d2356b`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "ACCOUNTS",
  "Header 1": "List All Connected Accounts",
  "Header 2": "Returns"
}
```

**Content:**
> A dictionary with a `data` array of Account objects. Includes `has_more` for pagination.

---

### Chunk 45 | ID: `d0e8cd70-6fce-4b35-bd5e-cfbe2856b6cc`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Example Request",
  "api_class": "ACCOUNTS",
  "Header 1": "List All Connected Accounts"
}
```

**Content:**
> ```curl
> curl -G https://api.stripe.com/v1/accounts \
> -u "<<YOUR_SECRET_KEY>>" \
> -d limit=3
> ```

---

### Chunk 46 | ID: `01536e1e-ec94-400e-9997-f7479778821d`

**Metadata:**
```json
{
  "Header 1": "List All Connected Accounts",
  "Header 2": "Example Response",
  "api_class": "ACCOUNTS",
  "version": "v2"
}
```

**Content:**
> ```json
> {
> "object": "list",
> "url": "/v1/accounts",
> "has_more": false,
> "data": [
> {
> "id": "acct_1Nv0FGQ9RKHgCVdK",
> "object": "account",
> "email": "jenny.rosen@example.com",
> "country": "US",
> "default_currency": "usd",
> "type": "none",
> "charges_enabled": false,
> "payouts_enabled": false,
> "details_submitted": false,
> "created": 1695830751,
> "metadata": {},
> "capabilities": {},
> "requirements": {
> "currently_due": ["business_profile.mcc", "business_type", "external_account"],
> "disabled_reason": "requirements.past_due"
> }
> }
> ]
> }
> ```

---

### Chunk 47 | ID: `2aa2a060-8f59-4fce-be45-091f61928369`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 1": "Customers",
  "version": "v1"
}
```

**Content:**
> Customers
> 
> A Customer object represents a customer of your business. Use it to save payment and contact information and track payments.

---

### Chunk 48 | ID: `b2248f75-bda8-4853-8ebb-199bc59a1213`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "version": "v1",
  "Header 1": "Customers",
  "Header 2": "Endpoints"
}
```

**Content:**
> Endpoints
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 15 40 45
> 
>    * - Method
>      - Endpoint
>      - Description
>    * - POST
>      - ``/v1/customers``
>      - Create a customer
>    * - POST
>      - ``/v1/customers/:id``
>      - Update a customer
>    * - GET
>      - ``/v1/customers/:id``
>      - Retrieve a customer
>    * - GET
>      - ``/v1/customers``
>      - List all customers

---

### Chunk 49 | ID: `b16d93a9-b07c-416d-8387-b300c29d7eb0`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "version": "v1",
  "Header 2": "The Customer Object",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> The Customer Object

---

### Chunk 50 | ID: `3f895e92-14ef-41ed-9f5a-4deeb4cf8a26`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "Header 3": "Key Fields",
  "Header 2": "The Customer Object",
  "api_class": "CUSTOMERS",
  "version": "v1"
}
```

**Content:**
> Key Fields
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 30 20 50

---

### Chunk 51 | ID: `338fd568-16a1-4d1a-960b-8467da233b53`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 3": "Key Fields",
  "Header 2": "The Customer Object",
  "Header 1": "Customers",
  "version": "v1"
}
```

**Content:**
> * - Field
>      - Type
>      - Description
>    * - ``id``
>      - string
>      - Unique identifier (e.g. ``cus_NffrFeUfNV2Hib``)
>    * - ``object``
>      - string
>      - Always ``"customer"``
>    * - ``full_name``
>      - string
>      - Customer's full name or business name
>    * - ``email``
>      - string
>      - Customer's email address
>    * - ``phone``
>      - string
>      - Customer's phone number
>    * - ``description``
>      - string
>      - Arbitrary string for display/notes
>    * - ``metadata``
>      - object
>      - Key-value pairs for storing extra info
>    * - ``address``
>      - object
>      - Address: city, country, line1, line2, postal_code, state
>    * - ``balance``
>      - integer
>      - Current balance in cents. Negative = credit, positive = amount owed
>    * - ``currency``
>      - string
>      - Three-letter ISO currency code for recurring billing
>    * - ``delinquent``
>      - boolean
>      - True if customer has a past-due invoice
>    * - ``created``
>      - timestamp

---

### Chunk 52 | ID: `60030f1b-615c-4c82-b18b-f9b1bf34cc1c`

**Metadata:**
```json
{
  "Header 2": "The Customer Object",
  "Header 1": "Customers",
  "version": "v1",
  "Header 3": "Key Fields",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> - boolean
>      - True if customer has a past-due invoice
>    * - ``created``
>      - timestamp
>      - Unix timestamp of creation
>    * - ``livemode``
>      - boolean
>      - True if live mode, false if test mode
>    * - ``default_source``
>      - string
>      - ID of default payment source attached to this customer
>    * - ``invoice_settings.default_source``
>      - string
>      - ID of default source for subscriptions/invoices

---

### Chunk 53 | ID: `2e6fdea6-74f6-4b9f-abec-c25fd480cac6`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "Header 3": "Example Object",
  "version": "v1",
  "api_class": "CUSTOMERS",
  "Header 2": "The Customer Object"
}
```

**Content:**
> Example Object
> 
> .. code-block:: json
> 
>    {
>      "id": "cus_NffrFeUfNV2Hib",
>      "object": "customer",
>      "full_name": "Jenny Rosen",
>      "email": "jennyrosen@example.com",
>      "phone": null,
>      "description": null,
>      "metadata": {},
>      "address": null,
>      "balance": 0,
>      "currency": null,
>      "delinquent": false,
>      "created": 1680893993,
>      "livemode": false,
>      "default_source": null,
>      "invoice_settings": {
>        "default_source": null,
>        "custom_fields": null,
>        "footer": null
>      }
>    }

---

### Chunk 54 | ID: `07f25032-6f5f-4cc2-8f38-99b3b63ac1f0`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Customers",
  "api_class": "CUSTOMERS",
  "Header 2": "Create a Customer"
}
```

**Content:**
> Create a Customer
> 
> **POST** ``/v1/customers``

---

### Chunk 55 | ID: `8ba0f69b-5cda-492f-8e1a-9edbc142048f`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "api_class": "CUSTOMERS",
  "Header 2": "Create a Customer",
  "version": "v1",
  "Header 3": "Parameters"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 15 30

---

### Chunk 56 | ID: `7d9c0355-2e2a-47bc-8e6e-73494b9bf1cb`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "version": "v1",
  "Header 2": "Create a Customer",
  "Header 1": "Customers",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``full_name``
>      - string
>      - optional
>      - Full name or business name (max 256 chars)
>    * - ``email``
>      - string
>      - optional
>      - Email address (max 512 chars)
>    * - ``phone``
>      - string
>      - optional
>      - Phone number (max 20 chars)
>    * - ``description``
>      - string
>      - optional
>      - Arbitrary string for display/notes
>    * - ``metadata``
>      - object
>      - optional
>      - Key-value pairs for storing extra info
>    * - ``address``
>      - object
>      - optional
>      - Address fields: city, country, line1, line2, postal_code, state
>    * - ``balance``
>      - integer
>      - optional
>      - Starting balance in cents
>    * - ``source``
>      - string
>      - optional
>      - Token or source ID to attach as the customer's default payment source
>    * - ``invoice_settings.default_source``
>      - string
>      - optional
>      - Default source ID for invoices/subscriptions

---

### Chunk 57 | ID: `a0b936c0-3ac1-4e08-a116-dd35e4f712db`

**Metadata:**
```json
{
  "Header 2": "Create a Customer",
  "api_class": "CUSTOMERS",
  "version": "v1",
  "Header 1": "Customers",
  "Header 3": "Returns"
}
```

**Content:**
> Returns
> 
> Returns the Customer object after successful creation. Raises an error if parameters are invalid.

---

### Chunk 58 | ID: `bf7992b2-d899-45f7-86ea-3a42eae45b00`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Create a Customer",
  "api_class": "CUSTOMERS",
  "Header 1": "Customers",
  "Header 3": "Example Request"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/customers \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d full_name="Jenny Rosen" \
>      --data-urlencode email="jennyrosen@example.com"

---

### Chunk 59 | ID: `a7ffb7a9-b078-439f-b476-bdec043349fe`

**Metadata:**
```json
{
  "version": "v1",
  "Header 3": "Example Response",
  "api_class": "CUSTOMERS",
  "Header 2": "Create a Customer",
  "Header 1": "Customers"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "cus_NffrFeUfNV2Hib",
>      "object": "customer",
>      "full_name": "Jenny Rosen",
>      "email": "jennyrosen@example.com",
>      "balance": 0,
>      "created": 1680893993,
>      "livemode": false,
>      "default_source": null,
>      "metadata": {}
>    }

---

### Chunk 60 | ID: `b378f86d-48ab-49bd-a396-c40cf2dc2ced`

**Metadata:**
```json
{
  "Header 2": "Update a Customer",
  "api_class": "CUSTOMERS",
  "version": "v1",
  "Header 1": "Customers"
}
```

**Content:**
> Update a Customer
> 
> **POST** ``/v1/customers/:id``

---

### Chunk 61 | ID: `50c94cc3-41eb-48b6-be14-7469d727d76f`

**Metadata:**
```json
{
  "Header 2": "Update a Customer",
  "Header 3": "Parameters",
  "Header 1": "Customers",
  "version": "v1",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> Parameters
> 
> Any subset of fields can be updated. Pass an empty string to clear a field.
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 45
> 
>    * - Parameter
>      - Type
>      - Description
>    * - ``full_name``
>      - string
>      - Full name or business name
>    * - ``email``
>      - string
>      - Email address
>    * - ``phone``
>      - string
>      - Phone number
>    * - ``description``
>      - string
>      - Arbitrary string for display/notes
>    * - ``metadata``
>      - object
>      - Key-value pairs. Set a key to empty string to unset it
>    * - ``address``
>      - object
>      - Address: city, country, line1, line2, postal_code, state
>    * - ``balance``
>      - integer
>      - Balance in cents. Negative = credit, positive = amount owed
>    * - ``source``
>      - string
>      - New default payment source token or ID
>    * - ``invoice_settings.default_source``
>      - string
>      - Default source ID for invoices/subscriptions

---

### Chunk 62 | ID: `dcddbe55-d725-45fe-a425-749e2f26505b`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 3": "Returns",
  "Header 1": "Customers",
  "version": "v1",
  "Header 2": "Update a Customer"
}
```

**Content:**
> Returns
> 
> Returns the updated Customer object. Raises an error if parameters are invalid.

---

### Chunk 63 | ID: `6b03b4e6-0ad2-431d-a471-1b2d7744c91f`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Update a Customer",
  "api_class": "CUSTOMERS",
  "Header 1": "Customers",
  "Header 3": "Example Request"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
>      -u "<<YOUR_SECRET_KEY>>" \
>      --data-urlencode email="alice@new.com"

---

### Chunk 64 | ID: `8b2e4c45-e694-4be0-a763-f3471aac27ee`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 2": "Update a Customer",
  "Header 3": "Example Response",
  "Header 1": "Customers",
  "version": "v1"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "cus_NffrFeUfNV2Hib",
>      "object": "customer",
>      "full_name": "Jenny Rosen",
>      "email": "alice@new.com",
>      "balance": 0,
>      "created": 1680893993,
>      "livemode": false,
>      "default_source": null,
>      "metadata": {}
>    }

---

### Chunk 65 | ID: `aba46622-0a04-4fbf-b2f5-8007d1917a61`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "api_class": "CUSTOMERS",
  "Header 2": "Retrieve a Customer",
  "version": "v1"
}
```

**Content:**
> Retrieve a Customer
> 
> **GET** ``/v1/customers/:id``

---

### Chunk 66 | ID: `5779ea99-1df5-4f9f-b78c-23108a900f9f`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 2": "Retrieve a Customer",
  "Header 3": "Parameters",
  "version": "v1",
  "Header 1": "Customers"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 20 20 60
> 
>    * - Parameter
>      - Type
>      - Description
>    * - ``id``
>      - string (path)
>      - The ID of the customer to retrieve

---

### Chunk 67 | ID: `6f261124-4106-4b83-91d0-c7770a539a0a`

**Metadata:**
```json
{
  "Header 2": "Retrieve a Customer",
  "api_class": "CUSTOMERS",
  "Header 1": "Customers",
  "Header 3": "Returns",
  "version": "v1"
}
```

**Content:**
> Returns
> 
> Returns the Customer object for a valid identifier. If the customer was deleted, returns a subset with ``deleted: true``.

---

### Chunk 68 | ID: `6dc7f208-d1df-4930-b672-ffedcf43c79a`

**Metadata:**
```json
{
  "Header 2": "Retrieve a Customer",
  "version": "v1",
  "api_class": "CUSTOMERS",
  "Header 3": "Example Request",
  "Header 1": "Customers"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
>      -u "<<YOUR_SECRET_KEY>>"

---

### Chunk 69 | ID: `8ce95764-469b-4dd1-92aa-dad362660c7e`

**Metadata:**
```json
{
  "Header 3": "Example Response",
  "Header 2": "Retrieve a Customer",
  "Header 1": "Customers",
  "version": "v1",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "cus_NffrFeUfNV2Hib",
>      "object": "customer",
>      "full_name": "Jenny Rosen",
>      "email": "jennyrosen@example.com",
>      "balance": 0,
>      "delinquent": false,
>      "created": 1680893993,
>      "livemode": false,
>      "default_source": null,
>      "metadata": {}
>    }

---

### Chunk 70 | ID: `a9167a20-49e0-4adb-b88e-64abf6d5e19f`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "version": "v1",
  "Header 1": "Customers",
  "Header 2": "List All Customers"
}
```

**Content:**
> List All Customers
> 
> **GET** ``/v1/customers``

---

### Chunk 71 | ID: `6d9737f4-a544-42b8-bbdd-a18ffcf0f61d`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 2": "List All Customers",
  "Header 1": "Customers",
  "Header 3": "Parameters",
  "version": "v1"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 25 20 15 40

---

### Chunk 72 | ID: `aacf64f5-b53e-4d22-9dc1-622be6eaa8d0`

**Metadata:**
```json
{
  "Header 2": "List All Customers",
  "api_class": "CUSTOMERS",
  "Header 3": "Parameters",
  "Header 1": "Customers",
  "version": "v1"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``email``
>      - string
>      - optional
>      - Filter by exact email address (case-sensitive)
>    * - ``limit``
>      - integer
>      - optional
>      - Number of results to return (1–100, default 10)
>    * - ``starting_after``
>      - string
>      - optional
>      - Customer ID cursor — fetch the next page after this ID
>    * - ``ending_before``
>      - string
>      - optional
>      - Customer ID cursor — fetch the previous page before this ID
>    * - ``created.gt``
>      - integer
>      - optional
>      - Return customers created after this Unix timestamp (exclusive)
>    * - ``created.gte``
>      - integer
>      - optional
>      - Return customers created at or after this Unix timestamp (inclusive)
>    * - ``created.lt``
>      - integer
>      - optional
>      - Return customers created before this Unix timestamp (exclusive)
>    * - ``created.lte``
>      - integer
>      - optional

---

### Chunk 73 | ID: `ba18551a-ae93-4b2d-bd4f-713d1b4932cf`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "api_class": "CUSTOMERS",
  "Header 2": "List All Customers",
  "Header 1": "Customers",
  "version": "v1"
}
```

**Content:**
> * - ``created.lte``
>      - integer
>      - optional
>      - Return customers created at or before this Unix timestamp (inclusive)

---

### Chunk 74 | ID: `1173ecf5-7b8f-4da3-b81a-287384c8e935`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "Header 2": "List All Customers",
  "version": "v1",
  "Header 3": "Returns",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> Returns
> 
> A dictionary with a ``data`` array of Customer objects, sorted newest first. Includes ``has_more`` boolean for pagination.

---

### Chunk 75 | ID: `ca963466-5b54-479a-bf68-60c851ab03e3`

**Metadata:**
```json
{
  "Header 1": "Customers",
  "api_class": "CUSTOMERS",
  "Header 3": "Example Request",
  "Header 2": "List All Customers",
  "version": "v1"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl -G https://api.stripe.com/v1/customers \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d limit=3

---

### Chunk 76 | ID: `a2c62a94-b81f-411f-bceb-4f5f11479a2b`

**Metadata:**
```json
{
  "Header 3": "Example Response",
  "version": "v1",
  "api_class": "CUSTOMERS",
  "Header 2": "List All Customers",
  "Header 1": "Customers"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "object": "list",
>      "url": "/v1/customers",
>      "has_more": false,
>      "data": [
>        {
>          "id": "cus_NffrFeUfNV2Hib",
>          "object": "customer",
>          "full_name": "Jenny Rosen",
>          "email": "jennyrosen@example.com",
>          "balance": 0,
>          "created": 1680893993,
>          "livemode": false,
>          "default_source": null,
>          "metadata": {}
>        }
>      ]
>    }

---

### Chunk 77 | ID: `2d5bd95c-b1a4-4e25-9111-1e6bc6fe7f0a`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 2": "Key Fields",
  "version": "v2",
  "Header 1": "The Customer Object"
}
```

**Content:**
> | Field | Type | Description |
> |-------|------|-------------|
> | `id` | string | Unique identifier (e.g. `cus_NffrFeUfNV2Hib`) |
> | `object` | string | Always `"customer"` |
> | `name` | string | Full name or business name |
> | `email` | string | Customer's email address |
> | `phone` | string | Customer's phone number |
> | `description` | string | Arbitrary string for display/notes |
> | `metadata` | object | Key-value pairs for storing extra info |
> | `address` | object | Address: city, country, line1, line2, postal_code, state |
> | `balance` | integer | Current balance in cents. Negative = credit, positive = amount owed |
> | `currency` | string | Three-letter ISO currency code for recurring billing |
> | `delinquent` | boolean | True if customer has a past-due invoice |
> | `created` | timestamp | Unix timestamp of creation |
> | `livemode` | boolean | True if live mode, false if test mode |
> | `default_source` | string | ID of default payment source |

---

### Chunk 78 | ID: `ee9a83bb-db95-4d23-b0b3-b0e67eea7e82`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "The Customer Object",
  "Header 2": "Key Fields",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> | `default_source` | string | ID of default payment source |
> | `invoice_settings.default_payment_method` | string | ID of default PaymentMethod for subscriptions/invoices |

---

### Chunk 79 | ID: `9f028223-71c7-4d88-ba09-05393e67c6f0`

**Metadata:**
```json
{
  "Header 1": "The Customer Object",
  "version": "v2",
  "Header 2": "Example",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> ```json
> {
> "id": "cus_NffrFeUfNV2Hib",
> "object": "customer",
> "name": "Jenny Rosen",
> "email": "jennyrosen@example.com",
> "phone": null,
> "description": null,
> "metadata": {},
> "address": null,
> "balance": 0,
> "currency": null,
> "delinquent": false,
> "created": 1680893993,
> "livemode": false,
> "default_source": null,
> "invoice_settings": {
> "default_payment_method": null,
> "custom_fields": null,
> "footer": null,
> "rendering_options": null
> },
> "invoice_prefix": "0759376C",
> "next_invoice_sequence": 1,
> "preferred_locales": [],
> "shipping": null,
> "tax_exempt": "none",
> "test_clock": null
> }
> ```

---

### Chunk 80 | ID: `0c8a5ea4-7b1a-4359-89d3-58137f5df22d`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "CUSTOMERS",
  "Header 1": "Customers"
}
```

**Content:**
> A Customer object represents a customer of your business. Use it to save payment and contact information and track payments.

---

### Chunk 81 | ID: `bcd70efa-a0f6-4899-9d5c-369326832d17`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "version": "v2",
  "Header 1": "Customers",
  "Header 2": "Endpoints"
}
```

**Content:**
> | Method | Endpoint | Description |
> |--------|----------|-------------|
> | POST | `/v1/customers` | Create a customer |
> | POST | `/v1/customers/:id` | Update a customer |
> | GET | `/v1/customers/:id` | Retrieve a customer |
> | GET | `/v1/customers` | List all customers |

---

### Chunk 82 | ID: `eb4d3c71-14d6-4714-b876-051db667565d`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Create a Customer",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> **POST** `/v1/customers`

---

### Chunk 83 | ID: `ee6e982e-e21d-4b4e-9e6e-e0b8d4916c09`

**Metadata:**
```json
{
  "Header 2": "Parameters",
  "api_class": "CUSTOMERS",
  "version": "v2",
  "Header 1": "Create a Customer"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `name` | string | optional | Full name or business name (max 256 chars) |
> | `email` | string | optional | Email address (max 512 chars) |
> | `phone` | string | optional | Phone number (max 20 chars) |
> | `description` | string | optional | Arbitrary string for display/notes |
> | `metadata` | object | optional | Key-value pairs for storing extra info |
> | `address` | object | optional | Address: city, country, line1, line2, postal_code, state |
> | `balance` | integer | optional | Starting balance in cents |
> | `payment_method` | string | optional | ID of a PaymentMethod to attach |
> | `invoice_settings.default_payment_method` | string | optional | Default PaymentMethod ID for invoices/subscriptions |

---

### Chunk 84 | ID: `44937676-dea8-4e90-a314-6264afa497e6`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Returns",
  "Header 1": "Create a Customer",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> Returns the Customer object after successful creation. Raises an error if parameters are invalid.

---

### Chunk 85 | ID: `051ea2e3-08ad-474e-b4cd-d8978a8ae7d5`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Example Request",
  "Header 1": "Create a Customer",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/customers \
> -u "<<YOUR_SECRET_KEY>>" \
> -d name="Jenny Rosen" \
> --data-urlencode email="jennyrosen@example.com"
> ```

---

### Chunk 86 | ID: `5e4f3d39-838e-4c5d-a93a-b0fbf3c90f20`

**Metadata:**
```json
{
  "Header 1": "Create a Customer",
  "version": "v2",
  "api_class": "CUSTOMERS",
  "Header 2": "Example Response"
}
```

**Content:**
> ```json
> {
> "id": "cus_NffrFeUfNV2Hib",
> "object": "customer",
> "name": "Jenny Rosen",
> "email": "jennyrosen@example.com",
> "phone": null,
> "description": null,
> "metadata": {},
> "address": null,
> "balance": 0,
> "created": 1680893993,
> "livemode": false,
> "default_source": null,
> "invoice_settings": {
> "default_payment_method": null,
> "custom_fields": null,
> "footer": null,
> "rendering_options": null
> }
> }
> ```

---

### Chunk 87 | ID: `a37752a5-d368-49b1-b8d4-1258750e9e96`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Update a Customer",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> **POST** `/v1/customers/:id`

---

### Chunk 88 | ID: `a4be6023-bbc5-4661-909d-2ffb5bd1c8d3`

**Metadata:**
```json
{
  "Header 1": "Update a Customer",
  "version": "v2",
  "api_class": "CUSTOMERS",
  "Header 2": "Parameters"
}
```

**Content:**
> Any subset of fields can be updated. Pass an empty string to clear a field.  
> | Parameter | Type | Description |
> |-----------|------|-------------|
> | `name` | string | Full name or business name |
> | `email` | string | Email address |
> | `phone` | string | Phone number |
> | `description` | string | Arbitrary string for display/notes |
> | `metadata` | object | Key-value pairs. Set a key to empty string to unset it |
> | `address` | object | Address: city, country, line1, line2, postal_code, state |
> | `balance` | integer | Balance in cents. Negative = credit, positive = amount owed |
> | `invoice_settings.default_payment_method` | string | Default PaymentMethod ID for invoices/subscriptions |

---

### Chunk 89 | ID: `00ea34cc-7dac-4b6c-80df-7386238c545d`

**Metadata:**
```json
{
  "Header 1": "Update a Customer",
  "api_class": "CUSTOMERS",
  "Header 2": "Returns",
  "version": "v2"
}
```

**Content:**
> Returns the updated Customer object. Raises an error if parameters are invalid.

---

### Chunk 90 | ID: `e7278cc8-0f95-4901-9c88-76370c944e46`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 1": "Update a Customer",
  "Header 2": "Example Request",
  "version": "v2"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
> -u "<<YOUR_SECRET_KEY>>" \
> --data-urlencode email="alice@new.com"
> ```

---

### Chunk 91 | ID: `726b2151-6e25-49a8-a198-e93dd5006672`

**Metadata:**
```json
{
  "Header 1": "Update a Customer",
  "api_class": "CUSTOMERS",
  "Header 2": "Example Response",
  "version": "v2"
}
```

**Content:**
> ```json
> {
> "id": "cus_NffrFeUfNV2Hib",
> "object": "customer",
> "name": "Jenny Rosen",
> "email": "alice@new.com",
> "phone": null,
> "description": null,
> "metadata": {},
> "balance": 0,
> "created": 1680893993,
> "livemode": false
> }
> ```

---

### Chunk 92 | ID: `49c4247e-d1b2-48df-a6aa-8d5b8ec091f1`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 1": "Retrieve a Customer",
  "version": "v2"
}
```

**Content:**
> **GET** `/v1/customers/:id`

---

### Chunk 93 | ID: `dd616489-dc7f-47e1-97f6-fbfc649e2bae`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 1": "Retrieve a Customer",
  "version": "v2",
  "Header 2": "Parameters"
}
```

**Content:**
> | Parameter | Type | Description |
> |-----------|------|-------------|
> | `id` | string (path) | The ID of the customer to retrieve |

---

### Chunk 94 | ID: `751386c8-5cbc-4174-8dd3-ff9341058442`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Retrieve a Customer",
  "api_class": "CUSTOMERS",
  "Header 2": "Returns"
}
```

**Content:**
> Returns the Customer object for a valid identifier. If the customer was deleted, returns a subset of fields with `deleted: true`.

---

### Chunk 95 | ID: `855c6fce-ff60-4304-a076-85cfb2827d14`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "Header 1": "Retrieve a Customer",
  "Header 2": "Example Request",
  "version": "v2"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
> -u "<<YOUR_SECRET_KEY>>"
> ```

---

### Chunk 96 | ID: `c26f6852-2323-40d8-8697-364a5a13d5e4`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "CUSTOMERS",
  "Header 1": "Retrieve a Customer",
  "Header 2": "Example Response"
}
```

**Content:**
> ```json
> {
> "id": "cus_NffrFeUfNV2Hib",
> "object": "customer",
> "name": "Jenny Rosen",
> "email": "jennyrosen@example.com",
> "phone": null,
> "description": null,
> "metadata": {},
> "address": null,
> "balance": 0,
> "created": 1680893993,
> "livemode": false,
> "default_source": null,
> "delinquent": false,
> "invoice_settings": {
> "default_payment_method": null,
> "custom_fields": null,
> "footer": null,
> "rendering_options": null
> }
> }
> ```

---

### Chunk 97 | ID: `22dae9ec-9777-447c-b0c0-f4353d19bc4d`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "version": "v2",
  "Header 1": "List All Customers"
}
```

**Content:**
> **GET** `/v1/customers`  
> Returns a list of customers sorted by creation date, newest first.

---

### Chunk 98 | ID: `5b81a873-56ce-4bb4-a6f3-3a1e6de5ece4`

**Metadata:**
```json
{
  "Header 1": "List All Customers",
  "api_class": "CUSTOMERS",
  "version": "v2",
  "Header 2": "Parameters"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `email` | string | optional | Filter by exact email address (case-sensitive) |
> | `limit` | integer | optional | Number of results to return (1–100, default 10) |
> | `starting_after` | string | optional | Customer ID cursor — fetch the next page after this ID |
> | `ending_before` | string | optional | Customer ID cursor — fetch the previous page before this ID |
> | `created.gt` | integer | optional | Return customers created after this Unix timestamp (exclusive) |
> | `created.gte` | integer | optional | Return customers created at or after this Unix timestamp (inclusive) |
> | `created.lt` | integer | optional | Return customers created before this Unix timestamp (exclusive) |
> | `created.lte` | integer | optional | Return customers created at or before this Unix timestamp (inclusive) |

---

### Chunk 99 | ID: `27e86a7c-d436-4def-83f5-e065654cb746`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "CUSTOMERS",
  "Header 2": "Returns",
  "Header 1": "List All Customers"
}
```

**Content:**
> A dictionary with a `data` array of Customer objects. Includes `has_more` to indicate if another page exists.

---

### Chunk 100 | ID: `b6480837-d464-445a-8640-dcd04e4fdef2`

**Metadata:**
```json
{
  "Header 2": "Example Request",
  "Header 1": "List All Customers",
  "version": "v2",
  "api_class": "CUSTOMERS"
}
```

**Content:**
> ```curl
> curl -G https://api.stripe.com/v1/customers \
> -u "<<YOUR_SECRET_KEY>>" \
> -d limit=3
> ```

---

### Chunk 101 | ID: `bca1a914-94bc-4aa5-82bc-0a256844c09b`

**Metadata:**
```json
{
  "api_class": "CUSTOMERS",
  "version": "v2",
  "Header 1": "List All Customers",
  "Header 2": "Example Response"
}
```

**Content:**
> ```json
> {
> "object": "list",
> "url": "/v1/customers",
> "has_more": false,
> "data": [
> {
> "id": "cus_NffrFeUfNV2Hib",
> "object": "customer",
> "name": "Jenny Rosen",
> "email": "jennyrosen@example.com",
> "phone": null,
> "balance": 0,
> "created": 1680893993,
> "livemode": false,
> "metadata": {}
> }
> ]
> }
> ```

---

### Chunk 102 | ID: `cf1889b0-3256-4dbb-a949-fa9824d8d453`

**Metadata:**
```json
{
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "version": "v1"
}
```

**Content:**
> PaymentIntents
> 
> A PaymentIntent guides you through collecting a payment from a customer. Create exactly one per order or session.
> 
> .. note::
> 
>    In v1, ``automatic_payment_methods`` is not supported. Payment method types must be explicitly specified via ``payment_method_types``. The ``confirmation_method`` field is also not available; all confirmations are manual by default.

---

### Chunk 103 | ID: `70534157-fa19-406c-9d18-2b7c192df73e`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Endpoints",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Endpoints
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 15 50 35
> 
>    * - Method
>      - Endpoint
>      - Description
>    * - POST
>      - ``/v1/payment_intents``
>      - Create a PaymentIntent
>    * - POST
>      - ``/v1/payment_intents/:id/confirm``
>      - Confirm a PaymentIntent
>    * - GET
>      - ``/v1/payment_intents/:id``
>      - Retrieve a PaymentIntent
>    * - GET
>      - ``/v1/payment_intents``
>      - List all PaymentIntents
>    * - POST
>      - ``/v1/payment_intents/:id/cancel``
>      - Cancel a PaymentIntent

---

### Chunk 104 | ID: `faaca457-5355-47f9-963a-d81291bd1652`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "The PaymentIntent Object",
  "version": "v1",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> The PaymentIntent Object

---

### Chunk 105 | ID: `f34e7d7f-850c-4f6d-8d53-c81b1c65a75b`

**Metadata:**
```json
{
  "Header 2": "The PaymentIntent Object",
  "version": "v1",
  "Header 3": "Status Lifecycle",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Status Lifecycle
> 
> ``requires_payment_method`` → ``requires_confirmation`` → ``requires_action`` → ``processing`` → ``succeeded``
> 
> Or: → ``requires_capture`` (if ``capture_method=manual``) | ``canceled``

---

### Chunk 106 | ID: `4babe280-5bed-4400-acb5-dbfcd26f812d`

**Metadata:**
```json
{
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Key Fields",
  "version": "v1",
  "Header 2": "The PaymentIntent Object"
}
```

**Content:**
> Key Fields
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 45

---

### Chunk 107 | ID: `d95661d0-089d-434c-b280-0f7d56c24fee`

**Metadata:**
```json
{
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 2": "The PaymentIntent Object",
  "Header 3": "Key Fields"
}
```

**Content:**
> * - Field
>      - Type
>      - Description
>    * - ``id``
>      - string
>      - Unique identifier (e.g. ``pi_3MtwBwLkdIwHu7ix28a3tqPa``)
>    * - ``object``
>      - string
>      - Always ``"payment_intent"``
>    * - ``amount``
>      - integer
>      - Amount in smallest currency unit (e.g. cents)
>    * - ``currency``
>      - string
>      - Three-letter ISO currency code (e.g. ``"usd"``)
>    * - ``status``
>      - enum
>      - Current status (see lifecycle above)
>    * - ``customer``
>      - string
>      - ID of the Customer this PaymentIntent belongs to
>    * - ``source``
>      - string
>      - ID of the Source or card token to charge
>    * - ``payment_method_types``
>      - array
>      - Explicit list of allowed payment method types (e.g. ``["card"]``)
>    * - ``capture_method``
>      - enum
>      - ``automatic`` or ``manual``
>    * - ``amount_received``
>      - integer
>      - Amount successfully received, in smallest currency unit
>    * - ``amount_capturable``
>      - integer

---

### Chunk 108 | ID: `d2fa4b22-312b-41df-b3d2-a50c59cf7ea7`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "The PaymentIntent Object",
  "Header 3": "Key Fields"
}
```

**Content:**
> * - ``amount_capturable``
>      - integer
>      - Amount that can still be captured (manual capture only)
>    * - ``client_secret``
>      - string
>      - Secret used client-side to confirm the PaymentIntent
>    * - ``latest_charge``
>      - string
>      - ID of the latest Charge created
>    * - ``last_payment_error``
>      - object
>      - Error from the last payment attempt, if any
>    * - ``next_action``
>      - object
>      - Actions required to complete the payment (e.g. 3D Secure redirect)
>    * - ``canceled_at``
>      - timestamp
>      - When the PaymentIntent was canceled
>    * - ``cancellation_reason``
>      - string
>      - Reason for cancellation
>    * - ``description``
>      - string
>      - Arbitrary description
>    * - ``metadata``
>      - object
>      - Key-value pairs for storing extra info
>    * - ``receipt_email``
>      - string
>      - Email to send receipt to after successful payment
>    * - ``statement_descriptor``
>      - string
>      - Text on customer's bank statement (max 22 chars)

---

### Chunk 109 | ID: `78bd4bee-f020-4d36-89f0-466f8fb8103a`

**Metadata:**
```json
{
  "Header 2": "The PaymentIntent Object",
  "Header 3": "Key Fields",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "version": "v1"
}
```

**Content:**
> - string
>      - Text on customer's bank statement (max 22 chars)
>    * - ``on_behalf_of``
>      - string
>      - Connected account ID on whose behalf the charge is made
>    * - ``transfer_data.destination``
>      - string
>      - Connected account to transfer funds to after success
>    * - ``application_fee_amount``
>      - integer
>      - Fee in cents to be collected for the platform
>    * - ``created``
>      - timestamp
>      - Unix timestamp of creation
>    * - ``livemode``
>      - boolean
>      - True if live mode, false if test mode

---

### Chunk 110 | ID: `45a1b0dd-d3e5-4932-8099-ef29e69de153`

**Metadata:**
```json
{
  "Header 3": "Example Object",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "Header 2": "The PaymentIntent Object",
  "version": "v1"
}
```

**Content:**
> Example Object
> 
> .. code-block:: json
> 
>    {
>      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
>      "object": "payment_intent",
>      "amount": 2000,
>      "currency": "usd",
>      "status": "requires_source",
>      "customer": null,
>      "source": null,
>      "payment_method_types": ["card"],
>      "capture_method": "automatic",
>      "amount_received": 0,
>      "amount_capturable": 0,
>      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
>      "latest_charge": null,
>      "last_payment_error": null,
>      "next_action": null,
>      "canceled_at": null,
>      "cancellation_reason": null,
>      "description": null,
>      "metadata": {},
>      "receipt_email": null,
>      "statement_descriptor": null,
>      "on_behalf_of": null,
>      "transfer_data": null,
>      "application_fee_amount": null,
>      "created": 1680800504,
>      "livemode": false
>    }

---

### Chunk 111 | ID: `36d7c064-6321-458d-8df9-bdad7b8c073e`

**Metadata:**
```json
{
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 2": "Create a PaymentIntent"
}
```

**Content:**
> Create a PaymentIntent
> 
> **POST** ``/v1/payment_intents``

---

### Chunk 112 | ID: `54049be6-c6e2-41ab-87d3-61df80c66869`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Create a PaymentIntent",
  "Header 3": "Parameters",
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 15 30

---

### Chunk 113 | ID: `7f90e5f8-ead2-4daa-abac-b3f4d772774e`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "Header 2": "Create a PaymentIntent",
  "Header 3": "Parameters",
  "version": "v1"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``amount``
>      - integer
>      - **required**
>      - Amount in smallest currency unit (e.g. 2000 = $20.00 USD)
>    * - ``currency``
>      - enum
>      - **required**
>      - Three-letter ISO currency code (e.g. ``usd``)
>    * - ``payment_method_types``
>      - array
>      - **required**
>      - List of payment method types (e.g. ``["card"]``). No default in v1
>    * - ``customer``
>      - string
>      - optional
>      - ID of the Customer to attach this PaymentIntent to
>    * - ``source``
>      - string
>      - optional
>      - ID of a Source or card token to attach
>    * - ``capture_method``
>      - enum
>      - optional
>      - ``automatic`` (default) charges immediately; ``manual`` requires a separate capture step
>    * - ``confirm``
>      - boolean
>      - optional
>      - If ``true``, confirm immediately upon creation
>    * - ``description``
>      - string
>      - optional
>      - Arbitrary description
>    * - ``metadata``
>      - object

---

### Chunk 114 | ID: `8a8db575-d701-402f-8cd6-d3f183061692`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 1": "PaymentIntents",
  "Header 2": "Create a PaymentIntent",
  "Header 3": "Parameters"
}
```

**Content:**
> - string
>      - optional
>      - Arbitrary description
>    * - ``metadata``
>      - object
>      - optional
>      - Key-value pairs for storing extra info
>    * - ``receipt_email``
>      - string
>      - optional
>      - Email to send receipt to after successful payment
>    * - ``statement_descriptor``
>      - string
>      - optional
>      - Text on customer's bank statement (max 22 chars)
>    * - ``on_behalf_of``
>      - string
>      - optional
>      - Connected account ID on whose behalf the charge is made
>    * - ``transfer_data.destination``
>      - string
>      - optional
>      - Connected account to transfer funds to after success
>    * - ``application_fee_amount``
>      - integer
>      - optional
>      - Fee in cents to collect for the platform (requires ``on_behalf_of``)
>    * - ``return_url``
>      - string
>      - optional
>      - URL to redirect to after actions (e.g. 3D Secure) are completed

---

### Chunk 115 | ID: `2897a521-12d6-45fd-9014-f03d00a13b8e`

**Metadata:**
```json
{
  "Header 3": "Returns",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "Header 2": "Create a PaymentIntent",
  "version": "v1"
}
```

**Content:**
> Returns
> 
> Returns a PaymentIntent object.

---

### Chunk 116 | ID: `66d50aa9-d53f-4c22-8a09-497fbad94090`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 3": "Example Request",
  "Header 1": "PaymentIntents",
  "Header 2": "Create a PaymentIntent"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/payment_intents \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d amount=2000 \
>      -d currency=usd \
>      -d "payment_method_types[0]"=card

---

### Chunk 117 | ID: `11d49b28-ed8b-46ff-beaf-e3fe7960918d`

**Metadata:**
```json
{
  "Header 2": "Create a PaymentIntent",
  "Header 3": "Example Response",
  "version": "v1",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
>      "object": "payment_intent",
>      "amount": 2000,
>      "currency": "usd",
>      "status": "requires_source",
>      "customer": null,
>      "source": null,
>      "payment_method_types": ["card"],
>      "capture_method": "automatic",
>      "amount_received": 0,
>      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
>      "latest_charge": null,
>      "next_action": null,
>      "description": null,
>      "metadata": {},
>      "created": 1680800504,
>      "livemode": false
>    }

---

### Chunk 118 | ID: `a63c91d3-06f9-4acd-a974-425b6a0567e6`

**Metadata:**
```json
{
  "Header 2": "Confirm a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Confirm a PaymentIntent
> 
> **POST** ``/v1/payment_intents/:id/confirm``
> 
> Confirms that the customer intends to pay. Upon confirmation, the PaymentIntent will attempt to initiate a payment.
> 
> - If additional auth is needed (e.g. 3D Secure), status moves to ``requires_action`` with ``next_action`` populated.
> - If payment fails, status moves to ``requires_source``.
> - If payment succeeds, status moves to ``succeeded`` (or ``requires_capture`` if ``capture_method=manual``).

---

### Chunk 119 | ID: `1f0d754b-a791-40e9-a276-f816a32ddc36`

**Metadata:**
```json
{
  "Header 2": "Confirm a PaymentIntent",
  "version": "v1",
  "Header 3": "Parameters",
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 30 20 15 35
> 
>    * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``source``
>      - string
>      - optional
>      - ID of the Source or card token to use for this confirmation
>    * - ``return_url``
>      - string
>      - optional
>      - URL to redirect to after any required actions (e.g. 3D Secure)
>    * - ``capture_method``
>      - enum
>      - optional
>      - Override capture method: ``automatic`` or ``manual``
>    * - ``receipt_email``
>      - string
>      - optional
>      - Email to send receipt to after successful payment

---

### Chunk 120 | ID: `ff3f0c04-d242-405d-81b7-7b9f134ed9ad`

**Metadata:**
```json
{
  "version": "v1",
  "Header 3": "Returns",
  "Header 2": "Confirm a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Returns
> 
> Returns the resulting PaymentIntent after all possible transitions are applied.

---

### Chunk 121 | ID: `9d9cd8af-dce6-45c8-a8d3-ec3f601a99d1`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Confirm a PaymentIntent",
  "version": "v1",
  "Header 3": "Example Request",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/payment_intents/pi_3MtweELkdIwHu7ix0Dt0gF2H/confirm \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d source=tok_visa \
>      --data-urlencode return_url="https://www.example.com"

---

### Chunk 122 | ID: `ef6775bb-1f17-4ca3-adee-e621d204ea36`

**Metadata:**
```json
{
  "Header 2": "Confirm a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 1": "PaymentIntents",
  "Header 3": "Example Response"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "pi_3MtweELkdIwHu7ix0Dt0gF2H",
>      "object": "payment_intent",
>      "amount": 2000,
>      "currency": "usd",
>      "status": "succeeded",
>      "source": "src_1MtweELkdIwHu7ixxrsejPtG",
>      "payment_method_types": ["card"],
>      "capture_method": "automatic",
>      "amount_received": 2000,
>      "amount_capturable": 0,
>      "client_secret": "pi_3MtweELkdIwHu7ix0Dt0gF2H_secret_ALlpPMIZse0ac8YzPxkMkFgGC",
>      "latest_charge": "ch_3MtweELkdIwHu7ix05lnLAFd",
>      "next_action": null,
>      "metadata": {},
>      "created": 1680802258,
>      "livemode": false
>    }

---

### Chunk 123 | ID: `cd3b72d6-9b81-44d2-99e4-15fd49d36759`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "PaymentIntents",
  "Header 2": "Retrieve a PaymentIntent",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Retrieve a PaymentIntent
> 
> **GET** ``/v1/payment_intents/:id``

---

### Chunk 124 | ID: `af39907c-7b54-4856-9fc2-d2cf22d20942`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "version": "v1",
  "Header 2": "Retrieve a PaymentIntent",
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 25 20 55
> 
>    * - Parameter
>      - Type
>      - Description
>    * - ``id``
>      - string (path)
>      - The ID of the PaymentIntent to retrieve

---

### Chunk 125 | ID: `203af958-8bc4-4425-8bd6-b7027463b4c9`

**Metadata:**
```json
{
  "Header 2": "Retrieve a PaymentIntent",
  "Header 1": "PaymentIntents",
  "version": "v1",
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Returns"
}
```

**Content:**
> Returns
> 
> Returns a PaymentIntent if a valid identifier was provided.

---

### Chunk 126 | ID: `c5ec33be-7b04-4506-9c91-35d80c3e180f`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Retrieve a PaymentIntent",
  "Header 1": "PaymentIntents",
  "version": "v1",
  "Header 3": "Example Request"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \
>      -u "<<YOUR_SECRET_KEY>>"

---

### Chunk 127 | ID: `6efe7c85-f634-43dc-ac96-8e71b2d30738`

**Metadata:**
```json
{
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Example Response",
  "version": "v1",
  "Header 2": "Retrieve a PaymentIntent"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
>      "object": "payment_intent",
>      "amount": 2000,
>      "currency": "usd",
>      "status": "requires_source",
>      "source": null,
>      "payment_method_types": ["card"],
>      "capture_method": "automatic",
>      "amount_received": 0,
>      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
>      "latest_charge": null,
>      "canceled_at": null,
>      "description": null,
>      "metadata": {},
>      "created": 1680800504,
>      "livemode": false
>    }

---

### Chunk 128 | ID: `afd32cdb-832e-427b-890f-073a344c3067`

**Metadata:**
```json
{
  "version": "v1",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "Header 2": "List All PaymentIntents"
}
```

**Content:**
> List All PaymentIntents
> 
> **GET** ``/v1/payment_intents``

---

### Chunk 129 | ID: `0e9faf5f-4817-429a-becb-819fc9d2be36`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "Header 3": "Parameters",
  "version": "v1",
  "Header 2": "List All PaymentIntents"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 25 20 15 40

---

### Chunk 130 | ID: `fb404de4-e3d5-4509-ba5b-5c4ababf4f38`

**Metadata:**
```json
{
  "Header 2": "List All PaymentIntents",
  "Header 3": "Parameters",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "PaymentIntents",
  "version": "v1"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``customer``
>      - string
>      - optional
>      - Only return PaymentIntents for this customer ID
>    * - ``limit``
>      - integer
>      - optional
>      - Number of results to return (1–100, default 10)
>    * - ``starting_after``
>      - string
>      - optional
>      - PaymentIntent ID cursor — fetch the next page after this ID
>    * - ``ending_before``
>      - string
>      - optional
>      - PaymentIntent ID cursor — fetch the previous page before this ID
>    * - ``created.gt``
>      - integer
>      - optional
>      - Created after this Unix timestamp (exclusive)
>    * - ``created.gte``
>      - integer
>      - optional
>      - Created at or after this Unix timestamp (inclusive)
>    * - ``created.lt``
>      - integer
>      - optional
>      - Created before this Unix timestamp (exclusive)
>    * - ``created.lte``
>      - integer
>      - optional
>      - Created at or before this Unix timestamp (inclusive)

---

### Chunk 131 | ID: `73bdd0ec-d235-4477-99ed-594e4c70cf76`

**Metadata:**
```json
{
  "Header 1": "PaymentIntents",
  "version": "v1",
  "Header 2": "List All PaymentIntents",
  "Header 3": "Returns",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Returns
> 
> A dictionary with a ``data`` array of PaymentIntent objects. Includes ``has_more`` for pagination.

---

### Chunk 132 | ID: `6ae91f41-acf7-47b3-9607-c550db7cc016`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Example Request",
  "Header 1": "PaymentIntents",
  "Header 2": "List All PaymentIntents",
  "version": "v1"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl -G https://api.stripe.com/v1/payment_intents \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d limit=3

---

### Chunk 133 | ID: `506db23f-d1f5-4971-943b-2f2bd07d39fc`

**Metadata:**
```json
{
  "version": "v1",
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Example Response",
  "Header 2": "List All PaymentIntents",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "object": "list",
>      "url": "/v1/payment_intents",
>      "has_more": false,
>      "data": [
>        {
>          "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
>          "object": "payment_intent",
>          "amount": 2000,
>          "currency": "usd",
>          "status": "requires_source",
>          "source": null,
>          "payment_method_types": ["card"],
>          "capture_method": "automatic",
>          "amount_received": 0,
>          "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
>          "description": null,
>          "metadata": {},
>          "created": 1680800504,
>          "livemode": false
>        }
>      ]
>    }

---

### Chunk 134 | ID: `c281db54-4a1a-4b67-b2a0-bdb6931def2c`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "version": "v1",
  "Header 1": "PaymentIntents",
  "Header 2": "Cancel a PaymentIntent"
}
```

**Content:**
> Cancel a PaymentIntent
> 
> **POST** ``/v1/payment_intents/:id/cancel``
> 
> Cancels a PaymentIntent. Cancelable when status is: ``requires_source``, ``requires_capture``, ``requires_confirmation``, ``requires_action``, or (rarely) ``processing``.

---

### Chunk 135 | ID: `2f32b10a-e8cd-4917-9562-e535ee55ab9b`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "Header 1": "PaymentIntents",
  "Header 2": "Cancel a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v1"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 30 20 15 35
> 
>    * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``id``
>      - string (path)
>      - **required**
>      - The ID of the PaymentIntent to cancel
>    * - ``cancellation_reason``
>      - string
>      - optional
>      - Reason: ``duplicate``, ``fraudulent``, ``requested_by_customer``, or ``abandoned``

---

### Chunk 136 | ID: `52615af3-8e58-407e-b0aa-d8d591fd9d19`

**Metadata:**
```json
{
  "Header 3": "Returns",
  "Header 1": "PaymentIntents",
  "Header 2": "Cancel a PaymentIntent",
  "version": "v1",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Returns
> 
> Returns the canceled PaymentIntent object. Returns an error if already canceled or not in a cancelable state.

---

### Chunk 137 | ID: `25145c10-1742-45ef-98fe-5d9ccdbd83d9`

**Metadata:**
```json
{
  "Header 2": "Cancel a PaymentIntent",
  "version": "v1",
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Example Request",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/cancel \
>      -u "<<YOUR_SECRET_KEY>>"

---

### Chunk 138 | ID: `5d5ce435-34e3-4b34-9ab4-458fcb360f0e`

**Metadata:**
```json
{
  "Header 2": "Cancel a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "Header 3": "Example Response",
  "version": "v1",
  "Header 1": "PaymentIntents"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
>      "object": "payment_intent",
>      "amount": 2000,
>      "currency": "usd",
>      "status": "canceled",
>      "source": null,
>      "payment_method_types": ["card"],
>      "amount_received": 0,
>      "canceled_at": 1680801569,
>      "cancellation_reason": null,
>      "metadata": {},
>      "created": 1680800504,
>      "livemode": false
>    }

---

### Chunk 139 | ID: `75352b00-fa15-4d8d-98cd-01e76a1222e3`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "The PaymentIntent Object",
  "version": "v2"
}
```

**Content:**
> A PaymentIntent guides you through collecting a payment from a customer. Create one per order or session, then confirm it to initiate the charge.

---

### Chunk 140 | ID: `08191124-d8e2-444f-b15b-52db2ee34f89`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "The PaymentIntent Object",
  "Header 2": "Status Lifecycle",
  "version": "v2"
}
```

**Content:**
> `requires_payment_method` → `requires_confirmation` → `requires_action` → `processing` → `succeeded`
> Or: → `requires_capture` (if `capture_method=manual`) | `canceled`

---

### Chunk 141 | ID: `acfd1db9-d3e3-47f1-91dd-67908d984d73`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "The PaymentIntent Object",
  "version": "v2",
  "Header 2": "Key Fields"
}
```

**Content:**
> | Field | Type | Description |
> |-------|------|-------------|
> | `id` | string | Unique identifier (e.g. `pi_3MtwBwLkdIwHu7ix28a3tqPa`) |
> | `object` | string | Always `"payment_intent"` |
> | `amount` | integer | Amount in smallest currency unit (e.g. cents). Min $0.50 USD |
> | `currency` | string | Three-letter ISO currency code (e.g. `"usd"`) |
> | `status` | enum | Current status (see lifecycle above) |
> | `customer` | string | ID of the Customer this PaymentIntent belongs to |
> | `payment_method` | string | ID of the PaymentMethod attached |
> | `payment_method_types` | array | List of allowed payment method types (e.g. `["card"]`) |
> | `capture_method` | enum | `automatic` or `manual` |
> | `confirmation_method` | enum | `automatic` or `manual` |
> | `amount_received` | integer | Amount successfully received, in smallest currency unit |
> | `amount_capturable` | integer | Amount that can still be captured (manual capture only) |

---

### Chunk 142 | ID: `f39f6783-649b-4396-b170-d36bdcd947b9`

**Metadata:**
```json
{
  "Header 1": "The PaymentIntent Object",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 2": "Key Fields"
}
```

**Content:**
> | `amount_capturable` | integer | Amount that can still be captured (manual capture only) |
> | `client_secret` | string | Secret used client-side to confirm the PaymentIntent |
> | `latest_charge` | string | ID of the latest Charge created |
> | `last_payment_error` | object | Error from the last payment attempt, if any |
> | `next_action` | object | Actions required to complete the payment (e.g. 3D Secure redirect) |
> | `canceled_at` | timestamp | When the PaymentIntent was canceled |
> | `cancellation_reason` | string | Reason for cancellation |
> | `description` | string | Arbitrary description |
> | `metadata` | object | Key-value pairs for storing extra info |
> | `receipt_email` | string | Email to send receipt to after successful payment |
> | `statement_descriptor` | string | Text on customer's bank statement (max 22 chars) |
> | `on_behalf_of` | string | Connected account ID on whose behalf the charge is made |

---

### Chunk 143 | ID: `96a21c19-8cfb-4a91-b2b5-98dc772c1c87`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Key Fields",
  "version": "v2",
  "Header 1": "The PaymentIntent Object"
}
```

**Content:**
> | `on_behalf_of` | string | Connected account ID on whose behalf the charge is made |
> | `transfer_data.destination` | string | Connected account to transfer funds to after success |
> | `transfer_group` | string | Groups related transfers together |
> | `application_fee_amount` | integer | Fee in cents to be collected for the platform |
> | `setup_future_usage` | enum | `on_session` or `off_session` — save payment method for future use |
> | `created` | timestamp | Unix timestamp of creation |
> | `livemode` | boolean | True if live mode, false if test mode |

---

### Chunk 144 | ID: `b467cb06-90ed-4610-9a0d-499da58d7dcb`

**Metadata:**
```json
{
  "Header 2": "Example Object",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 1": "The PaymentIntent Object"
}
```

**Content:**
> ```json
> {
> "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
> "object": "payment_intent",
> "amount": 2000,
> "currency": "usd",
> "status": "requires_payment_method",
> "customer": null,
> "payment_method": null,
> "payment_method_types": ["card", "link"],
> "capture_method": "automatic",
> "confirmation_method": "automatic",
> "amount_received": 0,
> "amount_capturable": 0,
> "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
> "latest_charge": null,
> "last_payment_error": null,
> "next_action": null,
> "canceled_at": null,
> "cancellation_reason": null,
> "description": null,
> "metadata": {},
> "receipt_email": null,
> "statement_descriptor": null,
> "on_behalf_of": null,
> "transfer_data": null,
> "transfer_group": null,
> "application_fee_amount": null,
> "setup_future_usage": null,
> "created": 1680800504,
> "livemode": false
> }
> ```

---

### Chunk 145 | ID: `96e2ad47-6f4e-4884-bf09-163ded25212c`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "PaymentIntents",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> A PaymentIntent guides you through collecting a payment from a customer. Create exactly one per order or session.

---

### Chunk 146 | ID: `ce22da32-7bff-445e-9394-c8d9e804aead`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 1": "PaymentIntents",
  "Header 2": "Endpoints"
}
```

**Content:**
> | Method | Endpoint | Description |
> |--------|----------|-------------|
> | POST | `/v1/payment_intents` | Create a PaymentIntent |
> | POST | `/v1/payment_intents/:id/confirm` | Confirm a PaymentIntent |
> | GET | `/v1/payment_intents/:id` | Retrieve a PaymentIntent |
> | GET | `/v1/payment_intents` | List all PaymentIntents |
> | POST | `/v1/payment_intents/:id/cancel` | Cancel a PaymentIntent |

---

### Chunk 147 | ID: `b4ce4e47-c866-4277-b7f1-25b466719fae`

**Metadata:**
```json
{
  "Header 1": "Create a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2"
}
```

**Content:**
> **POST** `/v1/payment_intents`

---

### Chunk 148 | ID: `7b0a6813-c6d5-4e3e-a967-1a1c0e8c2f21`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Parameters",
  "Header 1": "Create a PaymentIntent",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `amount` | integer | **required** | Amount in smallest currency unit (e.g. 2000 = $20.00 USD) |
> | `currency` | enum | **required** | Three-letter ISO currency code (e.g. `usd`) |
> | `customer` | string | optional | ID of the Customer to attach this PaymentIntent to |
> | `payment_method` | string | optional | ID of the PaymentMethod to attach |
> | `payment_method_types` | array | optional | List of payment method types (e.g. `["card"]`). Defaults to `["card"]` |
> | `automatic_payment_methods.enabled` | boolean | optional | Automatically determine payment methods based on currency/customer. Recommended |
> | `capture_method` | enum | optional | `automatic` (default) charges immediately; `manual` requires a separate capture step |
> | `confirmation_method` | enum | optional | `automatic` (default) or `manual` |
> | `confirm` | boolean | optional | If `true`, confirm immediately upon creation |

---

### Chunk 149 | ID: `241b1a61-1f49-4c09-9977-96521a77c3d2`

**Metadata:**
```json
{
  "Header 1": "Create a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 2": "Parameters"
}
```

**Content:**
> | `confirm` | boolean | optional | If `true`, confirm immediately upon creation |
> | `description` | string | optional | Arbitrary description |
> | `metadata` | object | optional | Key-value pairs for storing extra info |
> | `receipt_email` | string | optional | Email to send receipt to after successful payment |
> | `statement_descriptor` | string | optional | Text on customer's bank statement (max 22 chars) |
> | `statement_descriptor_suffix` | string | optional | Suffix appended to platform's statement descriptor |
> | `on_behalf_of` | string | optional | Connected account ID on whose behalf the charge is made |
> | `transfer_data.destination` | string | optional | Connected account to transfer funds to after success |
> | `transfer_group` | string | optional | Groups related transfers together |
> | `application_fee_amount` | integer | optional | Fee in cents to collect for the platform (requires `on_behalf_of`) |

---

### Chunk 150 | ID: `a6d446e1-e0ea-4f1d-8793-310ac1708cfa`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Parameters",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "Create a PaymentIntent"
}
```

**Content:**
> | `setup_future_usage` | enum | optional | `on_session` or `off_session` — save payment method for future use |
> | `return_url` | string | optional | URL to redirect to after actions (e.g. 3D Secure) are completed |
> | `off_session` | boolean | optional | Set to `true` if the customer is not in your checkout flow (e.g. recurring billing) |

---

### Chunk 151 | ID: `77f20b9f-62e0-49ea-8c52-189e602808e0`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Returns",
  "Header 1": "Create a PaymentIntent",
  "version": "v2"
}
```

**Content:**
> Returns a PaymentIntent object. If `confirm=true`, it will attempt to confirm immediately.

---

### Chunk 152 | ID: `0f5ca286-def2-4a6f-a7c6-b026a2a3ebba`

**Metadata:**
```json
{
  "Header 1": "Create a PaymentIntent",
  "version": "v2",
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Example Request"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/payment_intents \
> -u "<<YOUR_SECRET_KEY>>" \
> -d amount=2000 \
> -d currency=usd \
> -d "automatic_payment_methods[enabled]"=true
> ```

---

### Chunk 153 | ID: `f47453ef-e0ca-462e-a18c-f9ab98229fcf`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Create a PaymentIntent",
  "Header 2": "Example Response",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> ```json
> {
> "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
> "object": "payment_intent",
> "amount": 2000,
> "currency": "usd",
> "status": "requires_payment_method",
> "customer": null,
> "payment_method": null,
> "payment_method_types": ["card", "link"],
> "capture_method": "automatic",
> "confirmation_method": "automatic",
> "amount_received": 0,
> "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
> "latest_charge": null,
> "next_action": null,
> "description": null,
> "metadata": {},
> "created": 1680800504,
> "livemode": false
> }
> ```

---

### Chunk 154 | ID: `240f0c18-9f9e-46b0-869a-7a4ac3b081d5`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 1": "Confirm a PaymentIntent"
}
```

**Content:**
> **POST** `/v1/payment_intents/:id/confirm`  
> Confirms that the customer intends to pay. Upon confirmation, the PaymentIntent will attempt to initiate a payment.  
> - If additional auth is needed (e.g. 3D Secure), status moves to `requires_action` with `next_action` populated.
> - If payment fails, status moves to `requires_payment_method`.
> - If payment succeeds, status moves to `succeeded` (or `requires_capture` if `capture_method=manual`).

---

### Chunk 155 | ID: `8768317d-e661-4e48-a967-df0b37239f16`

**Metadata:**
```json
{
  "Header 1": "Confirm a PaymentIntent",
  "version": "v2",
  "Header 2": "Parameters",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `payment_method` | string | optional | ID of the PaymentMethod to use for this confirmation |
> | `return_url` | string | optional | URL to redirect to after any required actions (e.g. 3D Secure) |
> | `capture_method` | enum | optional | Override capture method: `automatic` or `manual` |
> | `receipt_email` | string | optional | Email to send receipt to after successful payment |
> | `setup_future_usage` | enum | optional | `on_session` or `off_session` — save payment method for future use |
> | `off_session` | boolean | optional | Set `true` if customer is not present in the checkout flow |

---

### Chunk 156 | ID: `c368b9fe-be8b-4b31-bbe1-4d0baf61b08b`

**Metadata:**
```json
{
  "Header 1": "Confirm a PaymentIntent",
  "Header 2": "Returns",
  "version": "v2",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> Returns the resulting PaymentIntent after all possible transitions are applied.

---

### Chunk 157 | ID: `8a088e7a-ad51-45c0-a270-18e329afe829`

**Metadata:**
```json
{
  "Header 2": "Example Request",
  "Header 1": "Confirm a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/payment_intents/pi_3MtweELkdIwHu7ix0Dt0gF2H/confirm \
> -u "<<YOUR_SECRET_KEY>>" \
> -d payment_method=pm_card_visa \
> --data-urlencode return_url="https://www.example.com"
> ```

---

### Chunk 158 | ID: `d22fed76-530c-4ae4-b6cc-a766c8242398`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Example Response",
  "Header 1": "Confirm a PaymentIntent",
  "version": "v2"
}
```

**Content:**
> ```json
> {
> "id": "pi_3MtweELkdIwHu7ix0Dt0gF2H",
> "object": "payment_intent",
> "amount": 2000,
> "currency": "usd",
> "status": "succeeded",
> "customer": null,
> "payment_method": "pm_1MtweELkdIwHu7ixxrsejPtG",
> "payment_method_types": ["card", "link"],
> "capture_method": "automatic",
> "amount_received": 2000,
> "amount_capturable": 0,
> "client_secret": "pi_3MtweELkdIwHu7ix0Dt0gF2H_secret_ALlpPMIZse0ac8YzPxkMkFgGC",
> "latest_charge": "ch_3MtweELkdIwHu7ix05lnLAFd",
> "next_action": null,
> "description": null,
> "metadata": {},
> "created": 1680802258,
> "livemode": false
> }
> ```

---

### Chunk 159 | ID: `14946167-f9bb-4f4c-bbe4-f655f801f16d`

**Metadata:**
```json
{
  "Header 1": "Retrieve a PaymentIntent",
  "version": "v2",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> **GET** `/v1/payment_intents/:id`

---

### Chunk 160 | ID: `a02add53-2fce-422e-8c12-7021f1fa8d0f`

**Metadata:**
```json
{
  "Header 1": "Retrieve a PaymentIntent",
  "Header 2": "Parameters",
  "version": "v2",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `id` | string (path) | **required** | The ID of the PaymentIntent to retrieve |
> | `client_secret` | string | required if using publishable key | The PaymentIntent's client secret (only needed for client-side retrieval) |

---

### Chunk 161 | ID: `c87ab872-9d45-4dc5-8643-03da19bdac9c`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "Retrieve a PaymentIntent",
  "Header 2": "Returns"
}
```

**Content:**
> Returns a PaymentIntent if a valid identifier was provided.

---

### Chunk 162 | ID: `ca1d5fef-398e-446e-a394-fdf9a6015c02`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "Retrieve a PaymentIntent",
  "version": "v2",
  "Header 2": "Example Request"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \
> -u "<<YOUR_SECRET_KEY>>"
> ```

---

### Chunk 163 | ID: `9433f446-56a8-4713-b9c6-b9a4960c561f`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Retrieve a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Example Response"
}
```

**Content:**
> ```json
> {
> "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
> "object": "payment_intent",
> "amount": 2000,
> "currency": "usd",
> "status": "requires_payment_method",
> "customer": null,
> "payment_method": null,
> "payment_method_types": ["card", "link"],
> "capture_method": "automatic",
> "amount_received": 0,
> "amount_capturable": 0,
> "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
> "latest_charge": null,
> "next_action": null,
> "canceled_at": null,
> "cancellation_reason": null,
> "description": null,
> "metadata": {},
> "receipt_email": null,
> "statement_descriptor": null,
> "created": 1680800504,
> "livemode": false
> }
> ```

---

### Chunk 164 | ID: `d85daf6e-c36a-410e-adb6-eb652ef167ae`

**Metadata:**
```json
{
  "Header 1": "List All PaymentIntents",
  "version": "v2",
  "api_class": "PAYMENT_INTENTS"
}
```

**Content:**
> **GET** `/v1/payment_intents`

---

### Chunk 165 | ID: `fa584a39-c1cb-4a32-8675-938211c94389`

**Metadata:**
```json
{
  "Header 1": "List All PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Parameters",
  "version": "v2"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `customer` | string | optional | Only return PaymentIntents for this customer ID |
> | `limit` | integer | optional | Number of results to return (1–100, default 10) |
> | `starting_after` | string | optional | PaymentIntent ID cursor — fetch the next page after this ID |
> | `ending_before` | string | optional | PaymentIntent ID cursor — fetch the previous page before this ID |
> | `created.gt` | integer | optional | Return PaymentIntents created after this Unix timestamp (exclusive) |
> | `created.gte` | integer | optional | Return PaymentIntents created at or after this Unix timestamp (inclusive) |
> | `created.lt` | integer | optional | Return PaymentIntents created before this Unix timestamp (exclusive) |
> | `created.lte` | integer | optional | Return PaymentIntents created at or before this Unix timestamp (inclusive) |

---

### Chunk 166 | ID: `6389f70e-86ed-49d9-9b1c-83cccc46398b`

**Metadata:**
```json
{
  "Header 1": "List All PaymentIntents",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 2": "Returns"
}
```

**Content:**
> A dictionary with a `data` array of PaymentIntent objects. Includes `has_more` for pagination.

---

### Chunk 167 | ID: `92d56b2f-c211-4b6f-84ac-b7ce98216f87`

**Metadata:**
```json
{
  "Header 1": "List All PaymentIntents",
  "Header 2": "Example Request",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2"
}
```

**Content:**
> ```curl
> curl -G https://api.stripe.com/v1/payment_intents \
> -u "<<YOUR_SECRET_KEY>>" \
> -d limit=3
> ```

---

### Chunk 168 | ID: `bab2d7a3-9a3c-49f7-a2ab-f1d5a17b384c`

**Metadata:**
```json
{
  "Header 2": "Example Response",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "List All PaymentIntents",
  "version": "v2"
}
```

**Content:**
> ```json
> {
> "object": "list",
> "url": "/v1/payment_intents",
> "has_more": false,
> "data": [
> {
> "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
> "object": "payment_intent",
> "amount": 2000,
> "currency": "usd",
> "status": "requires_payment_method",
> "customer": null,
> "payment_method": null,
> "payment_method_types": ["card", "link"],
> "capture_method": "automatic",
> "amount_received": 0,
> "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
> "latest_charge": null,
> "description": null,
> "metadata": {},
> "created": 1680800504,
> "livemode": false
> }
> ]
> }
> ```

---

### Chunk 169 | ID: `23279d6d-7fc3-454e-a4f0-a2953559dc2e`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "PAYMENT_INTENTS",
  "Header 1": "Cancel a PaymentIntent"
}
```

**Content:**
> **POST** `/v1/payment_intents/:id/cancel`  
> Cancels a PaymentIntent. Cancelable when status is: `requires_payment_method`, `requires_capture`, `requires_confirmation`, `requires_action`, or (rarely) `processing`.  
> After cancellation, no further charges are made. For PaymentIntents with status `requires_capture`, the remaining `amount_capturable` is automatically refunded.

---

### Chunk 170 | ID: `4d3156f2-8cc0-422b-8e56-8ca7873c6c2d`

**Metadata:**
```json
{
  "Header 1": "Cancel a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 2": "Parameters"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `id` | string (path) | **required** | The ID of the PaymentIntent to cancel |
> | `cancellation_reason` | string | optional | Reason for canceling: `duplicate`, `fraudulent`, `requested_by_customer`, or `abandoned` |

---

### Chunk 171 | ID: `5dc2db21-b9e6-423b-8701-a1af1f448b32`

**Metadata:**
```json
{
  "Header 1": "Cancel a PaymentIntent",
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 2": "Returns"
}
```

**Content:**
> Returns the canceled PaymentIntent object. Returns an error if already canceled or not in a cancelable state.

---

### Chunk 172 | ID: `176fbb4d-abac-4d2d-a44f-d6dc3af1f82f`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "version": "v2",
  "Header 1": "Cancel a PaymentIntent",
  "Header 2": "Example Request"
}
```

**Content:**
> ```curl
> curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/cancel \
> -u "<<YOUR_SECRET_KEY>>"
> ```

---

### Chunk 173 | ID: `6e14fea4-5d9f-42e2-8e84-9e836050f990`

**Metadata:**
```json
{
  "api_class": "PAYMENT_INTENTS",
  "Header 2": "Example Response",
  "version": "v2",
  "Header 1": "Cancel a PaymentIntent"
}
```

**Content:**
> ```json
> {
> "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
> "object": "payment_intent",
> "amount": 2000,
> "currency": "usd",
> "status": "canceled",
> "customer": null,
> "payment_method": null,
> "payment_method_types": ["card", "link"],
> "capture_method": "automatic",
> "amount_received": 0,
> "amount_capturable": 0,
> "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
> "canceled_at": 1680801569,
> "cancellation_reason": null,
> "latest_charge": null,
> "description": null,
> "metadata": {},
> "created": 1680800504,
> "livemode": false
> }
> ```

---

### Chunk 174 | ID: `c97cc6d7-7bd6-453e-9e9a-7423c4966bff`

**Metadata:**
```json
{
  "version": "v1",
  "api_class": "PRICES",
  "Header 1": "Prices"
}
```

**Content:**
> ======
> Prices
> 
> Prices define the unit cost, currency, and (optional) billing cycle for products.

---

### Chunk 175 | ID: `8b35be41-a2a8-4554-babe-7ed2b2b1d543`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "version": "v1",
  "Header 2": "The Price Object",
  "api_class": "PRICES"
}
```

**Content:**
> The Price Object
> 
> * **id** (string): Unique identifier for the object.
> * **object** (string): Always has the value ``price``.
> * **is_active** (boolean): Whether the price can be used for new purchases.
> * **currency_code** (enum): Three-letter ISO currency code.
> * **product_reference_id** (string): The ID of the product this price is associated with.
> * **billing_cycle** (object, nullable): The recurring components of a price.
> * **price_in_cents** (integer, nullable): The unit amount in cents to be charged.

---

### Chunk 176 | ID: `824546fd-cf85-4344-ba58-ebede693512a`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "Header 2": "Endpoints",
  "api_class": "PRICES",
  "version": "v1"
}
```

**Content:**
> Endpoints

---

### Chunk 177 | ID: `664163be-d1ec-4812-956f-7f01ef3ee501`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "Header 2": "Create a price",
  "version": "v1",
  "api_class": "PRICES"
}
```

**Content:**
> Create a price
> **POST /api/v1.0/prices**
> 
> **Parameters:**
> 
> * **currency_code** (enum, required): Three-letter ISO currency code.
> * **price_in_cents** (integer, required): A positive integer in cents.
> * **product_reference_id** (string, required): The ID of the Product that this Price will belong to.
> * **billing_cycle** (object, optional): The recurring components of a price.

---

### Chunk 178 | ID: `88e2e65a-02a1-4d47-a454-6d1d6a04ced4`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "Header 2": "Retrieve a price",
  "version": "v1",
  "api_class": "PRICES"
}
```

**Content:**
> Retrieve a price
> **GET /api/v1.0/prices/:id**
> 
> **Example Response:**
> 
> .. code-block:: json
> 
>    {
>      "status": "success",
>      "api_version": "1.0",
>      "data": {
>        "id": "price_12345",
>        "object": "price",
>        "is_active": true,
>        "currency_code": "usd",
>        "price_in_cents": 1000,
>        "product_reference_id": "prod_12345",
>        "billing_cycle": null
>      }
>    }

---

### Chunk 179 | ID: `622fe3b5-043d-42a2-9166-1e9e3c389b85`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "version": "v1",
  "Header 2": "List all prices",
  "api_class": "PRICES"
}
```

**Content:**
> List all prices
> **GET /api/v1.0/prices**
> 
> **Parameters:**
> 
> * **is_active** (boolean, optional): Only return prices that are active or inactive.
> * **product_reference_id** (string, optional): Only return prices for the given product.
> * **max_results** (integer, optional): A limit on the number of objects to be returned.

---

### Chunk 180 | ID: `d61168f5-1a7c-4a7b-842c-447e4256385f`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "PRICES",
  "Header 1": "Prices"
}
```

**Content:**
> Prices define the unit cost, currency, and (optional) billing cycle for both recurring and one-time purchases of products. Different physical goods or levels of service should be represented by products, and pricing options should be represented by prices.

---

### Chunk 181 | ID: `dcebd28b-8282-4523-8934-0cc7195cbd50`

**Metadata:**
```json
{
  "api_class": "PRICES",
  "Header 1": "Prices",
  "Header 2": "The Price Object",
  "version": "v2"
}
```

**Content:**
> - `id` (string): Unique identifier for the object.
> - `object` (string): String representing the object’s type. Always has the value `price`.
> - `active` (boolean): Whether the price can be used for new purchases.
> - `created` (timestamp): Time at which the object was created.
> - `currency` (enum): Three-letter ISO currency code, in lowercase.
> - `lookup_key` (string, nullable): A lookup key used to retrieve prices dynamically from a static string.
> - `metadata` (object): Set of key-value pairs that you can attach to an object.
> - `product` (string): The ID of the product this price is associated with.
> - `recurring` (object, nullable): The recurring components of a price such as `interval` and `usage_type`.
> - `recurring.interval` (enum): The frequency at which a subscription is billed. One of `day`, `week`, `month` or `year`.
> - `recurring.interval_count` (integer): The number of intervals between subscription billings.

---

### Chunk 182 | ID: `f67d9a37-e0ba-497d-b61f-7547a1aa5692`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "The Price Object",
  "api_class": "PRICES",
  "Header 1": "Prices"
}
```

**Content:**
> - `recurring.interval_count` (integer): The number of intervals between subscription billings.
> - `type` (enum): One of `one_time` or `recurring` depending on whether the price is for a one-time purchase or a recurring (subscription) purchase.
> - `unit_amount` (integer, nullable): The unit amount in cents to be charged.

---

### Chunk 183 | ID: `4a95aeea-8030-4ac8-a396-fb1165bcf323`

**Metadata:**
```json
{
  "Header 2": "Endpoints",
  "Header 1": "Prices",
  "api_class": "PRICES",
  "Header 3": "Create a price",
  "version": "v2"
}
```

**Content:**
> **POST /v1/prices**  
> Creates a new Price for an existing Product. The Price can be recurring or one-time.  
> **Parameters:**  
> - `currency` (enum, required): Three-letter ISO currency code, in lowercase.
> - `unit_amount` (integer, required conditionally): A positive integer in cents (or 0 for a free price) representing how much to charge.
> - `product` (string, required unless product_data is provided): The ID of the Product that this Price will belong to.
> - `product_data` (object, required unless product is provided): These fields can be used to create a new product that this price will belong to.
> - `product_data.name` (string, required): The product’s name, meant to be displayable to the customer.
> - `recurring` (object, optional): The recurring components of a price such as `interval` and `usage_type`.
> - `recurring.interval` (enum, required): Specifies billing frequency. Either `day`, `week`, `month` or `year`.

---

### Chunk 184 | ID: `479bf13c-c4fa-4575-93cb-8f7851414a9e`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "Header 3": "Create a price",
  "Header 2": "Endpoints",
  "version": "v2",
  "api_class": "PRICES"
}
```

**Content:**
> - `active` (boolean, optional): Whether the price can be used for new purchases.
> - `lookup_key` (string, optional): A lookup key used to retrieve prices dynamically from a static string.
> - `metadata` (object, optional): Set of key-value pairs that you can attach to an object.

---

### Chunk 185 | ID: `76725a1f-7bc9-41c8-98e8-b24232de2015`

**Metadata:**
```json
{
  "Header 2": "Endpoints",
  "Header 1": "Prices",
  "version": "v2",
  "Header 3": "Retrieve a price",
  "api_class": "PRICES"
}
```

**Content:**
> **GET /v1/prices/:id**  
> Retrieves the price with the given ID.

---

### Chunk 186 | ID: `9b26bff7-cbc5-4b11-9d80-cc66f7f11aab`

**Metadata:**
```json
{
  "Header 1": "Prices",
  "Header 2": "Endpoints",
  "api_class": "PRICES",
  "version": "v2",
  "Header 3": "List all prices"
}
```

**Content:**
> **GET /v1/prices**  
> Returns a list of your active prices.  
> **Parameters:**  
> - `active` (boolean, optional): Only return prices that are active or inactive (e.g., pass `false` to list all inactive prices).
> - `currency` (enum, optional): Only return prices for the given currency.
> - `product` (string, optional): Only return prices for the given product.
> - `type` (enum, optional): Only return prices of type `recurring` or `one_time`.
> - `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100.
> - `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
> - `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.

---

### Chunk 187 | ID: `59d1fd02-8226-4656-b21a-2f59ec08f582`

**Metadata:**
```json
{
  "Header 1": "Products",
  "api_class": "PRODUCTS",
  "version": "v1"
}
```

**Content:**
> ========
> Products
> 
> Products describe the specific goods or services you offer to your customers.

---

### Chunk 188 | ID: `84a96213-0154-4a85-ab92-e650942ff081`

**Metadata:**
```json
{
  "Header 1": "Products",
  "Header 2": "The Product Object",
  "version": "v1",
  "api_class": "PRODUCTS"
}
```

**Content:**
> The Product Object
> 
> * **id** (string): Unique identifier for the object.
> * **object** (string): Always has the value ``product``.
> * **is_active** (boolean): Whether the product is currently available for purchase.
> * **created_at** (timestamp): Time at which the object was created.
> * **product_name** (string): The product’s name.
> * **description_text** (string, nullable): The product’s description.

---

### Chunk 189 | ID: `22854c26-0e00-430d-84bb-cea3053039be`

**Metadata:**
```json
{
  "Header 1": "Products",
  "api_class": "PRODUCTS",
  "Header 2": "Endpoints",
  "version": "v1"
}
```

**Content:**
> Endpoints

---

### Chunk 190 | ID: `a2e4d178-3a80-46b6-8362-27ee587dc0e5`

**Metadata:**
```json
{
  "Header 2": "Create a product",
  "api_class": "PRODUCTS",
  "Header 1": "Products",
  "version": "v1"
}
```

**Content:**
> Create a product
> **POST /api/v1.0/products**
> 
> **Parameters:**
> 
> * **product_name** (string, required): The product’s name.
> * **is_active** (boolean, optional): Whether the product is currently available. Defaults to ``true``.
> * **description_text** (string, optional): The product’s description.

---

### Chunk 191 | ID: `16095d1e-a79e-44cb-862f-684df13940aa`

**Metadata:**
```json
{
  "Header 2": "Retrieve a product",
  "api_class": "PRODUCTS",
  "Header 1": "Products",
  "version": "v1"
}
```

**Content:**
> Retrieve a product
> **GET /api/v1.0/products/:id**
> 
> **Example Response:**
> 
> .. code-block:: json
> 
>    {
>      "status": "success",
>      "api_version": "1.0",
>      "data": {
>        "id": "prod_12345",
>        "object": "product",
>        "is_active": true,
>        "product_name": "Gold Plan",
>        "description_text": "Premium access"
>      }
>    }

---

### Chunk 192 | ID: `93cfd12e-b90e-48bf-b813-9f27b9b36756`

**Metadata:**
```json
{
  "Header 1": "Products",
  "api_class": "PRODUCTS",
  "Header 2": "List all products",
  "version": "v1"
}
```

**Content:**
> List all products
> **GET /api/v1.0/products**
> 
> **Parameters:**
> 
> * **is_active** (boolean, optional): Only return products that are active or inactive.
> * **max_results** (integer, optional): A limit on the number of objects to be returned.
> * **page_cursor** (string, optional): A cursor for use in pagination.

---

### Chunk 193 | ID: `bc708d08-fee7-4008-bcaa-1ec2e0aaf211`

**Metadata:**
```json
{
  "Header 1": "Products",
  "version": "v2",
  "api_class": "PRODUCTS"
}
```

**Content:**
> Products describe the specific goods or services you offer to your customers. They can be used in conjunction with Prices to configure pricing in Payment Links, Checkout, and Subscriptions.

---

### Chunk 194 | ID: `62f0e55e-a5b0-4c07-acc8-4561af335efb`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Products",
  "Header 2": "The Product Object",
  "api_class": "PRODUCTS"
}
```

**Content:**
> - `id` (string): Unique identifier for the object.
> - `object` (string): String representing the object’s type. Always has the value `product`.
> - `active` (boolean): Whether the product is currently available for purchase.
> - `created` (timestamp): Time at which the object was created. Measured in seconds since the Unix epoch.
> - `default_price` (string, nullable): The ID of the Price object that is the default price for this product.
> - `description` (string, nullable): The product’s description, meant to be displayable to the customer.
> - `livemode` (boolean): If the object exists in live mode, the value is `true`. If the object exists in test mode, the value is `false`.
> - `metadata` (object): Set of key-value pairs that you can attach to an object.
> - `name` (string): The product’s name, meant to be displayable to the customer.
> - `shippable` (boolean, nullable): Whether this product is shipped (i.e., physical goods).

---

### Chunk 195 | ID: `cb54c6fa-6d2f-409a-8520-2f7f272d2efc`

**Metadata:**
```json
{
  "api_class": "PRODUCTS",
  "Header 1": "Products",
  "Header 2": "The Product Object",
  "version": "v2"
}
```

**Content:**
> - `shippable` (boolean, nullable): Whether this product is shipped (i.e., physical goods).
> - `statement_descriptor` (string, nullable): Extra information about a product which will appear on your customer’s credit card statement. Only used for subscription payments.
> - `updated` (timestamp): Time at which the object was last updated.

---

### Chunk 196 | ID: `0ff0b0d0-2a5c-4dca-a8fb-c5ebf6838447`

**Metadata:**
```json
{
  "Header 3": "Create a product",
  "version": "v2",
  "Header 2": "Endpoints",
  "Header 1": "Products",
  "api_class": "PRODUCTS"
}
```

**Content:**
> **POST /v1/products**  
> Creates a new product object.  
> **Parameters:**  
> - `name` (string, required): The product’s name, meant to be displayable to the customer.
> - `active` (boolean, optional): Whether the product is currently available for purchase. Defaults to `true`.
> - `description` (string, optional): The product’s description, meant to be displayable to the customer.
> - `default_price_data` (object, optional): Data used to generate a new Price object. This Price will be set as the default price for this product.
> - `default_price_data.currency` (enum, required): Three-letter ISO currency code, in lowercase.
> - `default_price_data.unit_amount` (integer, required conditionally): A positive integer in cents (or 0 for a free price) representing how much to charge.
> - `default_price_data.recurring` (object, optional): The recurring components of a price such as `interval` and `interval_count`.

---

### Chunk 197 | ID: `3c776955-17c8-4ad6-8132-c3ad9e9e83a0`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Endpoints",
  "Header 3": "Create a product",
  "api_class": "PRODUCTS",
  "Header 1": "Products"
}
```

**Content:**
> - `default_price_data.recurring.interval` (enum, required): Specifies billing frequency. Either `day`, `week`, `month` or `year`.
> - `metadata` (object, optional): Set of key-value pairs that you can attach to an object.
> - `shippable` (boolean, optional): Whether this product is shipped (i.e., physical goods).
> - `statement_descriptor` (string, optional): An arbitrary string to be displayed on your customer’s credit card or bank statement. Only used for subscription payments.

---

### Chunk 198 | ID: `7da868c1-003e-4b6d-b0aa-dcc91ee7a21b`

**Metadata:**
```json
{
  "Header 3": "Retrieve a product",
  "Header 2": "Endpoints",
  "version": "v2",
  "Header 1": "Products",
  "api_class": "PRODUCTS"
}
```

**Content:**
> **GET /v1/products/:id**  
> Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.

---

### Chunk 199 | ID: `3355d255-f432-42ce-b3dc-b0550234d8cd`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Endpoints",
  "api_class": "PRODUCTS",
  "Header 3": "List all products",
  "Header 1": "Products"
}
```

**Content:**
> **GET /v1/products**  
> Returns a list of your products. The products are returned sorted by creation date, with the most recently created products appearing first.  
> **Parameters:**  
> - `active` (boolean, optional): Only return products that are active or inactive (e.g., pass `false` to list all inactive products).
> - `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
> - `ids` (array of strings, optional): Only return products with the given IDs.
> - `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
> - `shippable` (boolean, optional): Only return products that can be shipped (i.e., physical, not digital products).
> - `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.

---

### Chunk 200 | ID: `b3878029-11ba-4641-a218-0d092d75fe24`

**Metadata:**
```json
{
  "version": "v1",
  "api_class": "REFUNDS",
  "Header 1": "Refunds"
}
```

**Content:**
> =======
> Refunds
> 
> Refund objects allow you to refund a previously created charge that isn’t refunded yet.

---

### Chunk 201 | ID: `fd22de82-b888-4f56-ab7a-a7130d6d8935`

**Metadata:**
```json
{
  "Header 2": "The Refund Object",
  "api_class": "REFUNDS",
  "Header 1": "Refunds",
  "version": "v1"
}
```

**Content:**
> The Refund Object
> 
> * **id** (string): Unique identifier for the object.
> * **object** (string): Always has the value ``refund``.
> * **refund_amount_cents** (integer): Amount, in cents.
> * **charge_id** (string, nullable): ID of the charge that’s refunded.
> * **transaction_id** (string, nullable): ID of the PaymentIntent that’s refunded.
> * **refund_reason** (enum, nullable): Reason for the refund (``duplicate``, ``fraudulent``, ``requested_by_customer``).
> * **refund_status** (string, nullable): Status of the refund (``pending``, ``succeeded``, ``failed``).

---

### Chunk 202 | ID: `e93029e3-de29-4eb6-80e3-8e744f7ef82c`

**Metadata:**
```json
{
  "Header 2": "Endpoints",
  "version": "v1",
  "Header 1": "Refunds",
  "api_class": "REFUNDS"
}
```

**Content:**
> Endpoints

---

### Chunk 203 | ID: `131653dd-1144-41bc-aaab-1f719814f364`

**Metadata:**
```json
{
  "Header 1": "Refunds",
  "version": "v1",
  "Header 2": "Create a refund",
  "api_class": "REFUNDS"
}
```

**Content:**
> Create a refund
> **POST /api/v1.0/refunds**
> 
> **Parameters:**
> 
> * **charge_id** (string, optional): The identifier of the charge to refund.
> * **transaction_id** (string, optional): The identifier of the PaymentIntent to refund.
> * **refund_amount_cents** (integer, optional): A positive integer representing how much of this charge to refund.
> * **refund_reason** (string, optional): String indicating the reason for the refund.

---

### Chunk 204 | ID: `161c480d-14cd-4cd5-b73a-ecdd228ea7d0`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Refunds",
  "Header 2": "Retrieve a refund",
  "api_class": "REFUNDS"
}
```

**Content:**
> Retrieve a refund
> **GET /api/v1.0/refunds/:id**
> 
> **Example Response:**
> 
> .. code-block:: json
> 
>    {
>      "status": "success",
>      "api_version": "1.0",
>      "data": {
>        "id": "re_12345",
>        "object": "refund",
>        "refund_amount_cents": 1000,
>        "charge_id": "ch_9876",
>        "transaction_id": null,
>        "refund_status": "succeeded"
>      }
>    }

---

### Chunk 205 | ID: `fa6e2904-fea6-444a-8499-288fbeb6ad6c`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "List all refunds",
  "Header 1": "Refunds",
  "api_class": "REFUNDS"
}
```

**Content:**
> List all refunds
> **GET /api/v1.0/refunds**
> 
> **Parameters:**
> 
> * **charge_id** (string, optional): Only return refunds for the charge specified by this charge ID.
> * **transaction_id** (string, optional): Only return refunds for the PaymentIntent specified by this ID.
> * **max_results** (integer, optional): A limit on the number of objects to be returned.

---

### Chunk 206 | ID: `419c2b51-eddb-46c8-aea1-3417560eda7b`

**Metadata:**
```json
{
  "Header 1": "Refunds",
  "version": "v2",
  "api_class": "REFUNDS"
}
```

**Content:**
> Refund objects allow you to refund a previously created charge that isn’t refunded yet. Funds are refunded to the credit or debit card that’s initially charged.

---

### Chunk 207 | ID: `2895cd28-9d0d-4f09-94e3-f29c452fee42`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Refunds",
  "Header 2": "The Refund Object",
  "api_class": "REFUNDS"
}
```

**Content:**
> - `id` (string): Unique identifier for the object.
> - `object` (string): String representing the object’s type. Objects of the same type share the same value. Always has the value `refund`.
> - `amount` (integer): Amount, in cents.
> - `balance_transaction` (string, nullable): Balance transaction that describes the impact on your account balance.
> - `charge` (string, nullable): ID of the charge that’s refunded.
> - `created` (timestamp): Time at which the object was created. Measured in seconds since the Unix epoch.
> - `currency` (enum): Three-letter ISO currency code, in lowercase.
> - `metadata` (object, nullable): Set of key-value pairs that you can attach to an object.
> - `payment_intent` (string, nullable): ID of the PaymentIntent that’s refunded.
> - `reason` (enum, nullable): Reason for the refund, which is either user-provided (`duplicate`, `fraudulent`, or `requested_by_customer`) or generated by Stripe internally (`expired_uncaptured_charge`).

---

### Chunk 208 | ID: `b6b82286-67c7-46b3-8e4f-4c542354920a`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "The Refund Object",
  "Header 1": "Refunds",
  "api_class": "REFUNDS"
}
```

**Content:**
> - `status` (string, nullable): Status of the refund. This can be `pending`, `requires_action`, `succeeded`, `failed`, or `canceled`.

---

### Chunk 209 | ID: `d7d70f24-2645-4b9d-82de-ffbcd6afaadd`

**Metadata:**
```json
{
  "Header 3": "Create a refund",
  "version": "v2",
  "Header 1": "Refunds",
  "Header 2": "Endpoints",
  "api_class": "REFUNDS"
}
```

**Content:**
> **POST /v1/refunds**  
> When you create a new refund, you must specify a Charge or a PaymentIntent object on which to create it. You can optionally refund only part of a charge. You can do so multiple times, until the entire charge has been refunded.  
> **Parameters:**  
> - `charge` (string, optional): The identifier of the charge to refund.
> - `payment_intent` (string, optional): The identifier of the PaymentIntent to refund.
> - `amount` (integer, optional): A positive integer in the smallest currency unit representing how much of this charge to refund. Can refund only up to the remaining, unrefunded amount of the charge.
> - `reason` (string, optional): String indicating the reason for the refund. If set, possible values are `duplicate`, `fraudulent`, and `requested_by_customer`.
> - `metadata` (object, optional): Set of key-value pairs that you can attach to an object.

---

### Chunk 210 | ID: `314e389d-82ee-4eb8-8f41-2025220dcdf5`

**Metadata:**
```json
{
  "Header 3": "Retrieve a refund",
  "Header 1": "Refunds",
  "version": "v2",
  "api_class": "REFUNDS",
  "Header 2": "Endpoints"
}
```

**Content:**
> **GET /v1/refunds/:id**  
> Retrieves the details of an existing refund.

---

### Chunk 211 | ID: `0697e940-e1b7-47a2-a925-263893ee0715`

**Metadata:**
```json
{
  "Header 1": "Refunds",
  "Header 3": "List all refunds",
  "Header 2": "Endpoints",
  "api_class": "REFUNDS",
  "version": "v2"
}
```

**Content:**
> **GET /v1/refunds**  
> Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first.  
> **Parameters:**  
> - `charge` (string, optional): Only return refunds for the charge specified by this charge ID.
> - `payment_intent` (string, optional): Only return refunds for the PaymentIntent specified by this ID.
> - `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
> - `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
> - `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.

---

### Chunk 212 | ID: `6f731038-c950-4a69-82f9-785d081c8101`

**Metadata:**
```json
{
  "version": "v1",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions"
}
```

**Content:**
> Subscriptions
> 
> Subscriptions allow you to charge a customer on a recurring basis.
> 
> .. note::
> 
>    In v1, subscriptions use ``plan`` instead of ``price`` to reference recurring billing configurations. The ``pause_collection`` feature is not available. ``default_payment_method`` is replaced by ``default_source``.

---

### Chunk 213 | ID: `70e01ad8-4994-43ba-86fb-5994e4765d6d`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 2": "Endpoints",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Endpoints
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 15 45 40
> 
>    * - Method
>      - Endpoint
>      - Description
>    * - POST
>      - ``/v1/subscriptions``
>      - Create a subscription
>    * - POST
>      - ``/v1/subscriptions/:id``
>      - Update a subscription
>    * - GET
>      - ``/v1/subscriptions/:id``
>      - Retrieve a subscription
>    * - GET
>      - ``/v1/subscriptions``
>      - List all subscriptions
>    * - DELETE
>      - ``/v1/subscriptions/:id``
>      - Cancel a subscription
>    * - POST
>      - ``/v1/subscriptions/:id/resume``
>      - Resume a paused subscription

---

### Chunk 214 | ID: `c23cbc04-0016-4563-8c42-1af01ad42700`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 2": "The Subscription Object"
}
```

**Content:**
> The Subscription Object

---

### Chunk 215 | ID: `cbffaf4b-fd65-434e-9c5a-9a24e7b488d8`

**Metadata:**
```json
{
  "Header 3": "Status Lifecycle",
  "Header 1": "Subscriptions",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "The Subscription Object"
}
```

**Content:**
> Status Lifecycle
> 
> ``trialing`` → ``active`` → ``past_due`` → ``canceled`` / ``unpaid``

---

### Chunk 216 | ID: `ca96a4cd-5fd2-46f5-a88b-af4d46cb8b7a`

**Metadata:**
```json
{
  "Header 3": "Key Fields",
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 2": "The Subscription Object",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Key Fields
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 45

---

### Chunk 217 | ID: `91b9626b-5ded-4e81-bec7-b644c46f283f`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "Header 3": "Key Fields",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 2": "The Subscription Object"
}
```

**Content:**
> * - Field
>      - Type
>      - Description
>    * - ``id``
>      - string
>      - Unique identifier (e.g. ``sub_1MowQVLkdIwHu7ixeRlqHVzs``)
>    * - ``object``
>      - string
>      - Always ``"subscription"``
>    * - ``customer``
>      - string
>      - ID of the Customer being billed
>    * - ``status``
>      - enum
>      - ``trialing``, ``active``, ``past_due``, ``canceled``, or ``unpaid``
>    * - ``items.data``
>      - array
>      - List of subscription items, each with a ``plan`` and ``quantity``
>    * - ``items.data[].plan.id``
>      - string
>      - ID of the Plan for this item
>    * - ``items.data[].plan.amount``
>      - integer
>      - Plan amount in smallest currency unit
>    * - ``items.data[].plan.interval``
>      - string
>      - Billing interval: ``day``, ``week``, ``month``, or ``year``
>    * - ``items.data[].quantity``
>      - integer
>      - Quantity of the plan
>    * - ``currency``
>      - string
>      - Three-letter ISO currency code
>    * - ``collection_method``
>      - enum

---

### Chunk 218 | ID: `df5ab27e-9679-44c5-9356-591a7963ddc0`

**Metadata:**
```json
{
  "Header 3": "Key Fields",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "The Subscription Object",
  "Header 1": "Subscriptions"
}
```

**Content:**
> - string
>      - Three-letter ISO currency code
>    * - ``collection_method``
>      - enum
>      - ``charge_automatically`` or ``send_invoice``
>    * - ``default_source``
>      - string
>      - ID of default Source for this subscription
>    * - ``latest_invoice``
>      - string
>      - ID of the most recent invoice
>    * - ``billing_cycle_anchor``
>      - timestamp
>      - Reference point for billing cycle
>    * - ``current_period_start``
>      - timestamp
>      - Start of the current billing period
>    * - ``current_period_end``
>      - timestamp
>      - End of the current billing period
>    * - ``cancel_at_period_end``
>      - boolean
>      - If ``true``, cancels at end of current period
>    * - ``cancel_at``
>      - timestamp
>      - Scheduled cancellation timestamp
>    * - ``canceled_at``
>      - timestamp
>      - When the subscription was canceled
>    * - ``ended_at``
>      - timestamp
>      - When the subscription ended
>    * - ``start_date``
>      - timestamp
>      - When the subscription started

---

### Chunk 219 | ID: `2fa7dd16-5f61-4a5b-81c8-0db8452adfb3`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "The Subscription Object",
  "Header 3": "Key Fields"
}
```

**Content:**
> * - ``start_date``
>      - timestamp
>      - When the subscription started
>    * - ``trial_start``
>      - timestamp
>      - Start of trial period
>    * - ``trial_end``
>      - timestamp
>      - End of trial period
>    * - ``description``
>      - string
>      - Arbitrary description
>    * - ``metadata``
>      - object
>      - Key-value pairs for storing extra info
>    * - ``on_behalf_of``
>      - string
>      - Connected account ID on whose behalf charges are made
>    * - ``transfer_data.destination``
>      - string
>      - Connected account to transfer funds to
>    * - ``application_fee_percent``
>      - float
>      - Percentage of subscription amount to collect for the platform
>    * - ``created``
>      - timestamp
>      - Unix timestamp of creation
>    * - ``livemode``
>      - boolean
>      - True if live mode, false if test mode

---

### Chunk 220 | ID: `d72ba715-e185-4803-b27b-e2f3343b6cbb`

**Metadata:**
```json
{
  "Header 3": "Example Object",
  "Header 2": "The Subscription Object",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "version": "v1"
}
```

**Content:**
> Example Object
> 
> .. code-block:: json

---

### Chunk 221 | ID: `8fac984c-3132-4022-bdca-934a7dd26df4`

**Metadata:**
```json
{
  "Header 2": "The Subscription Object",
  "Header 3": "Example Object",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 1": "Subscriptions"
}
```

**Content:**
> {
>      "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
>      "object": "subscription",
>      "customer": "cus_Na6dX7aXxi11N4",
>      "status": "active",
>      "currency": "usd",
>      "collection_method": "charge_automatically",
>      "default_source": null,
>      "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
>      "billing_cycle_anchor": 1679609767,
>      "start_date": 1679609767,
>      "cancel_at_period_end": false,
>      "cancel_at": null,
>      "canceled_at": null,
>      "ended_at": null,
>      "trial_start": null,
>      "trial_end": null,
>      "description": null,
>      "metadata": {},
>      "on_behalf_of": null,
>      "transfer_data": null,
>      "created": 1679609767,
>      "livemode": false,
>      "items": {
>        "object": "list",
>        "data": [
>          {
>            "id": "si_Na6dzxczY5fwHx",
>            "object": "subscription_item",
>            "quantity": 1,
>            "plan": {
>              "id": "plan_Na6dGcTsmU0I4R",
>              "object": "plan",
>              "currency": "usd",

---

### Chunk 222 | ID: `a85754db-a766-4942-994c-79be9d011e03`

**Metadata:**
```json
{
  "Header 3": "Example Object",
  "Header 2": "The Subscription Object",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "version": "v1"
}
```

**Content:**
> "object": "plan",
>              "currency": "usd",
>              "amount": 1000,
>              "interval": "month",
>              "interval_count": 1,
>              "product": "prod_Na6dGcTsmU0I4R",
>              "active": true
>            }
>          }
>        ],
>        "has_more": false
>      }
>    }

---

### Chunk 223 | ID: `efb5d264-3e83-4b9f-8587-3b8b032cc6c7`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions"
}
```

**Content:**
> Create a Subscription
> 
> **POST** ``/v1/subscriptions``

---

### Chunk 224 | ID: `6115229b-410f-4c33-8a43-f6072ce0d149`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 3": "Parameters",
  "Header 2": "Create a Subscription"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 15 30

---

### Chunk 225 | ID: `cef0ea87-f110-4c33-94b9-c9c65e06b820`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "version": "v1",
  "Header 2": "Create a Subscription",
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``customer``
>      - string
>      - **required**
>      - ID of the Customer to subscribe
>    * - ``items``
>      - array
>      - **required**
>      - List of items. Each item needs a ``plan`` (Plan ID) and optional ``quantity`` (default 1)
>    * - ``items[].plan``
>      - string
>      - required per item
>      - ID of the Plan to subscribe to
>    * - ``items[].quantity``
>      - integer
>      - optional
>      - Quantity for this plan (default 1)
>    * - ``currency``
>      - enum
>      - optional
>      - Three-letter ISO currency code. Defaults to the plan's currency
>    * - ``default_source``
>      - string
>      - optional
>      - ID of default Source for this subscription
>    * - ``collection_method``
>      - enum
>      - optional
>      - ``charge_automatically`` (default) or ``send_invoice``
>    * - ``days_until_due``
>      - integer
>      - optional
>      - Days until invoice is due (required when ``collection_method=send_invoice``)

---

### Chunk 226 | ID: `b00e5d01-b9fd-4c28-b6e3-0448894b0cf7`

**Metadata:**
```json
{
  "Header 2": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 3": "Parameters",
  "Header 1": "Subscriptions"
}
```

**Content:**
> - optional
>      - Days until invoice is due (required when ``collection_method=send_invoice``)
>    * - ``proration_behavior``
>      - enum
>      - optional
>      - ``create_prorations`` (default), ``none``, or ``always_invoice``
>    * - ``billing_cycle_anchor``
>      - timestamp
>      - optional
>      - Sets the billing cycle anchor to a specific Unix timestamp
>    * - ``cancel_at_period_end``
>      - boolean
>      - optional
>      - If ``true``, cancels at end of current period
>    * - ``cancel_at``
>      - timestamp
>      - optional
>      - Schedules cancellation at this Unix timestamp
>    * - ``trial_period_days``
>      - integer
>      - optional
>      - Number of trial days before billing starts
>    * - ``trial_end``
>      - timestamp or ``now``
>      - optional
>      - Ends trial at this Unix timestamp
>    * - ``description``
>      - string
>      - optional
>      - Arbitrary description
>    * - ``metadata``
>      - object
>      - optional
>      - Key-value pairs for storing extra info

---

### Chunk 227 | ID: `16c037e8-e56b-4f45-8918-c59b43f8afc5`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Create a Subscription",
  "Header 3": "Parameters",
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> * - ``metadata``
>      - object
>      - optional
>      - Key-value pairs for storing extra info
>    * - ``on_behalf_of``
>      - string
>      - optional
>      - Connected account ID on whose behalf charges are made
>    * - ``transfer_data.destination``
>      - string
>      - optional
>      - Connected account to transfer funds to after each payment
>    * - ``application_fee_percent``
>      - float
>      - optional
>      - Percentage of amount to collect for the platform

---

### Chunk 228 | ID: `7d826fcb-fec1-44cf-b632-4f70d34b2ab1`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "version": "v1",
  "Header 2": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "Header 3": "Returns"
}
```

**Content:**
> Returns
> 
> Returns the created Subscription object.

---

### Chunk 229 | ID: `f7f791c4-ee9e-4da3-9271-740845747467`

**Metadata:**
```json
{
  "Header 2": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 3": "Example Request"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/subscriptions \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d customer=cus_Na6dX7aXxi11N4 \
>      -d "items[0][plan]"=plan_Na6dGcTsmU0I4R

---

### Chunk 230 | ID: `89fd0ecd-aa14-4806-87d1-2177ad9844a5`

**Metadata:**
```json
{
  "Header 3": "Example Response",
  "Header 2": "Create a Subscription",
  "Header 1": "Subscriptions",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
>      "object": "subscription",
>      "customer": "cus_Na6dX7aXxi11N4",
>      "status": "active",
>      "currency": "usd",
>      "collection_method": "charge_automatically",
>      "default_source": null,
>      "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
>      "billing_cycle_anchor": 1679609767,
>      "cancel_at_period_end": false,
>      "metadata": {},
>      "created": 1679609767,
>      "livemode": false,
>      "items": {
>        "data": [
>          {
>            "id": "si_Na6dzxczY5fwHx",
>            "quantity": 1,
>            "plan": {
>              "id": "plan_Na6dGcTsmU0I4R",
>              "amount": 1000,
>              "currency": "usd",
>              "interval": "month",
>              "interval_count": 1
>            }
>          }
>        ]
>      }
>    }

---

### Chunk 231 | ID: `62beec01-5b24-47d7-9d7e-1bedeb1a7ec0`

**Metadata:**
```json
{
  "Header 2": "Update a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 1": "Subscriptions"
}
```

**Content:**
> Update a Subscription
> 
> **POST** ``/v1/subscriptions/:id``
> 
> Updates an existing subscription. Used for upgrading/downgrading plans, changing quantities, and more. Stripe optionally prorates charges when plans or quantities change.

---

### Chunk 232 | ID: `4ec0c7ea-06eb-446e-9c3f-e78e07e8ddb8`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Update a Subscription",
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 35 20 45

---

### Chunk 233 | ID: `20b90118-0fee-49f8-a7d9-b477ef48c207`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "version": "v1",
  "Header 2": "Update a Subscription"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Description
>    * - ``items``
>      - array
>      - Updated list of items. Each can include ``id`` (existing item ID), ``plan``, ``quantity``, or ``deleted: true`` to remove
>    * - ``items[].id``
>      - string
>      - ID of existing subscription item to modify
>    * - ``items[].plan``
>      - string
>      - New Plan ID to switch to
>    * - ``items[].quantity``
>      - integer
>      - Updated quantity
>    * - ``items[].deleted``
>      - boolean
>      - Set ``true`` to remove this item
>    * - ``default_source``
>      - string
>      - ID of new default Source
>    * - ``collection_method``
>      - enum
>      - ``charge_automatically`` or ``send_invoice``
>    * - ``days_until_due``
>      - integer
>      - Days until invoice is due (for ``send_invoice``)
>    * - ``proration_behavior``
>      - enum
>      - ``create_prorations`` (default), ``none``, or ``always_invoice``
>    * - ``proration_date``
>      - timestamp
>      - Calculate prorations as if change happened at this time

---

### Chunk 234 | ID: `e97f5f0f-31f8-4b81-810e-95512d0413ec`

**Metadata:**
```json
{
  "version": "v1",
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Update a Subscription",
  "Header 1": "Subscriptions"
}
```

**Content:**
> - timestamp
>      - Calculate prorations as if change happened at this time
>    * - ``billing_cycle_anchor``
>      - ``now`` or ``unchanged``
>      - Reset billing anchor to now, or keep unchanged
>    * - ``cancel_at_period_end``
>      - boolean
>      - Set ``true`` to cancel at end of period
>    * - ``cancel_at``
>      - timestamp or ``""``
>      - Schedule/unschedule cancellation
>    * - ``trial_end``
>      - timestamp or ``now``
>      - End the trial at this time
>    * - ``description``
>      - string
>      - Arbitrary description
>    * - ``metadata``
>      - object
>      - Key-value pairs. Set key to ``""`` to unset

---

### Chunk 235 | ID: `d40b4b9b-1e45-4464-83b9-54609732abf2`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "Update a Subscription",
  "Header 1": "Subscriptions",
  "Header 3": "Returns",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Returns
> 
> Returns the updated Subscription object.

---

### Chunk 236 | ID: `a07b8d42-fb24-4de5-8588-2a1393c16b45`

**Metadata:**
```json
{
  "Header 2": "Update a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 3": "Example Request"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d "metadata[order_id]"=6735

---

### Chunk 237 | ID: `0b5a4e91-adef-4b94-9865-ae0b43f98848`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Update a Subscription",
  "Header 3": "Example Response"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
>      "object": "subscription",
>      "customer": "cus_Na6dX7aXxi11N4",
>      "status": "active",
>      "currency": "usd",
>      "default_source": null,
>      "cancel_at_period_end": false,
>      "metadata": { "order_id": "6735" },
>      "created": 1679609767,
>      "livemode": false,
>      "items": {
>        "data": [
>          {
>            "id": "si_Na6dzxczY5fwHx",
>            "quantity": 1,
>            "plan": {
>              "id": "plan_Na6dGcTsmU0I4R",
>              "amount": 1000,
>              "currency": "usd",
>              "interval": "month"
>            }
>          }
>        ]
>      }
>    }

---

### Chunk 238 | ID: `c6af2922-0088-4e89-8e1c-e847d741f4df`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 2": "Retrieve a Subscription"
}
```

**Content:**
> Retrieve a Subscription
> 
> **GET** ``/v1/subscriptions/:id``

---

### Chunk 239 | ID: `f62494c5-ce0b-41b7-b849-8822cfc2953c`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "Header 2": "Retrieve a Subscription",
  "version": "v1"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 20 20 60
> 
>    * - Parameter
>      - Type
>      - Description
>    * - ``id``
>      - string (path)
>      - The ID of the subscription to retrieve

---

### Chunk 240 | ID: `55d30f19-f891-436f-8684-f7d5682a9dea`

**Metadata:**
```json
{
  "Header 3": "Returns",
  "Header 2": "Retrieve a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 1": "Subscriptions"
}
```

**Content:**
> Returns
> 
> Returns the Subscription object.

---

### Chunk 241 | ID: `2c6c4ab7-6158-43d5-8d75-d720b95ce41a`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "Header 3": "Example Request",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Retrieve a Subscription",
  "version": "v1"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
>      -u "<<YOUR_SECRET_KEY>>"

---

### Chunk 242 | ID: `3c2cd76e-a2b5-4a39-892d-f30f9df0e2f1`

**Metadata:**
```json
{
  "version": "v1",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "Header 3": "Example Response",
  "Header 2": "Retrieve a Subscription"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
>      "object": "subscription",
>      "customer": "cus_Na6dX7aXxi11N4",
>      "status": "active",
>      "currency": "usd",
>      "collection_method": "charge_automatically",
>      "default_source": null,
>      "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
>      "billing_cycle_anchor": 1679609767,
>      "cancel_at_period_end": false,
>      "trial_start": null,
>      "trial_end": null,
>      "metadata": {},
>      "created": 1679609767,
>      "livemode": false,
>      "items": {
>        "data": [
>          {
>            "id": "si_Na6dzxczY5fwHx",
>            "quantity": 1,
>            "plan": {
>              "id": "plan_Na6dGcTsmU0I4R",
>              "amount": 1000,
>              "currency": "usd",
>              "interval": "month",
>              "interval_count": 1
>            }
>          }
>        ]
>      }
>    }

---

### Chunk 243 | ID: `74030894-51ce-4504-80ef-ee7f497b4fc9`

**Metadata:**
```json
{
  "version": "v1",
  "Header 2": "List Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions"
}
```

**Content:**
> List Subscriptions
> 
> **GET** ``/v1/subscriptions``
> 
> By default, returns subscriptions that have not been canceled. Use ``status=canceled`` to include canceled ones.

---

### Chunk 244 | ID: `5b19b674-515b-40cf-bf11-bc72d5a8ae57`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "Header 2": "List Subscriptions",
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 25 20 15 40

---

### Chunk 245 | ID: `261753e2-915b-4f5a-bedf-8c5b11ad5243`

**Metadata:**
```json
{
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "Header 2": "List Subscriptions",
  "version": "v1"
}
```

**Content:**
> * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``customer``
>      - string
>      - optional
>      - Filter by customer ID
>    * - ``plan``
>      - string
>      - optional
>      - Filter by Plan ID
>    * - ``status``
>      - enum
>      - optional
>      - Filter by status: ``active``, ``canceled``, ``past_due``, ``trialing``, ``unpaid``, or ``all``
>    * - ``collection_method``
>      - enum
>      - optional
>      - ``charge_automatically`` or ``send_invoice``
>    * - ``limit``
>      - integer
>      - optional
>      - Number of results (1–100, default 10)
>    * - ``starting_after``
>      - string
>      - optional
>      - Subscription ID cursor — fetch next page after this ID
>    * - ``ending_before``
>      - string
>      - optional
>      - Subscription ID cursor — fetch previous page before this ID
>    * - ``created.gt``
>      - integer
>      - optional
>      - Created after this Unix timestamp (exclusive)
>    * - ``created.gte``
>      - integer
>      - optional

---

### Chunk 246 | ID: `406a6a26-0983-4bea-86e9-ab01e1b398ff`

**Metadata:**
```json
{
  "Header 2": "List Subscriptions",
  "Header 1": "Subscriptions",
  "Header 3": "Parameters",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> * - ``created.gte``
>      - integer
>      - optional
>      - Created at or after this Unix timestamp (inclusive)
>    * - ``created.lt``
>      - integer
>      - optional
>      - Created before this Unix timestamp (exclusive)
>    * - ``created.lte``
>      - integer
>      - optional
>      - Created at or before this Unix timestamp (inclusive)

---

### Chunk 247 | ID: `7245c873-eeca-401c-93b7-3d29d930b472`

**Metadata:**
```json
{
  "Header 3": "Returns",
  "Header 1": "Subscriptions",
  "Header 2": "List Subscriptions",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Returns
> 
> A dictionary with a ``data`` array of Subscription objects. Includes ``has_more`` for pagination.

---

### Chunk 248 | ID: `c3fb1bfd-ef1a-4f6a-b342-05f688990e8a`

**Metadata:**
```json
{
  "Header 2": "List Subscriptions",
  "Header 1": "Subscriptions",
  "version": "v1",
  "Header 3": "Example Request",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl -G https://api.stripe.com/v1/subscriptions \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d limit=3

---

### Chunk 249 | ID: `7487bf80-cd57-48f5-b0ab-a706857dda46`

**Metadata:**
```json
{
  "Header 2": "List Subscriptions",
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 3": "Example Response",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "object": "list",
>      "url": "/v1/subscriptions",
>      "has_more": false,
>      "data": [
>        {
>          "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
>          "object": "subscription",
>          "customer": "cus_Na6dX7aXxi11N4",
>          "status": "active",
>          "currency": "usd",
>          "default_source": null,
>          "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
>          "cancel_at_period_end": false,
>          "metadata": {},
>          "created": 1679609767,
>          "livemode": false,
>          "items": {
>            "data": [
>              {
>                "id": "si_Na6dzxczY5fwHx",
>                "quantity": 1,
>                "plan": {
>                  "id": "plan_Na6dGcTsmU0I4R",
>                  "amount": 1000,
>                  "currency": "usd",
>                  "interval": "month"
>                }
>              }
>            ]
>          }
>        }
>      ]
>    }

---

### Chunk 250 | ID: `9448b80a-b355-4a63-b23e-b21165f26c77`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 2": "Cancel a Subscription",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Cancel a Subscription
> 
> **DELETE** ``/v1/subscriptions/:id``
> 
> Cancels a subscription immediately. The customer won't be charged again.

---

### Chunk 251 | ID: `01e1bf7b-870c-4466-a408-2952bdbad506`

**Metadata:**
```json
{
  "Header 2": "Cancel a Subscription",
  "Header 1": "Subscriptions",
  "version": "v1",
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 30 20 15 35
> 
>    * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``id``
>      - string (path)
>      - **required**
>      - The ID of the subscription to cancel
>    * - ``invoice_now``
>      - boolean
>      - optional
>      - If ``true``, generates a final invoice for un-invoiced usage. Default ``false``
>    * - ``prorate``
>      - boolean
>      - optional
>      - If ``true``, generates a proration credit for unused time. Default ``false``

---

### Chunk 252 | ID: `ae8f8628-0469-4746-98e9-832fc1a8196d`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "Header 3": "Returns",
  "version": "v1",
  "Header 2": "Cancel a Subscription",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Returns
> 
> Returns the canceled Subscription object with ``status: "canceled"``.

---

### Chunk 253 | ID: `5f924a8c-055d-4c4e-81c1-1c7762049a8a`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Subscriptions",
  "Header 3": "Example Request",
  "Header 2": "Cancel a Subscription",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl -X DELETE https://api.stripe.com/v1/subscriptions/sub_1MlPf9LkdIwHu7ixB6VIYRyX \
>      -u "<<YOUR_SECRET_KEY>>"

---

### Chunk 254 | ID: `d93b678f-d6a2-4d38-87e2-32dabb3af543`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "version": "v1",
  "Header 2": "Cancel a Subscription",
  "Header 3": "Example Response",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "sub_1MlPf9LkdIwHu7ixB6VIYRyX",
>      "object": "subscription",
>      "customer": "cus_NWSaVkvdacCUi4",
>      "status": "canceled",
>      "currency": "usd",
>      "canceled_at": 1678768842,
>      "ended_at": 1678768842,
>      "cancel_at_period_end": false,
>      "metadata": {},
>      "created": 1678768838,
>      "livemode": false,
>      "items": {
>        "data": [
>          {
>            "id": "si_NWSaWTp80M123q",
>            "quantity": 1,
>            "plan": {
>              "id": "plan_NWSaMgipulx8IQ",
>              "amount": 1099,
>              "currency": "usd",
>              "interval": "month"
>            }
>          }
>        ]
>      }
>    }

---

### Chunk 255 | ID: `2de24b46-bfc9-4022-94b8-6e777411511e`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Resume a Subscription",
  "Header 1": "Subscriptions",
  "version": "v1"
}
```

**Content:**
> Resume a Subscription
> 
> **POST** ``/v1/subscriptions/:id/resume``
> 
> Resumes a subscription that was canceled with ``cancel_at_period_end=true`` and has not yet reached the period end. Not applicable for immediately canceled subscriptions.

---

### Chunk 256 | ID: `0c31bb01-d229-4354-9815-381f0e324a9b`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "Header 2": "Resume a Subscription",
  "version": "v1",
  "Header 3": "Parameters",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Parameters
> 
> .. list-table::
>    :header-rows: 1
>    :widths: 30 20 15 35
> 
>    * - Parameter
>      - Type
>      - Required
>      - Description
>    * - ``id``
>      - string (path)
>      - **required**
>      - The ID of the subscription to resume
>    * - ``billing_cycle_anchor``
>      - enum
>      - optional
>      - ``now`` (default) resets billing cycle; ``unchanged`` keeps existing anchor
>    * - ``proration_behavior``
>      - enum
>      - optional
>      - ``create_prorations`` (default), ``none``, or ``always_invoice``

---

### Chunk 257 | ID: `de6eb428-ff4a-43c2-8933-4bfb5ef4b6bd`

**Metadata:**
```json
{
  "Header 2": "Resume a Subscription",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Subscriptions",
  "Header 3": "Returns"
}
```

**Content:**
> Returns
> 
> Returns the Subscription object with ``status: "active"``.

---

### Chunk 258 | ID: `92168d95-f9e6-4b7b-88d1-e437e6efcd98`

**Metadata:**
```json
{
  "Header 1": "Subscriptions",
  "Header 2": "Resume a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v1",
  "Header 3": "Example Request"
}
```

**Content:**
> Example Request
> 
> .. code-block:: bash
> 
>    curl https://api.stripe.com/v1/subscriptions/sub_1MoGGtLkdIwHu7ixk5CfdiqC/resume \
>      -u "<<YOUR_SECRET_KEY>>" \
>      -d billing_cycle_anchor=now

---

### Chunk 259 | ID: `0155a22d-fc8e-4d28-8f1d-d7b13c88b4d3`

**Metadata:**
```json
{
  "Header 3": "Example Response",
  "version": "v1",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Resume a Subscription",
  "Header 1": "Subscriptions"
}
```

**Content:**
> Example Response
> 
> .. code-block:: json
> 
>    {
>      "id": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",
>      "object": "subscription",
>      "customer": "cus_NZP5i1diUz55jp",
>      "status": "active",
>      "currency": "usd",
>      "billing_cycle_anchor": 1679447726,
>      "default_source": null,
>      "latest_invoice": "in_1MoGGwLkdIwHu7ixHSrelo8X",
>      "cancel_at_period_end": false,
>      "metadata": {},
>      "created": 1679447723,
>      "livemode": false,
>      "items": {
>        "data": [
>          {
>            "id": "si_NZP5BhUIuWzXDG",
>            "quantity": 1,
>            "plan": {
>              "id": "plan_NZP5rEATBlScM9",
>              "amount": 1099,
>              "currency": "usd",
>              "interval": "month"
>            }
>          }
>        ]
>      }
>    }

---

### Chunk 260 | ID: `a5f9bbc2-14d0-4f9c-86e0-2dbff19eeaca`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "The Subscription Object",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> A Subscription charges a customer on a recurring basis using a Price attached to a Product.

---

### Chunk 261 | ID: `b8da09b7-3475-41dd-99a6-a183638efed6`

**Metadata:**
```json
{
  "Header 2": "Status Lifecycle",
  "Header 1": "The Subscription Object",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2"
}
```

**Content:**
> `incomplete` → `active` → `past_due` → `canceled` / `unpaid`
> Or: `trialing` → `active` | `paused` (when `pause_collection` is set)

---

### Chunk 262 | ID: `8462678e-9f7c-48ca-960f-4a73dd712fe7`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "The Subscription Object",
  "Header 2": "Key Fields",
  "version": "v2"
}
```

**Content:**
> | Field | Type | Description |
> |-------|------|-------------|
> | `id` | string | Unique identifier (e.g. `sub_1MowQVLkdIwHu7ixeRlqHVzs`) |
> | `object` | string | Always `"subscription"` |
> | `customer` | string | ID of the Customer being billed |
> | `status` | enum | `incomplete`, `incomplete_expired`, `trialing`, `active`, `past_due`, `canceled`, `unpaid`, or `paused` |
> | `items.data` | array | List of subscription items, each with a `price` and `quantity` |
> | `items.data[].price.id` | string | ID of the Price for this item |
> | `items.data[].price.unit_amount` | integer | Price amount in smallest currency unit |
> | `items.data[].price.recurring.interval` | string | Billing interval: `day`, `week`, `month`, or `year` |
> | `items.data[].quantity` | integer | Quantity of the price |
> | `currency` | string | Three-letter ISO currency code |
> | `collection_method` | enum | `charge_automatically` or `send_invoice` |

---

### Chunk 263 | ID: `92e50ff3-bbd3-4a33-a971-5ac14f61413d`

**Metadata:**
```json
{
  "Header 2": "Key Fields",
  "Header 1": "The Subscription Object",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> | `collection_method` | enum | `charge_automatically` or `send_invoice` |
> | `default_payment_method` | string | ID of default PaymentMethod for this subscription |
> | `latest_invoice` | string | ID of the most recent invoice |
> | `current_period_start` | timestamp | Start of the current billing period |
> | `current_period_end` | timestamp | End of the current billing period |
> | `billing_cycle_anchor` | timestamp | Reference point for billing cycle |
> | `cancel_at_period_end` | boolean | If `true`, cancels at end of current period |
> | `cancel_at` | timestamp | Scheduled cancellation timestamp |
> | `canceled_at` | timestamp | When the subscription was canceled |
> | `ended_at` | timestamp | When the subscription ended |
> | `start_date` | timestamp | When the subscription started |
> | `trial_start` | timestamp | Start of trial period |
> | `trial_end` | timestamp | End of trial period |
> | `pause_collection` | object | If set, collection is paused. Contains `behavior` and optional `resumes_at` |

---

### Chunk 264 | ID: `727cff58-beef-4517-8d7d-7254a01ec1c8`

**Metadata:**
```json
{
  "Header 2": "Key Fields",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "The Subscription Object"
}
```

**Content:**
> | `description` | string | Arbitrary description |
> | `metadata` | object | Key-value pairs for storing extra info |
> | `on_behalf_of` | string | Connected account ID on whose behalf charges are made |
> | `transfer_data.destination` | string | Connected account to transfer funds to |
> | `application_fee_percent` | float | Percentage of subscription amount to collect for the platform |
> | `proration_behavior` | enum | How prorations are handled on updates: `create_prorations`, `none`, or `always_invoice` |
> | `created` | timestamp | Unix timestamp of creation |
> | `livemode` | boolean | True if live mode, false if test mode |

---

### Chunk 265 | ID: `d4f854c0-c8b1-4899-b73c-dbb694c9878b`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "The Subscription Object",
  "Header 2": "Example Object"
}
```

**Content:**
> ```json
> {
> "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
> "object": "subscription",
> "customer": "cus_Na6dX7aXxi11N4",
> "status": "active",
> "currency": "usd",
> "collection_method": "charge_automatically",
> "default_payment_method": null,
> "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
> "billing_cycle_anchor": 1679609767,
> "start_date": 1679609767,
> "cancel_at_period_end": false,
> "cancel_at": null,
> "canceled_at": null,
> "ended_at": null,
> "trial_start": null,
> "trial_end": null,
> "pause_collection": null,
> "description": null,
> "metadata": {},
> "on_behalf_of": null,
> "transfer_data": null,
> "created": 1679609767,
> "livemode": false,
> "items": {
> "object": "list",
> "data": [
> {
> "id": "si_Na6dzxczY5fwHx",
> "object": "subscription_item",
> "quantity": 1,
> "price": {
> "id": "price_1MowQULkdIwHu7ixraBm864M",
> "object": "price",
> "currency": "usd",
> "unit_amount": 1000,
> "type": "recurring",
> "recurring": {
> "interval": "month",
> "interval_count": 1
> },
> "product": "prod_Na6dGcTsmU0I4R",
> "active": true
> }
> }
> ],
> "has_more": false
> }
> }
> ```

---

### Chunk 266 | ID: `84f2c46b-70d7-481e-9d3e-816ca179b167`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Subscriptions allow you to charge a customer on a recurring basis.

---

### Chunk 267 | ID: `407098f0-b9af-4b00-bf99-a0b4a0946bc2`

**Metadata:**
```json
{
  "Header 2": "Endpoints",
  "Header 1": "Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2"
}
```

**Content:**
> | Method | Endpoint | Description |
> |--------|----------|-------------|
> | POST | `/v1/subscriptions` | Create a subscription |
> | POST | `/v1/subscriptions/:id` | Update a subscription |
> | GET | `/v1/subscriptions/:id` | Retrieve a subscription |
> | GET | `/v1/subscriptions` | List all subscriptions |
> | DELETE | `/v1/subscriptions/:id` | Cancel a subscription |
> | POST | `/v1/subscriptions/:id/resume` | Resume a paused subscription |

---

### Chunk 268 | ID: `6a9fe3ac-2666-4622-97c5-727f627de82c`

**Metadata:**
```json
{
  "Header 1": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2"
}
```

**Content:**
> **POST** `/v1/subscriptions`

---

### Chunk 269 | ID: `a632ec1a-1fa9-4cca-909e-911d51106ab9`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Create a Subscription"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `customer` | string | **required** | ID of the Customer to subscribe |
> | `items` | array | **required** | List of items. Each item needs a `price` (Price ID) and optional `quantity` (default 1) |
> | `items[].price` | string | required per item | ID of the Price to subscribe to |
> | `items[].quantity` | integer | optional | Quantity for this price (default 1) |
> | `currency` | enum | optional | Three-letter ISO currency code. Defaults to the price's currency |
> | `default_payment_method` | string | optional | ID of default PaymentMethod for this subscription |
> | `collection_method` | enum | optional | `charge_automatically` (default) or `send_invoice` |
> | `days_until_due` | integer | optional | Days until invoice is due (required when `collection_method=send_invoice`) |
> | `payment_behavior` | enum | optional | `allow_incomplete`, `error_if_incomplete` (default), or `default_incomplete` |

---

### Chunk 270 | ID: `e37afa23-acd9-4a5e-92e6-9137a09c0e1d`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 2": "Parameters",
  "Header 1": "Create a Subscription"
}
```

**Content:**
> | `proration_behavior` | enum | optional | `create_prorations` (default), `none`, or `always_invoice` |
> | `billing_cycle_anchor` | timestamp | optional | Sets the billing cycle anchor to a specific Unix timestamp |
> | `cancel_at_period_end` | boolean | optional | If `true`, cancels at end of current period |
> | `cancel_at` | timestamp | optional | Schedules cancellation at this Unix timestamp |
> | `trial_period_days` | integer | optional | Number of trial days before billing starts |
> | `trial_end` | timestamp or `now` | optional | Ends trial at this Unix timestamp |
> | `description` | string | optional | Arbitrary description |
> | `metadata` | object | optional | Key-value pairs for storing extra info |
> | `on_behalf_of` | string | optional | Connected account ID on whose behalf charges are made |
> | `transfer_data.destination` | string | optional | Connected account to transfer funds to after each payment |

---

### Chunk 271 | ID: `56e1284a-ad0f-4fd8-a8e9-f530b3e70ecf`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Create a Subscription",
  "Header 2": "Parameters",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> | `application_fee_percent` | float | optional | Percentage of amount to collect for the platform |
> | `off_session` | boolean | optional | Set `true` if customer is not actively in your checkout flow |

---

### Chunk 272 | ID: `83dab16e-e61f-4265-922f-cfde79dd6b86`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Returns",
  "version": "v2",
  "Header 1": "Create a Subscription"
}
```

**Content:**
> Returns the created Subscription object.

---

### Chunk 273 | ID: `9bd70660-4577-47f6-9994-b0a1633f650f`

**Metadata:**
```json
{
  "Header 2": "Example Request",
  "version": "v2",
  "Header 1": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/subscriptions \
> -u "<<YOUR_SECRET_KEY>>" \
> -d customer=cus_Na6dX7aXxi11N4 \
> -d "items[0][price]"=price_1MowQULkdIwHu7ixraBm864M
> ```

---

### Chunk 274 | ID: `49621e74-c20b-40cc-b61d-a7b1c0e8d23c`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Example Response",
  "Header 1": "Create a Subscription",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> ```json
> {
> "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
> "object": "subscription",
> "customer": "cus_Na6dX7aXxi11N4",
> "status": "active",
> "currency": "usd",
> "collection_method": "charge_automatically",
> "default_payment_method": null,
> "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
> "billing_cycle_anchor": 1679609767,
> "start_date": 1679609767,
> "cancel_at_period_end": false,
> "trial_start": null,
> "trial_end": null,
> "metadata": {},
> "created": 1679609767,
> "livemode": false,
> "items": {
> "object": "list",
> "data": [
> {
> "id": "si_Na6dzxczY5fwHx",
> "quantity": 1,
> "price": {
> "id": "price_1MowQULkdIwHu7ixraBm864M",
> "currency": "usd",
> "unit_amount": 1000,
> "recurring": { "interval": "month", "interval_count": 1 }
> }
> }
> ]
> }
> }
> ```

---

### Chunk 275 | ID: `2eb99274-d918-446d-ad41-60cd02a703c7`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 1": "Update a Subscription"
}
```

**Content:**
> **POST** `/v1/subscriptions/:id`  
> Updates an existing subscription. Used for upgrading/downgrading plans, changing quantities, pausing collection, and more. Stripe optionally prorates charges when prices or quantities change.

---

### Chunk 276 | ID: `c21593ad-014e-49b4-92f0-bb5e633d1e4f`

**Metadata:**
```json
{
  "Header 1": "Update a Subscription",
  "Header 2": "Parameters",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `items` | array | optional | Updated list of items. Each can include `id` (existing item ID), `price`, `quantity`, or `deleted: true` to remove |
> | `items[].id` | string | optional | ID of existing subscription item to modify |
> | `items[].price` | string | optional | New Price ID to switch to |
> | `items[].quantity` | integer | optional | Updated quantity |
> | `items[].deleted` | boolean | optional | Set `true` to remove this item |
> | `default_payment_method` | string | optional | ID of new default PaymentMethod |
> | `collection_method` | enum | optional | `charge_automatically` or `send_invoice` |
> | `days_until_due` | integer | optional | Days until invoice is due (for `send_invoice`) |
> | `proration_behavior` | enum | optional | `create_prorations` (default), `none`, or `always_invoice` |
> | `proration_date` | timestamp | optional | Calculate prorations as if change happened at this time |

---

### Chunk 277 | ID: `b7058cb5-4e9d-42ea-9bb6-3fc5e5a4874e`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Update a Subscription",
  "version": "v2",
  "Header 2": "Parameters"
}
```

**Content:**
> | `billing_cycle_anchor` | `now` or `unchanged` | optional | Reset billing anchor to now, or keep unchanged |
> | `cancel_at_period_end` | boolean | optional | Set `true` to cancel at end of period, `false` to undo |
> | `cancel_at` | timestamp or `""` | optional | Schedule/unschedule cancellation |
> | `trial_end` | timestamp or `now` | optional | End the trial at this time |
> | `pause_collection` | object | optional | Pause billing. Set `behavior` to `keep_as_draft`, `mark_uncollectible`, or `void`. Set to `""` to resume |
> | `pause_collection.behavior` | enum | optional | What to do with invoices while paused |
> | `pause_collection.resumes_at` | timestamp | optional | Auto-resume at this timestamp |
> | `payment_behavior` | enum | optional | `allow_incomplete`, `error_if_incomplete`, or `default_incomplete` |
> | `description` | string | optional | Arbitrary description |
> | `metadata` | object | optional | Key-value pairs. Set key to `""` to unset |

---

### Chunk 278 | ID: `b924308d-4e34-47cd-b735-553314063801`

**Metadata:**
```json
{
  "Header 1": "Update a Subscription",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Parameters"
}
```

**Content:**
> | `metadata` | object | optional | Key-value pairs. Set key to `""` to unset |
> | `on_behalf_of` | string | optional | Connected account ID |
> | `transfer_data` | object | optional | Set destination for fund transfers, or `""` to remove |
> | `cancellation_details.comment` | string | optional | Comment about why subscription is being changed |
> | `cancellation_details.feedback` | enum | optional | Customer feedback reason |

---

### Chunk 279 | ID: `6ff177bd-89e4-48c8-ab9e-882b4f81a81a`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Update a Subscription",
  "Header 2": "Returns"
}
```

**Content:**
> Returns the updated Subscription object.

---

### Chunk 280 | ID: `49a5940b-571f-4fc1-b12c-1b21125f3d96`

**Metadata:**
```json
{
  "Header 1": "Update a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 2": "Example Request"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
> -u "<<YOUR_SECRET_KEY>>" \
> -d "metadata[order_id]"=6735
> ```

---

### Chunk 281 | ID: `2e8eb858-9d61-4c8b-9555-6245ab90ca1a`

**Metadata:**
```json
{
  "Header 2": "Example Response",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 1": "Update a Subscription"
}
```

**Content:**
> ```json
> {
> "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
> "object": "subscription",
> "customer": "cus_Na6dX7aXxi11N4",
> "status": "active",
> "currency": "usd",
> "collection_method": "charge_automatically",
> "default_payment_method": null,
> "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
> "cancel_at_period_end": false,
> "pause_collection": null,
> "metadata": { "order_id": "6735" },
> "created": 1679609767,
> "livemode": false,
> "items": {
> "object": "list",
> "data": [
> {
> "id": "si_Na6dzxczY5fwHx",
> "quantity": 1,
> "price": {
> "id": "price_1MowQULkdIwHu7ixraBm864M",
> "currency": "usd",
> "unit_amount": 1000,
> "recurring": { "interval": "month", "interval_count": 1 }
> }
> }
> ]
> }
> }
> ```

---

### Chunk 282 | ID: `12bffc07-0607-4675-bc19-96c1e02e5195`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 1": "Retrieve a Subscription"
}
```

**Content:**
> **GET** `/v1/subscriptions/:id`

---

### Chunk 283 | ID: `3bbdf884-0280-4630-bd56-c4b7cccf0257`

**Metadata:**
```json
{
  "Header 1": "Retrieve a Subscription",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Parameters"
}
```

**Content:**
> | Parameter | Type | Description |
> |-----------|------|-------------|
> | `id` | string (path) | The ID of the subscription to retrieve |

---

### Chunk 284 | ID: `ee00d489-0dd2-4ba6-aa2b-2a9f276ddeb9`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Retrieve a Subscription",
  "Header 2": "Returns",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Returns the Subscription object.

---

### Chunk 285 | ID: `1e28064d-fa2b-487a-bf84-767c6b53dee2`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 2": "Example Request",
  "Header 1": "Retrieve a Subscription"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/subscriptions/sub_1MowQVLkdIwHu7ixeRlqHVzs \
> -u "<<YOUR_SECRET_KEY>>"
> ```

---

### Chunk 286 | ID: `0791943a-5d06-4f34-9029-80e106e8a364`

**Metadata:**
```json
{
  "Header 1": "Retrieve a Subscription",
  "version": "v2",
  "Header 2": "Example Response",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> ```json
> {
> "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
> "object": "subscription",
> "customer": "cus_Na6dX7aXxi11N4",
> "status": "active",
> "currency": "usd",
> "collection_method": "charge_automatically",
> "default_payment_method": null,
> "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
> "billing_cycle_anchor": 1679609767,
> "start_date": 1679609767,
> "cancel_at_period_end": false,
> "cancel_at": null,
> "canceled_at": null,
> "ended_at": null,
> "trial_start": null,
> "trial_end": null,
> "pause_collection": null,
> "description": null,
> "metadata": {},
> "created": 1679609767,
> "livemode": false,
> "items": {
> "object": "list",
> "data": [
> {
> "id": "si_Na6dzxczY5fwHx",
> "quantity": 1,
> "price": {
> "id": "price_1MowQULkdIwHu7ixraBm864M",
> "currency": "usd",
> "unit_amount": 1000,
> "recurring": { "interval": "month", "interval_count": 1 }
> }
> }
> ]
> }
> }
> ```

---

### Chunk 287 | ID: `4ed9a3ae-aab5-4f0e-9ebb-0b371ebbeaf0`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "List Subscriptions"
}
```

**Content:**
> **GET** `/v1/subscriptions`  
> By default, returns subscriptions that have not been canceled. Use `status=canceled` to include canceled ones.

---

### Chunk 288 | ID: `3a87058c-44b7-4fcb-9388-c17058726a4a`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Parameters",
  "Header 1": "List Subscriptions"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `customer` | string | optional | Filter by customer ID |
> | `status` | enum | optional | Filter by status: `active`, `canceled`, `incomplete`, `incomplete_expired`, `past_due`, `paused`, `trialing`, `unpaid`, or `all` |
> | `price` | string | optional | Filter by Price ID |
> | `collection_method` | enum | optional | `charge_automatically` or `send_invoice` |
> | `limit` | integer | optional | Number of results (1–100, default 10) |
> | `starting_after` | string | optional | Subscription ID cursor — fetch next page after this ID |
> | `ending_before` | string | optional | Subscription ID cursor — fetch previous page before this ID |
> | `created.gt` | integer | optional | Created after this Unix timestamp (exclusive) |
> | `created.gte` | integer | optional | Created at or after this Unix timestamp (inclusive) |
> | `created.lt` | integer | optional | Created before this Unix timestamp (exclusive) |

---

### Chunk 289 | ID: `be1f519d-e748-4dfd-9222-ca4124652fa3`

**Metadata:**
```json
{
  "Header 2": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 1": "List Subscriptions"
}
```

**Content:**
> | `created.lt` | integer | optional | Created before this Unix timestamp (exclusive) |
> | `created.lte` | integer | optional | Created at or before this Unix timestamp (inclusive) |

---

### Chunk 290 | ID: `770c329e-dda7-4eac-92e1-48aa3abbede1`

**Metadata:**
```json
{
  "Header 2": "Returns",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "List Subscriptions",
  "version": "v2"
}
```

**Content:**
> A dictionary with a `data` array of Subscription objects. Includes `has_more` for pagination.

---

### Chunk 291 | ID: `d90042fe-969a-4d6b-89cc-ce4182a91f02`

**Metadata:**
```json
{
  "Header 1": "List Subscriptions",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Example Request",
  "version": "v2"
}
```

**Content:**
> ```curl
> curl -G https://api.stripe.com/v1/subscriptions \
> -u "<<YOUR_SECRET_KEY>>" \
> -d limit=3
> ```

---

### Chunk 292 | ID: `1e8f40ae-a428-441a-aee8-4b6eb4810886`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "List Subscriptions",
  "Header 2": "Example Response",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> ```json
> {
> "object": "list",
> "url": "/v1/subscriptions",
> "has_more": false,
> "data": [
> {
> "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
> "object": "subscription",
> "customer": "cus_Na6dX7aXxi11N4",
> "status": "active",
> "currency": "usd",
> "collection_method": "charge_automatically",
> "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
> "cancel_at_period_end": false,
> "metadata": {},
> "created": 1679609767,
> "livemode": false,
> "items": {
> "data": [
> {
> "id": "si_Na6dzxczY5fwHx",
> "quantity": 1,
> "price": {
> "id": "price_1MowQULkdIwHu7ixraBm864M",
> "unit_amount": 1000,
> "currency": "usd",
> "recurring": { "interval": "month", "interval_count": 1 }
> }
> }
> ]
> }
> }
> ]
> }
> ```

---

### Chunk 293 | ID: `6eebd105-8cd5-427d-9d52-6e1c28fc496e`

**Metadata:**
```json
{
  "Header 1": "Cancel a Subscription",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2"
}
```

**Content:**
> **DELETE** `/v1/subscriptions/:id`  
> Cancels a subscription immediately. The customer won't be charged again. After cancellation, the subscription can no longer be updated.

---

### Chunk 294 | ID: `f1256d78-d3f4-4b16-95c0-3e74488db309`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Cancel a Subscription",
  "Header 2": "Parameters",
  "version": "v2"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `id` | string (path) | **required** | The ID of the subscription to cancel |
> | `invoice_now` | boolean | optional | If `true`, generates a final invoice for any un-invoiced usage. Default `false` |
> | `prorate` | boolean | optional | If `true`, generates a proration credit for unused time. Default `false` |
> | `cancellation_details.comment` | string | optional | Internal comment about the cancellation |
> | `cancellation_details.feedback` | enum | optional | Customer reason: `customer_service`, `low_quality`, `missing_features`, `other`, `switched_service`, `too_complex`, `too_expensive`, or `unused` |

---

### Chunk 295 | ID: `92afbc0b-4249-4bcb-8eab-81d06c5e3ffa`

**Metadata:**
```json
{
  "Header 1": "Cancel a Subscription",
  "Header 2": "Returns",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> Returns the canceled Subscription object with `status: "canceled"`.

---

### Chunk 296 | ID: `6a3c811b-7941-431b-a9d9-7a529422927e`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Example Request",
  "Header 1": "Cancel a Subscription",
  "version": "v2"
}
```

**Content:**
> ```curl
> curl -X DELETE https://api.stripe.com/v1/subscriptions/sub_1MlPf9LkdIwHu7ixB6VIYRyX \
> -u "<<YOUR_SECRET_KEY>>"
> ```

---

### Chunk 297 | ID: `58b81991-9963-4744-881b-4ec31caa2c02`

**Metadata:**
```json
{
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Cancel a Subscription",
  "Header 2": "Example Response",
  "version": "v2"
}
```

**Content:**
> ```json
> {
> "id": "sub_1MlPf9LkdIwHu7ixB6VIYRyX",
> "object": "subscription",
> "customer": "cus_NWSaVkvdacCUi4",
> "status": "canceled",
> "currency": "usd",
> "canceled_at": 1678768842,
> "ended_at": 1678768842,
> "cancel_at_period_end": false,
> "cancellation_details": {
> "comment": null,
> "feedback": null,
> "reason": "cancellation_requested"
> },
> "latest_invoice": "in_1MlPf9LkdIwHu7ixEo6hdgCw",
> "metadata": {},
> "created": 1678768838,
> "livemode": false,
> "items": {
> "data": [
> {
> "id": "si_NWSaWTp80M123q",
> "quantity": 1,
> "price": {
> "id": "price_1MlPf7LkdIwHu7ixgcbP7cwE",
> "unit_amount": 1099,
> "currency": "usd",
> "recurring": { "interval": "month", "interval_count": 1 }
> }
> }
> ]
> }
> }
> ```

---

### Chunk 298 | ID: `2d85f0e3-28da-4d79-9f46-9b16df489ee4`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Resume a Subscription",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> **POST** `/v1/subscriptions/:id/resume`  
> Resumes a paused subscription. If no resumption invoice is generated, the subscription becomes `active` immediately. If a resumption invoice is generated, the subscription stays `paused` until it's paid.

---

### Chunk 299 | ID: `a1e7ea0e-349c-4c09-b1de-242bb6197332`

**Metadata:**
```json
{
  "version": "v2",
  "Header 2": "Parameters",
  "api_class": "SUBSCRIPTIONS",
  "Header 1": "Resume a Subscription"
}
```

**Content:**
> | Parameter | Type | Required | Description |
> |-----------|------|----------|-------------|
> | `id` | string (path) | **required** | The ID of the subscription to resume |
> | `billing_cycle_anchor` | enum | optional | `now` (default) resets billing cycle; `unchanged` keeps existing anchor |
> | `proration_behavior` | enum | optional | Only applies when `billing_cycle_anchor=unchanged`. `create_prorations` (default), `none`, or `always_invoice` |

---

### Chunk 300 | ID: `d4b8a052-4623-4e3e-b46b-57dceca61a13`

**Metadata:**
```json
{
  "Header 2": "Returns",
  "api_class": "SUBSCRIPTIONS",
  "version": "v2",
  "Header 1": "Resume a Subscription"
}
```

**Content:**
> Returns the Subscription object with updated status.

---

### Chunk 301 | ID: `ca5f7b22-415d-4ab2-9311-810655733095`

**Metadata:**
```json
{
  "Header 1": "Resume a Subscription",
  "version": "v2",
  "api_class": "SUBSCRIPTIONS",
  "Header 2": "Example Request"
}
```

**Content:**
> ```curl
> curl https://api.stripe.com/v1/subscriptions/sub_1MoGGtLkdIwHu7ixk5CfdiqC/resume \
> -u "<<YOUR_SECRET_KEY>>" \
> -d billing_cycle_anchor=now
> ```

---

### Chunk 302 | ID: `a5d2e209-5aea-4bba-89f2-f4b707e27a5b`

**Metadata:**
```json
{
  "Header 1": "Resume a Subscription",
  "version": "v2",
  "Header 2": "Example Response",
  "api_class": "SUBSCRIPTIONS"
}
```

**Content:**
> ```json
> {
> "id": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",
> "object": "subscription",
> "customer": "cus_NZP5i1diUz55jp",
> "status": "active",
> "currency": "usd",
> "collection_method": "charge_automatically",
> "billing_cycle_anchor": 1679447726,
> "pause_collection": null,
> "latest_invoice": "in_1MoGGwLkdIwHu7ixHSrelo8X",
> "cancel_at_period_end": false,
> "metadata": {},
> "created": 1679447723,
> "livemode": false,
> "items": {
> "data": [
> {
> "id": "si_NZP5BhUIuWzXDG",
> "quantity": 1,
> "price": {
> "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",
> "unit_amount": 1099,
> "currency": "usd",
> "recurring": { "interval": "month", "interval_count": 1 }
> }
> }
> ]
> }
> }
> ```

---

### Chunk 303 | ID: `3a351b78-3795-4643-8b85-3ccf6036bb67`

**Metadata:**
```json
{
  "api_class": "TRANSFERS",
  "Header 1": "Transfers",
  "version": "v1"
}
```

**Content:**
> =========
> Transfers
> 
> A Transfer object is created when you move funds between accounts.

---

### Chunk 304 | ID: `f3864fad-df7c-40ee-a4be-66f03baf8381`

**Metadata:**
```json
{
  "api_class": "TRANSFERS",
  "Header 1": "Transfers",
  "version": "v1",
  "Header 2": "The Transfer Object"
}
```

**Content:**
> The Transfer Object
> 
> * **id** (string): Unique identifier for the object.
> * **object** (string): Always has the value ``transfer``.
> * **amount_in_cents** (integer): Amount in cents to be transferred.
> * **currency_code** (enum): Three-letter ISO currency code, in lowercase.
> * **recipient_id** (string): ID of the account the transfer was sent to.
> * **is_reversed** (boolean): Whether the transfer has been fully reversed.

---

### Chunk 305 | ID: `afb64421-9a49-46a3-9d30-3f88791fc974`

**Metadata:**
```json
{
  "version": "v1",
  "Header 1": "Transfers",
  "api_class": "TRANSFERS",
  "Header 2": "Endpoints"
}
```

**Content:**
> Endpoints

---

### Chunk 306 | ID: `0a359a63-d87a-4c34-86b8-3eaa7d68ef79`

**Metadata:**
```json
{
  "Header 1": "Transfers",
  "api_class": "TRANSFERS",
  "Header 2": "Create a transfer",
  "version": "v1"
}
```

**Content:**
> Create a transfer
> **POST /api/v1.0/transfers**
> 
> **Parameters:**
> 
> * **amount_in_cents** (integer, required): A positive integer in cents representing how much to transfer.
> * **currency_code** (enum, required): Three-letter ISO code for currency.
> * **recipient_id** (string, required): The ID of the connected account.

---

### Chunk 307 | ID: `54f8a377-162c-4a8c-a200-79bfca74060e`

**Metadata:**
```json
{
  "api_class": "TRANSFERS",
  "version": "v1",
  "Header 2": "Retrieve a transfer",
  "Header 1": "Transfers"
}
```

**Content:**
> Retrieve a transfer
> **GET /api/v1.0/transfers/:id**
> 
> **Example Response:**
> 
> .. code-block:: json
> 
>    {
>      "status": "success",
>      "api_version": "1.0",
>      "data": {
>        "id": "tr_12345",
>        "object": "transfer",
>        "amount_in_cents": 400,
>        "currency_code": "usd",
>        "recipient_id": "acct_9876",
>        "is_reversed": false
>      }
>    }

---

### Chunk 308 | ID: `1f7091be-02da-411f-9849-50a356169c4c`

**Metadata:**
```json
{
  "Header 1": "Transfers",
  "api_class": "TRANSFERS",
  "Header 2": "List all transfers",
  "version": "v1"
}
```

**Content:**
> List all transfers
> **GET /api/v1.0/transfers**
> 
> **Parameters:**
> 
> * **recipient_id** (string, optional): Only return transfers for the destination specified by this account ID.
> * **max_results** (integer, optional): A limit on the number of objects to be returned. Default is 10.

---

### Chunk 309 | ID: `08cdb6a4-d091-4b87-874b-3cf5da4f6a3c`

**Metadata:**
```json
{
  "version": "v2",
  "Header 1": "Transfers",
  "api_class": "TRANSFERS"
}
```

**Content:**
> A `Transfer` object is created when you move funds between Stripe accounts as part of Connect.

---

### Chunk 310 | ID: `f5844945-0ebc-42d6-891c-df4afd89d75d`

**Metadata:**
```json
{
  "api_class": "TRANSFERS",
  "Header 1": "Transfers",
  "Header 2": "The Transfer Object",
  "version": "v2"
}
```

**Content:**
> - `id` (string): Unique identifier for the object.
> - `object` (string): String representing the object’s type. Always has the value `transfer`.
> - `amount` (integer): Amount in cents to be transferred.
> - `amount_reversed` (integer): Amount in cents reversed (can be less than the amount attribute on the transfer if a partial reversal was issued).
> - `balance_transaction` (string, nullable): Balance transaction that describes the impact of this transfer on your account balance.
> - `created` (timestamp): Time that this record of the transfer was first created.
> - `currency` (enum): Three-letter ISO currency code, in lowercase.
> - `description` (string, nullable): An arbitrary string attached to the object. Often useful for displaying to users.
> - `destination` (string): ID of the Stripe account the transfer was sent to.
> - `destination_payment` (string, nullable): If the destination is a Stripe account, this will be the ID of the payment that the destination account received for the transfer.

---

### Chunk 311 | ID: `01023166-784a-4fb6-91c1-7f8f38b8645e`

**Metadata:**
```json
{
  "Header 1": "Transfers",
  "version": "v2",
  "api_class": "TRANSFERS",
  "Header 2": "The Transfer Object"
}
```

**Content:**
> - `livemode` (boolean): If the object exists in live mode, the value is `true`. If the object exists in test mode, the value is `false`.
> - `metadata` (object): Set of key-value pairs that you can attach to an object.
> - `reversed` (boolean): Whether the transfer has been fully reversed. If the transfer is only partially reversed, this attribute will still be false.
> - `source_transaction` (string, nullable): ID of the charge that was used to fund the transfer. If null, the transfer was funded from the available balance.
> - `source_type` (string, nullable): The source balance this transfer came from. One of `card`, `fpx`, or `bank_account`.
> - `transfer_group` (string, nullable): A string that identifies this transaction as part of a group.

---

### Chunk 312 | ID: `bfc4e512-ad35-44f3-a3a9-ab02ab0eae78`

**Metadata:**
```json
{
  "Header 3": "Create a transfer",
  "Header 1": "Transfers",
  "api_class": "TRANSFERS",
  "version": "v2",
  "Header 2": "Endpoints"
}
```

**Content:**
> **POST /v1/transfers**  
> To send funds from your Stripe account to a connected account, you create a new transfer object.  
> **Parameters:**  
> - `amount` (integer, required): A positive integer in cents representing how much to transfer.
> - `currency` (enum, required): Three-letter ISO code for currency in lowercase.
> - `destination` (string, required): The ID of a connected Stripe account.
> - `description` (string, optional): An arbitrary string attached to the object.
> - `metadata` (object, optional): Set of key-value pairs that you can attach to an object.
> - `source_transaction` (string, optional): You can use this parameter to transfer funds from a charge before they are added to your available balance.
> - `source_type` (string, optional): The source balance to use for this transfer. One of `bank_account`, `card`, or `fpx`.
> - `transfer_group` (string, optional): A string that identifies this transaction as part of a group.

---

### Chunk 313 | ID: `50351ccf-bfc3-4f3e-906b-68b98d990b37`

**Metadata:**
```json
{
  "Header 3": "Retrieve a transfer",
  "Header 2": "Endpoints",
  "api_class": "TRANSFERS",
  "version": "v2",
  "Header 1": "Transfers"
}
```

**Content:**
> **GET /v1/transfers/:id**  
> Retrieves the details of an existing transfer. Supply the unique transfer ID from either a transfer creation request or the transfer list, and Stripe will return the corresponding transfer information.

---

### Chunk 314 | ID: `96cbb55e-0ed0-480a-bb5f-dd4ca5db1c61`

**Metadata:**
```json
{
  "version": "v2",
  "api_class": "TRANSFERS",
  "Header 1": "Transfers",
  "Header 3": "List all transfers",
  "Header 2": "Endpoints"
}
```

**Content:**
> **GET /v1/transfers**  
> Returns a list of existing transfers sent to connected accounts. The transfers are returned in sorted order, with the most recently created transfers appearing first.  
> **Parameters:**  
> - `created` (object, optional): Only return transfers that were created during the given date interval (supports `gt`, `gte`, `lt`, `lte`).
> - `destination` (string, optional): Only return transfers for the destination specified by this account ID.
> - `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
> - `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
> - `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.
> - `transfer_group` (string, optional): Only return transfers with the specified transfer group.

---

