# Notes on Domain-Driven Design (DDD) and Pure Domain Objects

> Is the class in @3_crew/engineering_team/example_output_4o/accounts.py suitible as a pure domain object?
  ⎿  Read 3_crew/engineering_team/example_output_4o/accounts.py (243 lines)

⏺ No, the Account class is not suitable as a pure domain object because it has dependencies on external functions (get_share_price) that are passed as parameters to multiple
  methods.

  Issues that prevent it from being a pure domain object:

  1. External dependency injection - Methods like buy_shares, sell_shares, get_portfolio_value, and get_profit_or_loss require a get_share_price callable to be passed in, making
  the domain logic dependent on infrastructure concerns
  2. Inconsistent state - The initial_deposit tracking (lines 22, 40-41) is fragile and only works if deposits happen before other transactions

  To make it a pure domain object, you would need to:

- Remove the get_share_price parameter dependencies
- Either store prices at transaction time (snapshot approach) or calculate portfolio values differently
- Make the initial deposit explicit (e.g., via a dedicated initialization parameter or method)
- Keep all business logic self-contained without external function dependencies

  A pure domain object should encapsulate its business rules and state without relying on external services or functions for core operations.
