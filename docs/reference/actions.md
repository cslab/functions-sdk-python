Functions can return a list of "Actions" that should be performed in CIM Database Cloud. Not all Events support the same actions, so check the supported actions in the [Events documentation](events.md). For example Events that are triggered **after** the release of an object don't support AbortAndShowError, because the release can't be aborted anymore, however the "release check" events do support it.

### Return an Action:

Example:

```python
from csfunctions.actions import AbortAndShowErrorAction

def my_function(metadata, event, service):
    # this will show an error message to the user
    return AbortAndShowErrorAction(message="Custom error message.")
```

## AbortAndShowErrorAction

`csfunctions.actions.AbortAndShowErrorAction`

Aborts the current operation and shows an error message to the user.


**AbortAndShowErrorAction.name:** abort_and_show_error

**AbortAndShowErrorAction.message:** Error message that will be shown to the user
