# Prices

Prices define the unit cost, currency, and (optional) billing cycle for both recurring and one-time purchases of products. Different physical goods or levels of service should be represented by products, and pricing options should be represented by prices.

## The Price Object

- `id` (string): Unique identifier for the object.
- `object` (string): String representing the object’s type. Always has the value `price`.
- `active` (boolean): Whether the price can be used for new purchases.
- `created` (timestamp): Time at which the object was created.
- `currency` (enum): Three-letter ISO currency code, in lowercase.
- `lookup_key` (string, nullable): A lookup key used to retrieve prices dynamically from a static string.
- `metadata` (object): Set of key-value pairs that you can attach to an object.
- `product` (string): The ID of the product this price is associated with.
- `recurring` (object, nullable): The recurring components of a price such as `interval` and `usage_type`.
  - `recurring.interval` (enum): The frequency at which a subscription is billed. One of `day`, `week`, `month` or `year`.
  - `recurring.interval_count` (integer): The number of intervals between subscription billings.
- `type` (enum): One of `one_time` or `recurring` depending on whether the price is for a one-time purchase or a recurring (subscription) purchase.
- `unit_amount` (integer, nullable): The unit amount in cents to be charged.

## Endpoints

### Create a price

**POST /v1/prices**

Creates a new Price for an existing Product. The Price can be recurring or one-time.

**Parameters:**

- `currency` (enum, required): Three-letter ISO currency code, in lowercase.
- `unit_amount` (integer, required conditionally): A positive integer in cents (or 0 for a free price) representing how much to charge.
- `product` (string, required unless product_data is provided): The ID of the Product that this Price will belong to.
- `product_data` (object, required unless product is provided): These fields can be used to create a new product that this price will belong to.
  - `product_data.name` (string, required): The product’s name, meant to be displayable to the customer.
- `recurring` (object, optional): The recurring components of a price such as `interval` and `usage_type`.
  - `recurring.interval` (enum, required): Specifies billing frequency. Either `day`, `week`, `month` or `year`.
- `active` (boolean, optional): Whether the price can be used for new purchases.
- `lookup_key` (string, optional): A lookup key used to retrieve prices dynamically from a static string.
- `metadata` (object, optional): Set of key-value pairs that you can attach to an object.

### Retrieve a price

**GET /v1/prices/:id**

Retrieves the price with the given ID.

### List all prices

**GET /v1/prices**

Returns a list of your active prices.

**Parameters:**

- `active` (boolean, optional): Only return prices that are active or inactive (e.g., pass `false` to list all inactive prices).
- `currency` (enum, optional): Only return prices for the given currency.
- `product` (string, optional): Only return prices for the given product.
- `type` (enum, optional): Only return prices of type `recurring` or `one_time`.
- `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100.
- `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
- `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.
