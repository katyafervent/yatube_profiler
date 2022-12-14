import collections
import decimal
import functools
import time
from typing import Any, Callable, Optional

from django.core.management import BaseCommand
from django.db import connection, reset_queries


def show_time(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        _self: BaseCommand = args[0]
        start_time = time.time()
        result = func(*args, **kwargs)
        diff = time.time() - start_time
        message = (f'Время выполнения функции {func.__name__}: {diff:.3f}')
        if isinstance(_self, BaseCommand):
            _self.stdout.write(message)
        else:
            print(message)
        return result
    return wrapper


def _set_field_attributes(
    wrapper: Callable, label: Optional[str], short_description: Optional[str], kwargs: Any
) -> None:
    if label is None and short_description is not None:
        label = short_description
    if label is not None:
        wrapper.label = label  # type: ignore
        wrapper.short_description = short_description  # type: ignore

    for key, value in kwargs.items():
        setattr(wrapper, key, value)


def admin_field(label: str = None, short_description: str = None, **kwargs: Any) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            return func(*args, **kwargs)

        _set_field_attributes(wrapper, label, short_description, kwargs)
        return wrapper

    return decorator


def queries_stat(fn: Callable) -> Callable:

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        reset_queries()
        # start_t = time.time()
        original_return = fn(*args, **kwargs)
        # print('TOTAL EXECUTION TIME:', time.time() - start_t)
        queries = connection.queries
        total_queries_time = decimal.Decimal(0)
        total_queries_count = 0
        stats: Any = collections.defaultdict(lambda: dict())
        for query in queries:
            total_queries_time += decimal.Decimal(query['time'])
            total_queries_count += 1
            if query['sql'] in stats:
                stats[query['sql']]['time'] += decimal.Decimal(query['time'])
                stats[query['sql']]['count'] += 1
            else:
                stats[query['sql']]['time'] = decimal.Decimal(query['time'])
                stats[query['sql']]['count'] = 1
        print(f'TOTAL QUERIES STATS. COUNT: {total_queries_count} TIME: {total_queries_time}')
        # print('TOP 10 QUERIES BY COUNT')
        # for sql, stat in sorted(stats.items(), key=lambda elem: elem[1]['count'], reverse=True)[:10]:
        #     print(stat['count'], sql)
        print('TOP 10 QUERIES BY TIME')
        for sql, stat in sorted(stats.items(), key=lambda elem: elem[1]['time'], reverse=True)[:10]:
            print(stat['time'], sql)
        # print('\n')
        return original_return

    return wrapper
