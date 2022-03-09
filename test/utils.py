def assert_values_trend(values: list, trend: str) -> None or AssertionError:
    """Asserts that a vector of values follows a given trend

    Args:
        values: values whose trend is to be checked
        trend: one of ('increasing', 'decreasing', 'non-monotonic')
    """
    if trend == 'increasing':
        assert all([x <= y for x, y in zip(values, values[1:])])
    elif trend == 'decreasing':
        assert all([x >= y for x, y in zip(values, values[1:])])
    elif trend == 'non-monotonic':
        assert (not all([x <= y for x, y in zip(values, values[1:])]) and
                not all([x >= y for x, y in zip(values, values[1:])]))
