import pytest
from pytest_django.asserts import (
    assertContains,
    assertRedirects
)

from django.urls import reverse
from django.contrib.sessions.middleware import \
    SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView,
    CheeseUpdateView
)
from .factories import CheeseFactory, cheese

pytestmark = pytest.mark.django_db


def test_good_cheese_list_view_expanded(rf):
    url = reverse('cheeses:list')
    request = rf.get(url)
    callable_obj = CheeseListView.as_view()
    response = callable_obj(request)
    assertContains(response, 'Cheese List')


def test_cheese_list_contains_2_cheeses(rf):
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_good_cheese_detail_view(rf, cheese):
    url = reverse('cheeses:detail',
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)


def test_detail_contains_cheese_data(rf, cheese):
    request = rf.get(reverse('cheeses:detail',
                             kwargs={'slug': cheese.slug}))
    response = CheeseDetailView.as_view()(request, slug=cheese.slug)
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_good_cheese_create_view(rf, admin_user):
    # cheese = CheeseFactory()
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assert response.status_code == 200


def test_cheese_create_form_valid(rf, admin_user):
    data = {
        'name': 'Testy',
        'description': 'testy description',
        'firmness': Cheese.Firmness.HARD
    }
    request = rf.post(reverse('cheeses:add'), data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    # get created cheese.
    cheese = Cheese.objects.get(name='Testy')

    assert cheese.name == data.get('name')
    assert cheese.description == data.get('description')
    assert cheese.creator == admin_user


def test_cheese_create_correct_title(rf, admin_user):
    request = rf.post(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assertContains(response, 'Add Cheese')


def test_good_cheese_update(rf, admin_user, cheese):
    url = reverse('cheeses:update', kwargs={'slug': cheese.slug})
    request = rf.get(url)
    request.user = admin_user
    response = CheeseUpdateView.as_view()(request, slug=cheese.slug)
    assertContains(response, 'Update Cheese')


def test_cheese_update(rf, admin_user, cheese):
    data = {
        'name': 'New testy',
        'description': 'new testy description',
        'firmness': Cheese.Firmness.SEMI_HARD
    }
    request = rf.post(reverse('cheeses:update',
                              kwargs={'slug': cheese.slug}),
                      data)
    request.user = admin_user
    response = CheeseUpdateView.as_view()(request, slug=cheese.slug)
    cheese.refresh_from_db()
    assert cheese.name == 'New testy'
