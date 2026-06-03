from django.urls import reverse

from rest_framework import status

from apps.products.models import Product, ProductCategory

from .test_setup import TestSetUp


class TestProductViews(TestSetUp):

    def test_get_product_list(self):

        response = self.client.get(
            self.products_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_single_product(self):

        response = self.client.get(
            reverse(
                "products-detail",
                kwargs={"pk": self.product.pk}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_product_not_found(self):

        response = self.client.get(
            reverse(
                "products-detail",
                kwargs={"pk": 99999}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_search_product(self):

        Product.objects.create(
            name="Pizza",
            price=20,
            category=self.category
        )

        response = self.client.get(
            self.products_url,
            {"search": "Pizza"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_filter_product_by_category(self):

        ProductCategory.objects.create(
            name="Drinks"
        )

        response = self.client.get(
            self.products_url,
            {"category": "Fast Food"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )


    def test_client_cannot_create_product(self):

        self.authenticate_client()

        payload = {
            "name": "Pizza",
            "price": 25,
            "category_id": self.category.id
        }

        response = self.client.post(
            self.products_url,
            payload
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_delete_product(self):

        self.authenticate_admin()

        response = self.client.delete(
            reverse(
                "products-detail",
                kwargs={"pk": self.product.pk}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_client_cannot_delete_product(self):

        self.authenticate_client()

        response = self.client.delete(
            reverse(
                "products-detail",
                kwargs={"pk": self.product.pk}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    

    def test_client_cannot_update_product(self):

        self.authenticate_client()

        payload = {
            "name": "Updated Burger",
            "price": 20,
            "category_id": self.category.id
        }

        response = self.client.put(
            reverse(
                "products-detail",
                kwargs={"pk": self.product.pk}
            ),
            payload
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )