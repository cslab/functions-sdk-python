### Version 0.7.2
- Fix: removed (broken) logging redirect (will be handled by the runtime instead)

### Version 0.7.1
- Enhancement: The objects `document` and `ec` now contain the attribute `cdb_object_id`.

### Version 0.7.0
- Feature: Functions no longer need to explicitly return a `Response` object.
- Feature: The `event_id` of `Response` objects is now filled in automatically before the response is returned.
