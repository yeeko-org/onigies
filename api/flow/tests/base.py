"""Fixture base compartida por los tests de seguridad del flujo."""
from django.urls import reverse
from rest_framework.test import APITestCase

from flow.seed import seed_flow
from ies.initial_data import InitStatus
from ies.models import Institution, Period, User


class FlowSecurityTestCase(APITestCase):
    """Base: siembra el catálogo y crea dos IES con sus paquetes."""

    @classmethod
    def setUpTestData(cls):
        # Institution.save fija status_sending/status_register del flujo
        # viejo (StatusControl), que coexiste con flow.Status.
        InitStatus()
        seed_flow()
        cls.period = Period.objects.create(year=2025)

        cls.inst_a = Institution.objects.create(name='IES A', acronym='IESA')
        cls.inst_b = Institution.objects.create(name='IES B', acronym='IESB')

        cls.survey_a = cls.inst_a.surveys.get(period=cls.period)
        cls.survey_b = cls.inst_b.surveys.get(period=cls.period)
        cls.package_a = cls.survey_a.packages.first()
        cls.package_b = cls.survey_b.packages.first()

        cls.ies_a = User.objects.create_user(
            'iesa', password='x', institution=cls.inst_a)
        cls.ies_b = User.objects.create_user(
            'iesb', password='x', institution=cls.inst_b)
        cls.reviewer = User.objects.create_user(
            'rev', password='x', reviewer=True)

    def _transitions_url(self, obj):
        return reverse(
            'flow-transitions',
            args=['example', 'goodpracticepackage', obj.pk])

    def _events_url(self, obj):
        return reverse(
            'flow-events', args=['example', 'goodpracticepackage', obj.pk])
