from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product, Tag


class TagTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Outdoor", slug="outdoor")
        self.product = Product.objects.create(name="Bottle", category=category, price=Decimal("8.99"))
        self.url = reverse("product_detail", args=[category.slug, self.product.pk])

    def test_create_and_reuse_multiple_tags_on_products(self):
        limited = Tag.objects.create(name="Limited")
        limited.full_clean()
        sale = Tag.objects.create(name="Sale")
        other = Product.objects.create(name="Hat", category=self.product.category, price=Decimal("4.99"))

        self.product.tags.add(limited, sale)
        other.tags.add(limited)

        self.assertEqual(str(limited), "Limited")
        self.assertIsNotNone(limited.created_at)
        self.assertIsNotNone(limited.updated_at)
        self.assertCountEqual(self.product.tags.all(), [limited, sale])
        self.assertQuerySetEqual(other.tags.all(), [limited])

    def test_duplicate_tag_name_is_rejected(self):
        Tag.objects.create(name="Limited")
        duplicate = Tag(name="Limited")

        with self.assertRaises(ValidationError) as error:
            duplicate.full_clean()

        self.assertIn("name", error.exception.message_dict)

    def test_empty_tag_name_is_rejected(self):
        with self.assertRaises(ValidationError) as error:
            Tag(name="").full_clean()

        self.assertIn("name", error.exception.message_dict)

    def test_product_detail_displays_assigned_tags(self):
        self.product.tags.add(Tag.objects.create(name="Limited"), Tag.objects.create(name="Sale"))

        response = self.client.get(self.url)

        self.assertContains(response, '<span class="product-tag">Limited</span>', html=True)
        self.assertContains(response, '<span class="product-tag">Sale</span>', html=True)
        self.assertNotContains(response, "no tags available")

    def test_product_without_tags_displays_italic_placeholder(self):
        response = self.client.get(self.url)

        self.assertContains(response, '<span class="text-muted fst-italic">no tags available</span>', html=True)
