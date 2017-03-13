"""
This module defines a more user-friendly json encoder, supporting time objects and UUID
"""
import json
from decimal import Decimal
from datetime import time, date, datetime
from uuid import UUID


class FriendlyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        if isinstance(obj, datetime):
            # NB: standardized ISO 8601-format. (browsers convert automatically UTC to local date times)
            # 2011-06-29T16:52:48.000Z
            return obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Decimal):
            #return float(obj)
            return float("{0:.4f}".format(obj))
        if hasattr(obj, "to_json") and callable(obj.to_json):
            return obj.to_json()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


# monkey patching json.dumps to use, by default, a user-friendly encoder
base_dumps = json.dumps


def serialize(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):
    if cls is None:
        cls = FriendlyEncoder
    return base_dumps(obj,
                      skipkeys=skipkeys,
                      ensure_ascii=ensure_ascii,
                      check_circular=check_circular,
                      allow_nan=allow_nan,
                      cls=cls,
                      indent=indent,
                      separators=separators,
                      default=default,
                      sort_keys=sort_keys,
                      **kw)
json.dumps = serialize


class JsonSerializable:

    def to_json(self):
        return serialize(self.__dict__)
