# aiogram-pagination


*This module will help you create layered callback menus.
The module is based on the concept that each callback has all the preceding callbacks in it.*

***

### INSTALLATION
> pip install aiogram-pagination
***

### QUICK START


To create callbacks you need to use the callback factory from 
the aiogram-pagination module

```python
from aiogram_pagination.utils.callback_stack_factory import CallbackStackFactory
cb = CallbackStackFactory('foo', 'bar')
```

You can use both the simple version of the callback stack
and the version with abbreviated callbacks.

Simple version:
```python
from aiogram_pagination.callback_stack import SimpleCallbackStack


callback_stack = SimpleCallbackStack(callback_data={'foo': 0, 'bar': 1, 'previous': ''},
                                     callback_factory=cb)
callback_stack.next(callback_data={'foo': 6, 'bar': 6},
                    callback_factory=cb)
callback_stack.previous()
```

Version with abbreviation:

```python
from aiogram_pagination.callback_stack import AbbreviatedCallbackStack


callback_stack = AbbreviatedCallbackStack(
    callback_data={'foo': 0, 'bar': 1, 'previous': ''},
    callback_factory=cb
)

callback_stack.next(callback_data={'foo': 6, 'bar': 6},
                    callback_factory=cb)
callback_stack.previous(default='some:callback')
```

***

### CONFIGURATION
For configuration, you can use any configuration file placed 
in the root directory of the project or in the data folder.

The module uses configs under the "callback stack" key.
the default is config.json in the data folder of the aiogram-pagination module.

Example:

```json
{
  "callback_stack":
  {
      "storage": "sqlite",
      "cache_time_limit": 3600,
      "max_pagination_depth": false,
      "redis_db": 1
  }
}
```
 