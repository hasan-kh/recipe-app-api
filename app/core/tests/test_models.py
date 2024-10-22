"""
Test for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_user_default(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email(self):
        """Test creating an user with email is successful."""
        User = get_user_model()
        email = 'test@email.com'
        password = 'testpass123'
        user = User.objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_normalize_user_creation(self):
        """Test email  is normalize for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123'
            )

            self.assertEqual(user.email, expected)

    def test_empty_email_user_creation_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='pass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def create_recipe_just_required_fields(self):
        """Test creating a recipe with required fields."""
        user = create_user(email='test@example.com',
                           password='testpass123')

        payload = {
            'user': user,
            'title': 'recipe title',
            'time_minuts': 110,
            'price': Decimal(25.00)
        }
        recipe = models.Recipe.objects.create(**payload)
        for k, v in payload:
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.description, '')
        self.assertEqual(recipe.link, '')

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = create_user(email='test@example.com',
                           password='testpass123')

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user_default()
        payload = {
            'user': user,
            'name': 'Tag1'
        }
        models.Tag.objects.create(**payload)
        tag_from_db = models.Tag.objects.get(name=payload['name'])

        self.assertEqual(tag_from_db.name, payload['name'])
        self.assertEqual(tag_from_db.user, payload['user'])
        self.assertEqual(str(tag_from_db), tag_from_db.name)

    def test_creaete_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user_default()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredent1',
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_image_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
