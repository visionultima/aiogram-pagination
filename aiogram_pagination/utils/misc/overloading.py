import inspect


def _type_hint_matches(obj, hint):
    # only works with concrete types, not things like Optional
    return hint is inspect.Parameter.empty or isinstance(obj, hint)


def _signature_matches(sig: inspect.Signature,
                       bound_args: inspect.BoundArguments):
    # doesn't handle type hints on *args or **kwargs
    for name, arg in bound_args.arguments.items():
        param = sig.parameters[name]
        hint = param.annotation
        if not _type_hint_matches(arg, hint):
            return False
    return True


def overload(f):
    f.__overload__ = True
    return f


class OverloadList(list):
    pass


class Overload:
    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name

    def __init__(self, overload_list):
        if not isinstance(overload_list, OverloadList):
            raise TypeError('must use OverloadList')
        if not overload_list:
            raise ValueError('empty overload list')
        self.overload_list = overload_list
        self.signatures = [inspect.signature(f) for f in overload_list]

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.overload_list!r})'

    def __get__(self, instance, _owner=None):
        if instance is None:
            return self
        # don't use owner == type(instance)
        # we want self.owner, which is the class from which get is being called
        return BoundOverloadDispatcher(instance, self.owner, self.name,
                                       self.overload_list, self.signatures)

    def extend(self, other):
        if not isinstance(other, Overload):
            raise TypeError
        self.overload_list.extend(other.overload_list)
        self.signatures.extend(other.signatures)


class NoMatchingOverload(Exception):
    pass


class BoundOverloadDispatcher:
    def __init__(self, instance, owner_cls, name, overload_list, signatures):
        self.instance = instance
        self.owner_cls = owner_cls
        self.name = name
        self.overload_list = overload_list
        self.signatures = signatures

    def best_match(self, *args, **kwargs):
        for f, sig in zip(self.overload_list, self.signatures):
            try:
                bound_args = sig.bind(self.instance, *args, **kwargs)
            except TypeError:
                pass  # missing/extra/unexpected args or kwargs
            else:
                bound_args.apply_defaults()
                # just for demonstration, use the first one that matches
                if _signature_matches(sig, bound_args):
                    return f

        raise NoMatchingOverload()

    def __call__(self, *args, **kwargs):
        try:
            f = self.best_match(*args, **kwargs)
        except NoMatchingOverload:
            pass
        else:
            return f(self.instance, *args, **kwargs)

        # no matching overload in owner class, check next in line
        super_instance = super(self.owner_cls, self.instance)
        super_call = getattr(super_instance, self.name, _MISSING)
        if super_call is not _MISSING:
            return super_call(*args, **kwargs)
        else:
            raise NoMatchingOverload()


_MISSING = object()


class OverloadDict(dict):

    def __setitem__(self, key, value):
        assert isinstance(key, str), 'keys must be str'

        prior_val = self.get(key, _MISSING)
        overloaded = getattr(value, '__overload__', False)

        if prior_val is _MISSING:
            insert_val = OverloadList([value]) if overloaded else value
            super().__setitem__(key, insert_val)
        elif isinstance(prior_val, OverloadList):
            if not overloaded:
                raise ValueError(self._errmsg(key))
            prior_val.append(value)
        else:
            if overloaded:
                raise ValueError(self._errmsg(key))
            super().__setitem__(key, value)

    @staticmethod
    def _errmsg(key):
        return f'must mark all overloads with @overload: {key}'


class OverloadMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        return OverloadDict()

    def __new__(mcs, name, bases, namespace, **kwargs):
        overload_namespace = {
            key: Overload(val) if isinstance(val, OverloadList) else val
            for key, val in namespace.items()
        }
        return super().__new__(mcs, name, bases, overload_namespace, **kwargs)
