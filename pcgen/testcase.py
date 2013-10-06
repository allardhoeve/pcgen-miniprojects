import unittest
import mock


class TestCase(unittest.TestCase):
    """
    Test case for basic testing

    It provides the same functionality as unittest.TestCase, but it has the
    additional functionality of setUpPatch, which sets up a mock.patch using
    patchers and configures teardown of the patches as well.
    """

    def set_up_patch(self, topatch, themock=None):
        if themock is None:
            themock = mock.Mock()

        patcher = mock.patch(topatch, themock)
        self.addCleanup(patcher.stop)
        return patcher.start()
