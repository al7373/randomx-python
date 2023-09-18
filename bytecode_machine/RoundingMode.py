RoundToNearest = 0
RoundDown = 1
RoundUp = 2
RoundToZero = 3

_rounding_mode = RoundToNearest

def rx_set_rounding_mode(mode: int) -> None:
    global _rounding_mode
    _rounding_mode = mode

def rx_get_rounding_mode() -> int:
    global _rounding_mode
    return _rounding_mode

