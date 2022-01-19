# aiogram-pagination

*This module will help you create layered callback menus. The module is based on the concept that each callback has all
the preceding callbacks in it.*

***

### INSTALLATION

> pip install aiogram-pagination
> 
For Poetry:
>poetry add aiogram-pagination 
***

### QUICK START

To create callbacks you need to use the callback factory from the aiogram-pagination module

```python
from aiogram_pagination.utils.callback_stack_factory import CallbackStackFactory

cb = CallbackStackFactory('foo', 'bar')
```

You can use both the simple version of the callback stack and the version with abbreviated callbacks.

Simple version:

```python
from aiogram_pagination.callback_chain import CallbackChain

callback_chain = CallbackChain(query=cb.new(foo=1, bar=2),
                                     factory=cb)
callback_chain.next(cb.new('previous', foo='42', bar='624'))
callback_chain.previous()
callback_chain.edit_current_callback_query(cb.new(foo='0', bar='3', previous=''))
```

Version with compression:

```python
from aiogram_pagination.callback_chain.compression import CompressedCallbackChain

callback_chain = CompressedCallbackChain(
    data={'foo': 0, 'bar': 1, 'previous':''},
    factory=cb
)

callback_chain.next(cb.new(foo=2, bar=3))
callback_chain.previous(default='some:callback:query')
```

***

### CONFIGURATION

For configuration, you can use any configuration file placed in the root directory of the project or in the data folder.

The module uses configs under the "callback stack" and "callback storage" keys. The default is config.json in the data folder of the
aiogram-pagination module.

Example:

```json
{
  "callback_stack": {
    "max_pagination_depth": false
  },
  "callback_storage": {
    "storage": "redis",
    "cache_time_limit": 3600,
    "redis_db": 1
  }
}
```
 