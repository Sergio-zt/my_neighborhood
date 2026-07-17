from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from neighborhood.models import Post, District


DISTRICT_URL = reverse("neighborhood:district-list")
POSTS_URL = reverse("neighborhood:post-list")


class PublicDistrictTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISTRICT_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicPostTest(TestCase):
    def test_login_required(self):
        res = self.client.get(POSTS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_detail_required(self):
        res = self.client.get(reverse("neighborhood:post-detail", args=(1,)))
        self.assertNotEqual(res.status_code, 200)


class PrivateUserTest(TestCase):
    def setUp(self) -> None:
        username = "test_user_name"
        password = "testpassword"
        first_name = "First Name"
        last_name = "Last Name"
        self.user = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        self.client.force_login(self.user)

    def test_retrive_districts(self):
        response = self.client.get(DISTRICT_URL)
        self.assertEqual(response.status_code, 200)
        district = District.objects.all()
        self.assertEqual(
            list(response.context["district_list"]),
            list(district)
        )

    def test_retrive_user_detail(self):
        response = self.client.get(
            reverse("neighborhood:user-detail", args=(self.user.pk,))
        )
        user = get_user_model().objects.get(pk=self.user.pk,)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["user"],
            user
        )


class PrivatePostTest(TestCase):
    def setUp(self) -> None:
        username = "test_user_name"
        password = "testpassword"
        first_name = "First Name"
        last_name = "Last Name"
        self.user = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        self.district = District.objects.create(
            name="Test_Name",
        )
        self.post = Post.objects.create(
            user=self.user,
            title="Post_Title",
            text="Post Text",
        )
        self.post.districts.add(self.district)

        self.client.force_login(self.user)

    def test_retrive_posts(self):
        response = self.client.get(POSTS_URL)
        self.assertEqual(response.status_code, 200)
        posts = Post.objects.all()
        self.assertEqual(
            list(response.context["post_list"]),
            list(posts)
        )

    def test_retrive_post_detail(self):
        response = self.client.get(
            reverse("neighborhood:post-detail", args=(self.post.pk,))
        )
        post = Post.objects.get(id=self.post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["post"],
            post
        )
