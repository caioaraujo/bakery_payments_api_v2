from django.test import TestCase

from ..models import Branch


class TestBranch(TestCase):

    def test_str(self):
        branch = Branch(name='Branch Test')

        self.assertEqual('Branch Test', str(branch))
