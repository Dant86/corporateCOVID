from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from forum.models import Industry, Company, Post, User, Comment

class IndustryTestCase(TestCase):
    def setUp(self):
        Industry.objects.create(industry_field='Aviation')
        Industry.objects.create(industry_field='Technology')

    def test_existence(self):
        # check to see if objects exist
        aviation = Industry.objects.get(industry_field='Aviation')
        tech = Industry.objects.get(industry_field='Technology')

        # make sure names aren't corrupted
        self.assertEqual(aviation.industry_field, 'Aviation')
        self.assertEqual(tech.industry_field, 'Technology')
