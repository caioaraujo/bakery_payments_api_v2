from django.test import SimpleTestCase

from ..models import Branch


class TestBranch(SimpleTestCase):

    def test_str(self):
        branch = Branch(name='Branch Test')

        self.assertEqual('Branch Test', str(branch))
