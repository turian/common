"""
Moving average.

Yoshua Bengio:

    My preferred style of moving average is the following. Let's say you
    have a series x_t and you want to estimate the mean m of previous
    (recent) x's:

    m <-- m - (2/t) (m - x_t)

    Note that with (1/t) learning rate instead of (2/t) you get the exact
    historical average. With a larger learning rate (like 2/t) you give
    a bit more importance to recent stuff, which makes sense if x's are
    non-stationary (very likely here [in the setting of computing the
    moving average of the training error]). With a constant learning rate
    (independent of t) you get an exponential moving average.

    You can estimate a running average of the gradient variance by running
    averages of the mean gradient and of the
    square of the difference to the moving mean.

"""

import math

class MovingAverage:
    """
    .mean and .variance expose the moving average estimates.
    """
    def __init__(self, percent=False):
        self.mean = 0.
        self.variance = 0
        self.cnt = 0
        self.percent = percent
    def add(self, v):
        """
        Add value v to the moving average.
        """
        self.cnt += 1
        self.mean = self.mean - (2. / self.cnt) * (self.mean - v)
        # I believe I should compute self.variance AFTER updating the moving average, because
        # the estimate of the mean is better.
        # Yoshua concurs.
        this_variance = (v - self.mean) * (v - self.mean)
        self.variance = self.variance - (2. / self.cnt) * (self.variance - this_variance)
    def __str__(self):
        if self.percent:
            return "(moving average): mean=%.3f%% stddev=%.3f" % (self.mean, math.sqrt(self.variance))
        else:
            return "(moving average): mean=%.3f stddev=%.3f" % (self.mean, math.sqrt(self.variance))
    def verbose_string(self):
        if self.percent:
            return "(moving average): mean=%g%% stddev=%g" % (self.mean, math.sqrt(self.variance))
        else:
            return "(moving average): mean=%g stddev=%g" % (self.mean, math.sqrt(self.variance))
