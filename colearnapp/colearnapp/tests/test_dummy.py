"""
Test module of ColearnApp project.
"""
from unittest import TestCase

class DummyTests(TestCase):
    """
    A class containing dummy tests to integrate with CI pipeline.
    """
    def test_is_ci_pipeline_working(self):
        """
        Is CI pipeline working properly? This test should be deleted
        after creating real tests.
        """
        self.assertEqual(True, True)
