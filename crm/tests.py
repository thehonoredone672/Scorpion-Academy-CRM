from django.test import TestCase
from .models import Branch

class BranchModelTest(TestCase):
    def setUp(self):
        Branch.objects.create(name="Test Dojo", slug="test-dojo", password="123", instructor="Test User")

    def test_branch_creation(self):
        branch = Branch.objects.get(slug="test-dojo")
        self.assertEqual(branch.name, "Test Dojo")