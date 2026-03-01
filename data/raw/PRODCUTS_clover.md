# Products

Products describe the specific goods or services you offer to your customers. They can be used in conjunction with Prices to configure pricing in Payment Links, Checkout, and Subscriptions.

## The Product Object

- `id` (string): Unique identifier for the object.
- `object` (string): String representing the object’s type. Always has the value `product`.
- `active` (boolean): Whether the product is currently available for purchase.
- `created` (timestamp): Time at which the object was created. Measured in seconds since the Unix epoch.
- `default_price` (string, nullable): The ID of the Price object that is the default price for this product.
- `description` (string, nullable): The product’s description, meant to be displayable to the customer.
- `livemode` (boolean): If the object exists in live mode, the value is `true`. If the object exists in test mode, the value is `false`.
- `metadata` (object): Set of key-value pairs that you can attach to an object.
- `name` (string): The product’s name, meant to be displayable to the customer.
- `shippable` (boolean, nullable): Whether this product is shipped (i.e., physical goods).
- `statement_descriptor` (string, nullable): Extra information about a product which will appear on your customer’s credit card statement. Only used for subscription payments.
- `updated` (timestamp): Time at which the object was last updated.

## Endpoints

### Create a product

**POST /v1/products**

Creates a new product object.

**Parameters:**

- `name` (string, required): The product’s name, meant to be displayable to the customer.
- `active` (boolean, optional): Whether the product is currently available for purchase. Defaults to `true`.
- `description` (string, optional): The product’s description, meant to be displayable to the customer.
- `default_price_data` (object, optional): Data used to generate a new Price object. This Price will be set as the default price for this product.
  - `default_price_data.currency` (enum, required): Three-letter ISO currency code, in lowercase.
  - `default_price_data.unit_amount` (integer, required conditionally): A positive integer in cents (or 0 for a free price) representing how much to charge.
  - `default_price_data.recurring` (object, optional): The recurring components of a price such as `interval` and `interval_count`.
    - `default_price_data.recurring.interval` (enum, required): Specifies billing frequency. Either `day`, `week`, `month` or `year`.
- `metadata` (object, optional): Set of key-value pairs that you can attach to an object.
- `shippable` (boolean, optional): Whether this product is shipped (i.e., physical goods).
- `statement_descriptor` (string, optional): An arbitrary string to be displayed on your customer’s credit card or bank statement. Only used for subscription payments.

### Retrieve a product

**GET /v1/products/:id**

Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.

### List all products

**GET /v1/products**

Returns a list of your products. The products are returned sorted by creation date, with the most recently created products appearing first.

**Parameters:**

- `active` (boolean, optional): Only return products that are active or inactive (e.g., pass `false` to list all inactive products).
- `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
- `ids` (array of strings, optional): Only return products with the given IDs.
- `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
- `shippable` (boolean, optional): Only return products that can be shipped (i.e., physical, not digital products).
- `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.
