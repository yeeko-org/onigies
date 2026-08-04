"""
Tests de la app ies.

Contrato del payload de sesión: qué campos de la institución le llegan al
frontend al iniciar sesión o rehidratarla.
"""
from django.test import TestCase

from api.views.auth.serializers import UserDataSerializer
from ies.models import Institution, User


class LoginPayloadInstitutionTests(TestCase):
    """
    `is_test` viaja en el payload de `/login/` por las dos rutas en que la
    institución se serializa (`institution` e `institution_details`).

    Hoy llega gratis porque ambos serializers usan `fields='__all__'`; este
    test es la red por si alguien los cambia a una lista explícita. El
    frontend decide con esta bandera qué secciones muestra, así que
    perderla dejaría a las instituciones de prueba viendo solo lo
    publicado, sin ningún error visible.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.inst_test = Institution.objects.create(
            name='IES de prueba', acronym='TEST', is_test=True)
        cls.user_test = User.objects.create_user(
            'test', password='x', institution=cls.inst_test)
        cls.inst_real = Institution.objects.create(
            name='IES Real', acronym='REAL')
        cls.user_real = User.objects.create_user(
            'real', password='x', institution=cls.inst_real)

    def test_is_test_en_institution(self) -> None:
        data = UserDataSerializer(self.user_test).data
        self.assertIn('is_test', data['institution'])
        self.assertTrue(data['institution']['is_test'])

    def test_is_test_en_institution_details(self) -> None:
        data = UserDataSerializer(self.user_test).data
        self.assertIn('is_test', data['institution_details'])
        self.assertTrue(data['institution_details']['is_test'])

    def test_institucion_real_reporta_false(self) -> None:
        data = UserDataSerializer(self.user_real).data
        self.assertFalse(data['institution']['is_test'])
        self.assertFalse(data['institution_details']['is_test'])
