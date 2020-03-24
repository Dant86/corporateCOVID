from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from forum.models import Industry, Company, Post, User, Comment
from datetime import datetime

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

    def test_update(self):
        # check that db keeps track of updates
        aviation = Industry.objects.get(industry_field='Aviation')
        aviation.industry_field = 'Investment Banking'
        aviation.save()
        self.assertNotEqual(aviation.industry_field, 'Aviation')
        self.assertEqual(aviation.industry_field, 'Investment Banking')
        try:
            bad_obj = Industry.objects.get(industry_field='Aviation')
        except ObjectDoesNotExist:
            bad_obj = None
        self.assertIsNone(bad_obj)
        # The below line should return an error
        # if this doesn't exist. Expecting no error tho.
        good_obj = Industry.objects.get(industry_field='Investment Banking')

    def test_remove(self):
        # check that db keeps track of deletions
        aviation = Industry.objects.get(industry_field='Aviation')
        aviation.delete()
        self.assertEqual(len(Industry.objects.filter()), 1)

class CompanyTestCase(TestCase):
    def setUp(self):
        # set up industries
        IndustryTestCase().setUp()
        
        aviation = Industry.objects.get(industry_field='Aviation')
        tech = Industry.objects.get(industry_field='Technology')

        # add companies to db
        Company.objects.create(company_name='American Airlines',
                               industry_from=aviation)
        Company.objects.create(company_name='British Airways',
                               industry_from=aviation)
        Company.objects.create(company_name='Amazon',
                               industry_from=tech)
        Company.objects.create(company_name='Apple',
                               industry_from=tech)

    def test_existence(self):
        # check if null
        aa = Company.objects.get(company_name='American Airlines')
        ba = Company.objects.get(company_name='British Airways')
        amzn = Company.objects.get(company_name='Amazon')
        aapl = Company.objects.get(company_name='Apple')

        # check if no info is corrupted
        self.assertEqual(aa.company_name, 'American Airlines')
        self.assertEqual(ba.company_name, 'British Airways')
        self.assertEqual(amzn.company_name, 'Amazon')
        self.assertEqual(aapl.company_name, 'Apple')

        # check links up to industry level
        self.assertEqual(aa.industry_from.industry_field, 'Aviation')
        self.assertEqual(ba.industry_from.industry_field, 'Aviation')
        self.assertEqual(amzn.industry_from.industry_field, 'Technology')
        self.assertEqual(aapl.industry_from.industry_field, 'Technology')
        
        # check downward links from industry level
        aviation_companies = Company.objects.filter(industry_from__industry_field='Aviation')
        self.assertEqual(len(aviation_companies), 2)
        tech_companies = Company.objects.filter(industry_from__industry_field='Technology')
        self.assertEqual(len(tech_companies), 2)
    
    def test_update(self):
        amzn = Company.objects.get(company_name='Amazon')
        amzn.company_name = 'Facebook'
        amzn.save()
        try:
            bad_obj = Company.objects.get(company_name='Amazon')
        except ObjectDoesNotExist:
            bad_obj = None
        self.assertIsNone(bad_obj)
        # The below line shouldn't throw an ObjectDoesNotExist
        fb = Company.objects.get(company_name='Facebook')
    
    def test_delete(self):
        amzn = Company.objects.get(company_name='Amazon')
        amzn.delete()
        try:
            bad_obj = Company.objects.get(company_name='Amazon')
        except ObjectDoesNotExist:
            bad_obj = None
        self.assertIsNone(bad_obj)
        companies = Company.objects.filter()
        self.assertEqual(len(companies), 3)

class UserTestCase(TestCase):
    def setUp(self):
        usr = User.objects.create(username='vedant', password='asdfsdfasdf',
                                  email='test@ing.com')

    def test_existence(self):
        usr = User.objects.get(email='test@ing.com')
        self.assertEqual(usr.username, 'vedant')

class PostTestCase(TestCase):
    def setUp(self):
        CompanyTestCase().setUp()
        amzn = Company.objects.get(company_name='Amazon')
        UserTestCase().setUp()
        usr = User.objects.get(email='test@ing.com')
        Post.objects.create(body='This is a sample post',
                            timestamp=datetime.now(),
                            company_about=amzn, posted_by=usr)
    
    def test_existence(self):
        post = Post.objects.filter()[0]
        self.assertEqual(post.body, 'This is a sample post')

    def test_update(self):
        post = Post.objects.filter()[0]
        post.body = 'changed body.'
        post.save()
        self.assertNotEqual(post.body, 'This is a sample post')
        self.assertEqual(Post.objects.filter()[0].body, 'changed body.')

    def test_delete(self):
        post = Post.objects.filter()[0]
        post.delete()
        self.assertEqual(len(Post.objects.filter()), 0)

class CommentTestCase(TestCase):
    def setUp(self):
        PostTestCase().setUp()
        post = Post.objects.filter()[0]
        comment = Comment.objects.create(body='This is a sample comment',
                                         timestamp=datetime.now(),
                                         is_positive=True,
                                         commented_on=post,
                                         commented_by=User.objects.filter()[0])

    def test_existence(self):
        comment = Comment.objects.filter()[0]
        self.assertEqual(comment.body, 'This is a sample comment')
    
    def test_update(self):
        comment = Comment.objects.filter()[0]
        comment.body = 'Updated body'
        comment.save()
        self.assertEqual(Comment.objects.filter()[0].body, 'Updated body')

    def test_delete(self):
        comment = Comment.objects.filter()[0]
        comment.delete()
        self.assertEqual(len(Comment.objects.filter()), 0)


