import unittest

from simple_rolling_window import RollingWindow


class RollingWindowTests(unittest.TestCase):
    def test_size_must_be_positive_integer(self):
        with self.assertRaises(ValueError):
            RollingWindow(0)
        with self.assertRaises(ValueError):
            RollingWindow(-1)
        with self.assertRaises(TypeError):
            RollingWindow(2.5)
        with self.assertRaises(TypeError):
            RollingWindow(True)

    def test_empty_window_raises(self):
        w = RollingWindow(3)
        self.assertEqual(len(w), 0)
        with self.assertRaises(ValueError):
            w.mean()
        with self.assertRaises(ValueError):
            w.peak()
        with self.assertRaises(ValueError):
            w.trough()

    def test_push_rejects_non_numbers(self):
        w = RollingWindow(3)
        with self.assertRaises(TypeError):
            w.push("1")
        with self.assertRaises(TypeError):
            w.push(None)
        with self.assertRaises(TypeError):
            w.push(True)

    def test_single_value(self):
        w = RollingWindow(5)
        w.push(7)
        self.assertEqual(len(w), 1)
        self.assertEqual(w.mean(), 7.0)
        self.assertEqual(w.peak(), 7)
        self.assertEqual(w.trough(), 7)

    def test_mean_peak_trough_before_full(self):
        w = RollingWindow(4)
        w.push(1)
        w.push(3)
        w.push(2)
        self.assertEqual(w.mean(), 2.0)
        self.assertEqual(w.peak(), 3)
        self.assertEqual(w.trough(), 1)

    def test_eviction_keeps_only_last_size_values(self):
        w = RollingWindow(3)
        for v in (1, 2, 3, 4, 5):
            w.push(v)
        self.assertEqual(w.values(), (3, 4, 5))
        self.assertEqual(len(w), 3)
        self.assertEqual(w.mean(), 4.0)
        self.assertEqual(w.peak(), 5)
        self.assertEqual(w.trough(), 3)

    def test_mean_is_float(self):
        w = RollingWindow(2)
        w.push(1)
        w.push(2)
        self.assertIsInstance(w.mean(), float)
        self.assertEqual(w.mean(), 1.5)

    def test_peak_and_trough_return_original_types(self):
        w = RollingWindow(3)
        w.push(1.5)
        w.push(2)
        w.push(0.5)
        self.assertEqual(w.peak(), 2)
        self.assertEqual(w.trough(), 0.5)

    def test_clear_resets_window(self):
        w = RollingWindow(3)
        w.push(1)
        w.push(2)
        w.clear()
        self.assertEqual(len(w), 0)
        self.assertEqual(w.values(), ())
        with self.assertRaises(ValueError):
            w.mean()

    def test_values_returns_tuple_copy(self):
        w = RollingWindow(3)
        w.push(1)
        w.push(2)
        vals = w.values()
        self.assertIsInstance(vals, tuple)
        w.push(3)
        self.assertEqual(vals, (1, 2))
        self.assertEqual(w.values(), (1, 2, 3))

    def test_size_property(self):
        w = RollingWindow(4)
        self.assertEqual(w.size, 4)

    def test_negative_and_zero_values(self):
        w = RollingWindow(3)
        w.push(-5)
        w.push(0)
        w.push(5)
        self.assertEqual(w.mean(), 0.0)
        self.assertEqual(w.peak(), 5)
        self.assertEqual(w.trough(), -5)

    def test_large_stream(self):
        w = RollingWindow(10)
        for i in range(100):
            w.push(i)
        self.assertEqual(w.values(), tuple(range(90, 100)))
        self.assertEqual(w.mean(), 94.5)
        self.assertEqual(w.peak(), 99)
        self.assertEqual(w.trough(), 90)


if __name__ == "__main__":
    unittest.main()
