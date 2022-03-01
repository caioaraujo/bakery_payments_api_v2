import coreapi
import coreschema
from rest_framework.filters import BaseFilterBackend


class PaymentFilterBackend(BaseFilterBackend):
    """Filter fields for search engine"""

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="is_paid",
                required=False,
                schema=coreschema.Boolean(description="If true, returns only payments already paid"),
                location="query",
            )
        ]
