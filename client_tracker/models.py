from django.db import models
from datetime import date
from rest_framework import serializers


class Client(models.Model):
    place_id = models.CharField(max_length=500, unique=True)
    business_name = models.CharField(max_length=500)
    total_reviews = models.IntegerField(null=True, blank=True)
    previous_total_reviews = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    previous_rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    review_delta = models.IntegerField(null=True, blank=True)
    rating_delta = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    last_update = models.DateField(null=True, blank=True)

    competitor_1 = models.ForeignKey(
        "self",
        related_name="competitor_1a",
        on_delete=models.SET_NULL,
        to_field="place_id",
        null=True,
        blank=True,
    )
    competitor_2 = models.ForeignKey(
        "self",
        related_name="competitor_2a",
        on_delete=models.SET_NULL,
        to_field="place_id",
        null=True,
        blank=True,
    )
    competitor_3 = models.ForeignKey(
        "self",
        related_name="competitor_3a",
        on_delete=models.SET_NULL,
        to_field="place_id",
        null=True,
        blank=True,
    )
    competitor_4 = models.ForeignKey(
        "self",
        related_name="competitor_4a",
        on_delete=models.SET_NULL,
        to_field="place_id",
        null=True,
        blank=True,
    )
    competitor_5 = models.ForeignKey(
        "self",
        related_name="competitor_5a",
        on_delete=models.SET_NULL,
        to_field="place_id",
        null=True,
        blank=True,
    )

    def _get_days_since_last_review(self):
        today = date.today()
        if self.last_update is None:
            self.last_update = today
        return str((today - self.last_update).days)

    days_since_last_review = property(_get_days_since_last_review)
    is_client = models.BooleanField(default=False)
    reviews_this_week = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.business_name


class ClientSerializer(serializers.Serializer):
    place_id = serializers.CharField(max_length=500)
    business_name = serializers.CharField(max_length=500)
    total_reviews = serializers.IntegerField()
    previous_total_reviews = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    previous_rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    review_delta = serializers.IntegerField()
    rating_delta = serializers.DecimalField(max_digits=4, decimal_places=2)
    last_update = serializers.DateField()
    days_since_last_review = serializers.CharField(max_length=500)
    competitor_1 = serializers.CharField()
    competitor_2 = serializers.CharField()
    competitor_3 = serializers.CharField()
    competitor_4 = serializers.CharField()
    competitor_5 = serializers.CharField()
    is_client = serializers.BooleanField()
    reviews_this_week = serializers.IntegerField()

    class Meta:
        model = Client
        fields = [
            "place_id",
            "business_name",
            "total_reviews",
            "previous_total_reviews",
            "rating",
            "previous_rating",
            "review_delta",
            "rating_delta",
            "last_update",
            "days_since_last_review",
            "competitor_1",
            "competitor_2",
            "competitor_3",
            "competitor_4",
            "competitor_5",
            "is_client",
            "reviews_this_week",
        ]


class ClientSerializerWithCompetitors(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "place_id",
            "business_name",
            "total_reviews",
            "previous_total_reviews",
            "rating",
            "previous_rating",
            "review_delta",
            "rating_delta",
            "last_update",
            "days_since_last_review",
            "competitor_1",
            "competitor_2",
            "competitor_3",
            "competitor_4",
            "competitor_5",
            "is_client",
            "reviews_this_week",
        )
        depth = 1
