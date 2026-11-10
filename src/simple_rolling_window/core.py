from collections import deque


class RollingWindow:
    """A bounded window over a stream of numbers.

    The window keeps the most recent ``size`` values.  It exposes the mean,
    peak (maximum) and trough (minimum) of those values.

    Why a deque?  A bounded deque gives O(1) appends and pops from both ends,
    which is exactly what a sliding window needs.  We also keep a running sum
    so that ``mean()`` is O(1).  Peak and trough are computed on demand by
    scanning the window; for the small window sizes this class is designed for
    that is faster than maintaining a monotonic queue and far simpler to
    reason about.
    """

    def __init__(self, size):
        """Create a window that holds at most ``size`` values.

        ``size`` must be a positive integer.  A window of size zero has no
        meaningful mean, peak or trough, so it is rejected up front rather
        than failing later in a confusing way.
        """
        if not isinstance(size, int) or isinstance(size, bool):
            raise TypeError("size must be an integer")
        if size <= 0:
            raise ValueError("size must be positive")
        self._size = size
        self._values = deque()
        self._sum = 0.0

    @property
    def size(self):
        """The maximum number of values the window holds."""
        return self._size

    def __len__(self):
        """The number of values currently in the window."""
        return len(self._values)

    def push(self, value):
        """Add ``value`` to the window, evicting the oldest if full.

        ``value`` must be a real number (int or float).  Booleans are rejected
        because ``True`` silently acting as ``1`` hides bugs at the call site.
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("value must be a number")
        if len(self._values) == self._size:
            self._sum -= self._values.popleft()
        self._values.append(value)
        self._sum += value

    def mean(self):
        """Mean of the values currently in the window.

        Raises ``ValueError`` if the window is empty, because the mean of no
        values is undefined and returning 0.0 would silently corrupt any
        downstream average.
        """
        if not self._values:
            raise ValueError("window is empty")
        return self._sum / len(self._values)

    def peak(self):
        """Maximum value currently in the window.

        Raises ``ValueError`` if the window is empty.
        """
        if not self._values:
            raise ValueError("window is empty")
        return max(self._values)

    def trough(self):
        """Minimum value currently in the window.

        Raises ``ValueError`` if the window is empty.
        """
        if not self._values:
            raise ValueError("window is empty")
        return min(self._values)

    def values(self):
        """A tuple of the values in the window, oldest first.

        Returning a tuple rather than the internal deque prevents callers from
        mutating the window's state by accident.
        """
        return tuple(self._values)

    def clear(self):
        """Remove all values from the window."""
        self._values.clear()
        self._sum = 0.0
