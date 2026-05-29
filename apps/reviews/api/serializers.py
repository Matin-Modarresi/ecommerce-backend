from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "user_name",
            "product",
            "rating",
            "comment",
            "created_at",
        )
        read_only_fields = ("id", "user_name", "created_at")


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("product", "rating", "comment")

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")

        # ولیدیشن محدوده امتیاز
        if not (1 <= attrs['rating'] <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")

        return attrs
