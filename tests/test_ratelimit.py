import time
import unittest

import ratelimit


class Test_RateLimit(unittest.TestCase):

    def test_adding_triggers(self):
        """
        Verify that all trggers are added. Long period to ensure nothing is
        expired before the last trigger is added.
        """

        num_request = 5

        obj = ratelimit.RateLimit(10, 300)

        for _ in range(num_request):
            obj.trigger()

        self.assertEqual(num_request, len(obj))

    def test_expiring_triggers(self):
        """
        Verify that old triggers are expired if the time between triggers
        exceeds the max_period value.
        """

        num_request = 2

        obj = ratelimit.RateLimit(10, 2)

        for _ in range(num_request):
            obj.trigger()
            time.sleep(3)

        self.assertEqual(num_request - 1, len(obj))

    def test_wait_to_expire(self):
        """
        Verify that two many triggers will cause a wait and then removal of
        expired triggers.
        """

        num_request = 2

        obj = ratelimit.RateLimit(1, 2)

        start_time = time.time()

        for _ in range(num_request):
            obj.trigger()

        elapsed_time = time.time() - start_time

        self.assertEqual(num_request - 1, len(obj))
        self.assertLessEqual(2, elapsed_time)


if __name__ == '__main__':
    unittest.main()
