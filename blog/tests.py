from django.test import TestCase
from blog.models import Post

class SimpleTest(TestCase):
    def setUp(self):
        Post(contenido='This is a test greeting').save()

    def test_setup(self):
        self.assertEqual(1, len(Post.objects.all()))
        self.assertEqual('This is a test greeting', Post.objects.all()[0].content)
