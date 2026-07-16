from django.test import TestCase
from django.contrib.auth import get_user_model

from neighborhood.models import Post, District


class ModelsTests(TestCase):
    def test_district_str(self):
        district = District.objects.create(
            name="Test_Name"
        )
        self.assertEqual(
            str(district),
            f"{district.name}"
        )

    def test_user_str(self):
        user = get_user_model().objects.create(
            username="test_user",
            password="test_password",
            first_name="first_name",
            last_name="last_name"
        )
        self.assertEqual(
            str(user),
            f"{user.username} ({user.first_name} {user.last_name})"
        )

    def test_post_created(self):
        district = District.objects.create(
            name="Test_Name"
        )
        user = get_user_model().objects.create(
            username="test_user",
            password="test_password",
            first_name="first_name",
            last_name="last_name"
        )
        post = Post.objects.create(
            user=user,
            title="Post_Title",
            text="Post Text",
        )

        post.districts.add(district)

        self.assertEqual(Post.objects.count(), 1)


        saved_post = Post.objects.get(id=post.id)
        self.assertEqual(saved_post.title, "Post_Title")
        self.assertEqual(saved_post.text, "Post Text")
        self.assertEqual(saved_post.user, user)
        self.assertEqual(saved_post.districts.count(), 1)
        self.assertIn(district, saved_post.districts.all())
