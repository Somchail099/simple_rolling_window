# simple_rolling_window

A bounded rolling window over a stream of numbers that reports the mean, peak and trough of the most recent values.

```python
from simple_rolling_window import RollingWindow

window = RollingWindow(3)
window.push(1)
window.push(3)
window.push(2)

window.mean()    # 2.0
window.peak()    # 3
window.trough()  # 1

window.push(10)
window.values()  # (3, 2, 10)
window.mean()    # 5.0
window.peak()    # 10
window.trough()  # 2
```

## Why this exists

Computing a running average by keeping every value you have ever seen is wasteful when you only care about a recent slice. This library keeps exactly the last *n* values and maintains the sum incrementally, so `mean()` is O(1) and `push()` is O(1).

The trade-off: `peak()` and `trough()` scan the window on every call, which is O(n). For the small window sizes this class is meant for (think tens to low hundreds of samples) that is simpler and faster in practice than maintaining two monotonic deques. If you need O(1) extremes over a window of millions, use a different structure.

## API

- `RollingWindow(size)` — create a window holding at most `size` values. `size` must be a positive integer.
- `window.push(value)` — add a number, evicting the oldest if the window is full.
- `window.mean()` — arithmetic mean of the current values.
- `window.peak()` — maximum of the current values.
- `window.trough()` — minimum of the current values.
- `window.values()` — tuple of the current values, oldest first.
- `window.clear()` — empty the window.
- `len(window)` — number of values currently held.
- `window.size` — the configured capacity.

## Edge cases

Calling `mean()`, `peak()` or `trough()` on an empty window raises `ValueError`. Returning `0.0` for an empty window would silently poison any downstream average, so the library refuses instead.

`push()` rejects booleans even though `bool` is a subclass of `int` in Python. Passing `True` as `1` is almost always a bug at the call site, and failing loudly is cheaper than debugging a wrong mean later.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

