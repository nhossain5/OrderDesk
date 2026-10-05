# OrderDesk requirements

Every test references one of these IDs. The `req_id` column in `tests/data/orders.csv` and each test's docstring provide the traceability.

| ID | Requirement |
| --- | --- |
| REQ-01 | Users log in with username and password; wrong credentials show "Invalid username or password". |
| REQ-02 | Two roles: *trader* can submit and cancel orders; *viewer* can only view. |
| REQ-03 | Symbol must be one of: ABC1, DEF2, GHI3, JKL4, MNO5. |
| REQ-04 | Side is Buy or Sell. |
| REQ-05 | Quantity is a whole number from 1 to 10,000. |
| REQ-06 | Order type is Market or Limit; Limit requires a price. |
| REQ-07 | Limit price is greater than 0 with at most 2 decimals; Market orders must not include a price. |
| REQ-08 | New orders appear in the blotter with status NEW. |
| REQ-09 | A trader can cancel a NEW order; a cancelled order cannot be cancelled again. |
| REQ-10 | The API enforces the same rules as the UI and returns 422 with a clear message on bad input. |
| REQ-11 | API calls without a valid session return 401. |
