from django.core.management.base import BaseCommand
import asyncio
import aiohttp
import requests
from django.conf import settings
from dateutil import parser

from core.models import LostPassport, DocumentType


class Command(BaseCommand):
    help = "Update_DB"

    resource_urls_list = []
    DOCUMENT_DESCRIPTORS_LIST = LostPassport.objects.all()\
        .values_list('descriptor', flat=True)

    def make_packages_list(self):
        res = requests.get(settings.PASSPORT_PACKAGES_URL)
        pasport_packages = res.json()
        return [
            item["id"]
            for item in pasport_packages["result"]["resources"]
            if item["id"] != "25ce9105-f906-4972-ba29-2d8037d1854d"
        ]

    async def make_passport_url(self, package):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f"{settings.BASE_RESOURCE_URL}{package}"
                ) as response:
                    resource_file = await response.json()
                    self.resource_urls_list.append(
                        resource_file["result"]["url"]
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully got url "
                            f"{resource_file['result']['url']}."
                        )
                    )

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Unable to get url from package {package} "
                    f"due to {e.__class__}."
                )
            )

    async def make_passport_urls_list(self, packages):
        await asyncio.gather(*[
            self.make_passport_url(package) for package in packages
        ])

    def document_type(self, series):
        if series != "":
            return DocumentType.objects.get(id=1)
        return DocumentType.objects.get(id=2)

    def document_already_exists(self, document_descriptor):
        if document_descriptor["ID"] in self.DOCUMENT_DESCRIPTORS_LIST:
            return False
        return True

    def create_documents_types(self):
        already_exists = DocumentType.objects.filter(pk=1).exists()
        document_type_data = [
            {"id": 1,
             "title": "Паспорт громадянина України - є серія",
             "has_series": True},
            {"id": 2,
             "title": "Паспорт громадянина України - немає серії",
             "has_series": False}
        ]
        if not already_exists:
            DocumentType.objects.bulk_create(
                [DocumentType(**q) for q in document_type_data]
            )

    def fill_up_db(self, creation_data):
        LostPassport.objects.bulk_create(
            [LostPassport(**q) for q in creation_data],
            batch_size=100
        )

    def make_data_4_create(self, url):
        try:
            response = requests.get(url)
            documents = response.json()
            counter = 0
            bulk_creation_data = []

            for document in documents:

                if self.document_already_exists(document):
                    bulk_creation_data.append(
                        {
                            "descriptor": document["ID"],
                            "document_series": document["D_SERIES"],
                            "document_number": document["D_NUMBER"],
                            "document_type": self.document_type(
                                document["D_SERIES"]
                            ),
                            "status": document["D_STATUS"],
                            "theft_date": parser.parse(document["THEFT_DATA"]),
                            "insert_date": parser.parse(document["INSERT_DATE"]),
                            "ovd": document["OVD"],
                        }
                    )
                    counter += 1

            self.stdout.write(
                self.style.SUCCESS(f"Successfully added {counter} new documents"
                                   f" from total {len(documents)} documents "
                                   f"to list from url {url}.")
            )

            self.fill_up_db(bulk_creation_data)

            self.stdout.write(
                self.style.SUCCESS(f"Successfully added {counter} new documents"
                                   f" to database")
            )

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Unable to add data from url {url} due to {e.__class__}."
                )
            )

    def handle(self, *args, **options):
        self.create_documents_types()

        packages_list = self.make_packages_list()
        asyncio.run(self.make_passport_urls_list(packages_list))

        for url in self.resource_urls_list:
            self.make_data_4_create(url)
