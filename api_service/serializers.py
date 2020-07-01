from rest_framework import serializers

from core.models import DocumentType, LostPassport


class ReportTypeSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(
        choices=[("full", "full"), ("compact", "compact")]
    )


class SearchPhraseSerializer(serializers.Serializer):
    document_series = serializers.CharField(allow_blank=True, max_length=5)
    document_number = serializers.IntegerField(allow_null=True)


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ["id", "title", "has_expiration_date", "has_series"]
        read_only_fields = ("id",)


class LostPassportSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)

    class Meta:
        model = LostPassport
        fields = [
            "id",
            "descriptor",
            "document_series",
            "document_number",
            "document_type",
            "status",
            "theft_date",
            "insert_date",
            "ovd",
        ]
        read_only_fields = ("id",)
