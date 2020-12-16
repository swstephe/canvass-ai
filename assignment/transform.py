# -*- coding: utf8 -*-
from datetime import datetime, timezone


def transform_string(value):
    if value is None:
        return None
    return str(value)


def transform_numeric(value):
    if value is None or isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            pass
    return None


def transform_datetime(value):
    _value = transform_numeric(value)
    if _value is not None:
        return int(_value * 1000)
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value)
        return int(dt.timestamp() * 1000)
    except ValueError:
        pass
    return None


def transform_value(value):
    return dict(
        string=transform_string(value),
        numeric=transform_numeric(value),
        datetime=transform_datetime(value)
    )


def transform(data):
    return dict(
        source=data['deviceId'],
        timestamp=transform_datetime(data['timestamp']),
        data=dict(
            (k, transform_value(v))
            for k, v in data.items()
            if k not in ('deviceId', 'timestamp')
        )
    )
