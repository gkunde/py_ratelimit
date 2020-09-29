import logging
import math
import time


class RateLimit:
    """
    A process rate limiter. Tracking the number of times a counter is
    triggered. Then performing a wait when the number of triggers
    exceeds the number allowed for a given time period.

    :param max_triggers: The maximum number of triggers allowed per period.

    :param max_period: The maximum number of seconds for a period.

    :type max_triggers: int

    :type max_period: int
    """

    def __init__(self, max_triggers, max_period):
        """
        """

        self.__logger = logging.getLogger("ratelimit.RateLimit")

        self.__counter = []

        # When checking for cooldown, prevent infinite loop with a max number of iterations.
        self._max_checks = 100

        self.max_triggers = int(max_triggers)
        self.max_period = int(max_period)

    def __len__(self):
        return len(self.__counter)

    def trigger(self):
        """
        Called each time an operation is to be counted. When the max number of
        triggers has been reached, the method will sleep until the number of
        triggers falls below the max_triggers value.

        :rtype: None
        """

        self.__logger.debug("trigger()")

        # prevent infinite loops on when checking for cooldown.
        itr = 0

        self.__remove_expired_triggers()

        while self.__check_cooldown() and itr < self._max_checks:
            # Too many triggers are counted, start cooldown period.

            self.__cooldown()

            self.__remove_expired_triggers()

            itr += 1

        if self.__check_cooldown():
            # Still require cooldown, must have exceeded self._max_checks interations in while loop.
            raise RuntimeError("RateLimit timeout, unable to clear expired counts.")

        self.__add_trigger()

        return None

    def __check_cooldown(self):
        """
        Check if cooldown is needed.

        This method intended to be called by trigger() method.

        :returns: True when the counter exceeds the max_triggers attribute.

        :rtype: bool
        """

        self.__logger.debug("__check_cooldown()")

        return self.max_triggers <= len(self.__counter)

    def __cooldown(self):
        """
        Calculates and then sleeps the necassary amount of time for oldest
        trigger to expire.

        This method intended to be called by trigger() method.

        :rtype: None
        """

        self.__logger.debug("__cooldown()")

        wait_time = (min(self.__counter) + self.max_period) - time.time()

        # If max_period is set to 0 or too small, the wait will be negative.
        wait_time = int(math.ceil(max(wait_time, 0)))

        if wait_time > 0:

            self.__logger.info("Rate limit reached, waiting %s second(s)" % (wait_time, ))

            time.sleep(wait_time)

        return None

    def __remove_expired_triggers(self):
        """
        Remove all expired triggers from the counter.

        This method intended to be called by trigger() method.

        :rtype: None
        """

        self.__logger.debug("__remove_expired_triggers()")

        expire_ts = time.time() - self.max_period

        self.__counter = [ts for ts in self.__counter if ts >= expire_ts]

        return None

    def __add_trigger(self):
        """
        Records the current timestamp and adds it to the list of triggers.

        This method intended to be called by trigger() method.

        :rtype: None
        """

        self.__logger.debug("__add_trigger()")

        self.__counter.append(time.time())

        return None
