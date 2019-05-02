from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import ProteinViewSet, PeptideViewSet, SpanGroupViewSet, RegionViewSet
from .views import SpanGroup_RegionsViewSet, Peptide_SpanGroupsViewSet

router = DefaultRouter()

# Register some endpoints via "router.register(...)"
# router.register(...)
router.register("protein", ProteinViewSet, base_name="protein")
router.register("peptide", PeptideViewSet, base_name="peptide")
router.register("spangroup", SpanGroupViewSet, basename="spangroup")
router.register("region", RegionViewSet, basename="region")
router.register("spangroup_regions", SpanGroup_RegionsViewSet, basename="spangroup_regions")
router.register("peptide_spangroups", Peptide_SpanGroupsViewSet, basename="peptide_spangroups")

schema_view = get_schema_view(title="Peptide2Genome API")

urlpatterns = [
    path("/api/", include(router.urls)),
    # path("", render_aggregation, name="aggregation"),
]
