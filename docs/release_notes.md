

### Unreleased
- Automatically return an `EmptyResponse` if a Function has no return value. This means that it is no longer necessary to explicitly return a `Response` object from every Function.
- The `event_id` of `Response` objects is now filled in automatically before the response is returned.
