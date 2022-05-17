from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from users.utils import create_and_login_test_user

class SpaceCreateViewTests(TestCase):
    def setUp(self):
        create_and_login_test_user(self)

    def test_form(self):
        """
        Space creation form should contain necessary inputs.
        """
        response = self.client.get(reverse('spaces:create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post" enctype="multipart/form-data">')
        self.assertContains(response, '<label class="form-label" for="id_name">')
        self.assertContains(response, '<input type="text" name="name" maxlength="200" class="form-control" placeholder="Name" required id="id_name">')
        self.assertContains(response, '<label class="form-label" for="id_tags">')
        self.assertContains(response, '<input type="text" name="tags" maxlength="500" class="form-control" placeholder="Tags" id="id_tags">')
        self.assertContains(response, '<label class="form-label" for="id_cover_image">')
        self.assertContains(response, '<input type="file" name="cover_image" class="form-control" required id="id_cover_image">')
        self.assertContains(response, '<button class="btn btn-primary" type="submit">Create</button>')

    def test_form_submission(self):
        """
        Space creation form should create space.
        """
        name = "Test Space"
        tags = "test"
        cover_image = SimpleUploadedFile("cover-image.jpg", b"cover_image", content_type="image/jpeg")
        response = self.client.post(reverse('spaces:create'), data={'name':name, 'tags':tags, 'cover_image':cover_image}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your space has been created successfully.')

    def test_form_submission_with_invalid_form(self):
        """
        Space creation form should return to form if it is not valid.
        """
        email = "example1@example.com"
        username = "example1"
        password1 = "test"
        password2 = "test"
        interests = "example interests"
        response = self.client.post(reverse('spaces:create'), data={'email':email, 'username':username, 'password1': password1, 'password2': password2, 'interests': interests})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post" enctype="multipart/form-data">')
