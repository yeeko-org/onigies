# onigies api

Django REST Framework API. Validation and business shape live in serializers.

## Commands

Virtualenv interpreter: `venv/bin/python` (in `api/`).

```bash
python manage.py runserver   # dev server on :8018
pytest                       # run tests
pytest ies/tests.py          # single file
```

## Environment

```env
POSTGRESQL_DB=True
DATABASE_NAME=onigies-local
FRONTEND_SITE_URL=https://localhost:3018
```

## Apps

| App | Responsibility |
|-----|---------------|
| `ies` | User (custom AbstractUser), Institution, Period, StatusControl, InvitationToken, PasswordRecoveryToken |
| `indicator` | Axis → Component → Observable hierarchy; Sector, GeneralGroup |
| `question` | Question definitions by type (A, B, Reach, Plan, Special) with weights |
| `survey` | Survey per Institution-Period; AxisValue, ComponentValue, PopulationQuantity |
| `answer` | ObservableResponse, GroupResponse, attachments, comments |
| `example` | Good practices: GoodPracticePackage → GoodPractice → Feature → FeatureGoodPractice, Evidence |
| `ps_schema` | Schema/collection metadata for dynamic catalog and filter configuration |
| `email_send` | EmailProfile, TemplateBase, EmailRecord. Services: `send_template_email`, `send_simple_email` |
| `flow` | Validation-flow engine: Status catalog (groups `bp`/`cp`/`gen`), FlowEvent timeline, generic Attachment. Hierarchy registry in `flow/registry.py`. `ComponentValue` does NOT participate in the flow. Replaces `ies.StatusControl` (coexisting until data verification; see `docs/records/2026-06-05-diseno-del-motor-de-flujo.md`) |

Settings in `core/settings/__init__.py`; root URLs in `core/urls.py`; API routes in `api/urls.py`.

## Creating views

DRF conventions (APIView vs ViewSet, serializer-validated requests, error
format, docstrings) live in the global backend rules and apply here.
Project-specific:

- **Base classes:** `BaseViewSet` / `BaseGenericViewSet` from
  `api/views/common_views.py` for model CRUD; `views.APIView` for custom
  auth endpoints (login, recovery).
- **Serializer location:** `api/views/{sub-package}/serializers.py`
  (e.g. auth → `api/views/auth/serializers.py`).

## Reference

- ViewSet mixins catalog (`MultiSerializer*`, `ListMix`, `CreateMix`, etc.): `api/mixins.py`
- `BaseViewSet` extends `ModelViewSet` with `CustomPagination`, `UnaccentSearchFilter` (Postgres `unaccent__icontains`, degrades gracefully on SQLite), `DjangoFilterBackend`, `OrderingFilter`, delete-confirmation mixin: `api/views/common_views.py`
- `AdvancedConditionalFieldsViewMixin` — excludes serializer fields by `field_permissions` dict keyed by role (`anonymous`, `authenticated`, `staff`): same file