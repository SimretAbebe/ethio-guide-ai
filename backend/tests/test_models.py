import pytest
from pydantic import ValidationError
from app.models.site import CulturalSite


class TestCulturalSiteModel:
    """Test CulturalSite Pydantic model"""

    def test_valid_cultural_site(self):
        """Test creating a valid cultural site"""
        site = CulturalSite(
            name="Test Site",
            description="A test description",
            location="Test Location",
            region="Test Region",
            category="Historical"
        )
        assert site.name == "Test Site"
        assert site.description == "A test description"
        assert site.location == "Test Location"
        assert site.region == "Test Region"
        assert site.category == "Historical"

    def test_cultural_site_with_optional_fields(self):
        """Test creating a site with optional fields"""
        site = CulturalSite(
            name="Test Site",
            description="A test description",
            location="Test Location",
            region="Test Region",
            category="Historical",
            historical_significance="Very significant",
            visiting_hours="9 AM - 5 PM",
            entry_fee=50,
            coordinates={"latitude": 9.0, "longitude": 38.0}
        )
        assert site.historical_significance == "Very significant"
        assert site.visiting_hours == "9 AM - 5 PM"
        assert site.entry_fee == 50
        assert site.coordinates == {"latitude": 9.0, "longitude": 38.0}

    def test_cultural_site_missing_required_fields(self):
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            CulturalSite(
                name="Test Site",
                description="A test description"
                # Missing: location, region, category
            )

    def test_cultural_site_invalid_type(self):
        """Test that invalid field types raise validation error"""
        with pytest.raises(ValidationError):
            CulturalSite(
                name="Test Site",
                description="A test description",
                location="Test Location",
                region="Test Region",
                category="Historical",
                entry_fee="not a number"  # Should be int or float
            )
