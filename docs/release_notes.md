### Version 0.12.0:
Breaking changes:

- Changed the names of the events and their classes, to be more consistent:

  - `DocumentReleaseEvent` -> `DocumentReleasedEvent`

  - `PartReleaseEvent` -> `PartReleasedEvent`

  - `EngineeringChangeRelease` -> `EngineeringChangeReleasedEvent`

  - `EngineeringChangeCheck`> `EngineeringChangeCheckEvent`

- Event data now consistently uses the attributes `parts` and `documents` instead of `linked_parts` or `attached_parts`

### Version 0.11.1:
- Fix: crash when using pydantic>=2.11

### Version 0.11.0:
- Feature: Added Document and Part field calculation events.

### Version 0.10.0:
- Feature: Added development server that can be used to run Functions locally for testing and development.

### Version 0.9.0:
- Feature: Added new "Create Check" and "Modify Check" events for Documents, Parts and Engineering Changes, which are triggered before an object is created or modified and allow the creation or modification to be aborted by returning an Action.

### Version 0.8.4:
- Add MyPy support

### Version 0.8.3:
- added the fields `short_name`, `application` and `remark` to Material

### Version 0.8.2:
- added the fields `teilenummer`and `t_index` to BOMItem

### Version 0.8.1:
- Fix: removed incorrect dependency to urllib3

### Version 0.8.0:

- Feature: New "Release Check" events for Documents, Parts and Engineering Changes, which are triggered before an object is released and allow the release to be aborted by returning an Action.

- Feature: Actions can be returned by a Function to perform actions in CIM Database in response to an event. The first new Action `AbortAndShowErrorAction` can be used to abort the current operation in CIM Database, e.g. to abort a release process if certain conditions are not met.


### Version 0.7.2
- Fix: removed (broken) logging redirect (will be handled by the runtime instead)

### Version 0.7.1
- Enhancement: The objects `document` and `ec` now contain the attribute `cdb_object_id`.

### Version 0.7.0
- Feature: Functions no longer need to explicitly return a `Response` object.
- Feature: The `event_id` of `Response` objects is now filled in automatically before the response is returned.
