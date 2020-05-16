import pytest
from ..models import Cheese

# Connect tests with database.
pytestmark = pytest.mark.django_db


def test___str__():
    cheese = Cheese.objects.create(
        name="testycheese",
        description="test description",
        firmness=Cheese.Firmness.SOFT,
    )
    assert cheese.__str__() == "testycheese"
    assert str(cheese) == "testycheese"

