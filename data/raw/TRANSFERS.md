# Transfers

A `Transfer` object is created when you move funds between Stripe accounts as part of Connect.

## The Transfer Object

- `id` (string): Unique identifier for the object.
- `object` (string): String representing the object’s type. Always has the value `transfer`.
- `amount` (integer): Amount in cents to be transferred.
- `amount_reversed` (integer): Amount in cents reversed (can be less than the amount attribute on the transfer if a partial reversal was issued).
- `balance_transaction` (string, nullable): Balance transaction that describes the impact of this transfer on your account balance.
- `created` (timestamp): Time that this record of the transfer was first created.
- `currency` (enum): Three-letter ISO currency code, in lowercase.
- `description` (string, nullable): An arbitrary string attached to the object. Often useful for displaying to users.
- `destination` (string): ID of the Stripe account the transfer was sent to.
- `destination_payment` (string, nullable): If the destination is a Stripe account, this will be the ID of the payment that the destination account received for the transfer.
- `livemode` (boolean): If the object exists in live mode, the value is `true`. If the object exists in test mode, the value is `false`.
- `metadata` (object): Set of key-value pairs that you can attach to an object.
- `reversed` (boolean): Whether the transfer has been fully reversed. If the transfer is only partially reversed, this attribute will still be false.
- `source_transaction` (string, nullable): ID of the charge that was used to fund the transfer. If null, the transfer was funded from the available balance.
- `source_type` (string, nullable): The source balance this transfer came from. One of `card`, `fpx`, or `bank_account`.
- `transfer_group` (string, nullable): A string that identifies this transaction as part of a group.

## Endpoints

### Create a transfer

**POST /v1/transfers**

To send funds from your Stripe account to a connected account, you create a new transfer object.

**Parameters:**

- `amount` (integer, required): A positive integer in cents representing how much to transfer.
- `currency` (enum, required): Three-letter ISO code for currency in lowercase.
- `destination` (string, required): The ID of a connected Stripe account.
- `description` (string, optional): An arbitrary string attached to the object.
- `metadata` (object, optional): Set of key-value pairs that you can attach to an object.
- `source_transaction` (string, optional): You can use this parameter to transfer funds from a charge before they are added to your available balance.
- `source_type` (string, optional): The source balance to use for this transfer. One of `bank_account`, `card`, or `fpx`.
- `transfer_group` (string, optional): A string that identifies this transaction as part of a group.

### Retrieve a transfer

**GET /v1/transfers/:id**

Retrieves the details of an existing transfer. Supply the unique transfer ID from either a transfer creation request or the transfer list, and Stripe will return the corresponding transfer information.

### List all transfers

**GET /v1/transfers**

Returns a list of existing transfers sent to connected accounts. The transfers are returned in sorted order, with the most recently created transfers appearing first.

**Parameters:**

- `created` (object, optional): Only return transfers that were created during the given date interval (supports `gt`, `gte`, `lt`, `lte`).
- `destination` (string, optional): Only return transfers for the destination specified by this account ID.
- `ending_before` (string, optional): A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list.
- `limit` (integer, optional): A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
- `starting_after` (string, optional): A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list.
- `transfer_group` (string, optional): Only return transfers with the specified transfer group.
