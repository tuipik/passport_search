from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api_service.serializers import (
    ReportTypeSerializer,
    SearchPhraseSerializer,
    LostPassportSerializer,
)
from core.models import LostPassport


class SearchDocumentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        report_type = request.data["report_type"]
        document_series = request.data["search_phrase"]["document_series"]
        document_number = request.data["search_phrase"]["document_number"]

        report_type = ReportTypeSerializer(data={"report_type": report_type})

        search_phrase = SearchPhraseSerializer(
            data={
                "document_series": document_series,
                "document_number": document_number,
            }
        )
        if (
            report_type.is_valid()
            and search_phrase.is_valid()
            and report_type.is_valid()
            and document_number
            and report_type.data["report_type"] == "full"
        ):
            res_data = LostPassport.objects.filter(
                Q(document_series__icontains=document_series)
            ).filter(Q(document_number__iexact=document_number))

        elif (
            report_type.is_valid()
            and search_phrase.is_valid()
            and report_type.is_valid()
            and not document_number
            and report_type.data["report_type"] == "full"
        ):
            res_data = LostPassport.objects.filter(
                Q(document_series__icontains=document_series)
            )

        elif (
            report_type.is_valid()
            and search_phrase.is_valid()
            and report_type.is_valid()
            and document_number
            and report_type.data["report_type"] == "compact"
        ):
            is_exists = (
                LostPassport.objects.filter(
                    Q(document_series__icontains=document_series)
                )
                .filter(Q(document_number__iexact=document_number))
                .exists()
            )
            return Response({"result": 1 if is_exists else 0})

        data = [LostPassportSerializer(model).data for model in res_data]

        return Response(data)
