"""
MIT License

Copyright (c) 2022 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_ratelimit
"""
import time
import unittest

import ratelimit


class Test_RateLimit(unittest.TestCase):

    MAX_REQUESTS = 4
    PERIOD = 5

    def test_init(self):

        obj = ratelimit.RateLimit(self.MAX_REQUESTS, self.PERIOD)

        self.assertEqual(obj.max_count, self.MAX_REQUESTS)
        self.assertEqual(obj.period, self.PERIOD)
    
    def test_check(self):

        obj = ratelimit.RateLimit(self.MAX_REQUESTS, self.PERIOD)

        start = time.time()
        for _ in range(self.MAX_REQUESTS + 1):

            obj.check()
        
        total_time = time.time() - start
        
        self.assertGreaterEqual(total_time, self.PERIOD)

if __name__ == '__main__':
    unittest.main()
