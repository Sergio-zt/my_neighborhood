from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from neighborhood.models import District
from posts.models import Post


class DistrictSearchTests(TestCase):
    def setUp(self):
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
        self.url = reverse("neighborhood:district-list")

        self.matching_district = District.objects.create(
            name="Search_Name"
        )
        self.other_district = District.objects.create(
            name="Other_name"
        )
        self.client.force_login(self.user)

    def test_search_by_name_returns_correct_district(self):
        response = self.client.get(self.url, {"name": "Search"})
        self.assertEqual(response.status_code, 200)
        district_list = response.context["district_list"]

        self.assertIn(self.matching_district, district_list)
        self.assertNotIn(self.other_district, district_list)

    def test_search_with_no_results(self):
        response = self.client.get(self.url, {"name": "non_existent_name"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["district_list"]), 0)


class PostSearchTests(TestCase):
    def setUp(self):
        self.title = "test_title"
        self.text = "Test post text"
        self.url = reverse("posts:post-list")
        self.district = District.objects.create(
            name="Test_Name",
        )
        self.user = get_user_model().objects.create(
            username="gonzales",
            password="test_password",
            first_name="first_name",
            last_name="last_name",
        )
        self.post = Post.objects.create(
            title=self.title,
            text=self.text,
            user=self.user,
        )
        self.post.districts.add(self.district)

        self.client.force_login(self.user)

    def test_search_by_post_returns_correct_post(self):
        response = self.client.get(self.url, {"text": self.text})
        self.assertEqual(response.status_code, 200)
        post_list = response.context["post_list"]

        self.assertIn(self.post, post_list)

    def test_search_with_no_results(self):
        response = self.client.get(self.url, {"text": "non_existent_title"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["post_list"]), 0)
