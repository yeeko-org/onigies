# onigies api

Django REST Framework API. Validation and business shape live in serializers.

## Commands

Virtualenv interpreter: `venv/bin/python` (in `api/`).

```bash
python manage.py runserver   # dev server on :8018
pytest                       # run tests
pytest ies/tests.py          # single file
```

Test layout, what each test class covers and the shared fixtures: `TESTING.md`.

## Environment

```env
POSTGRESQL_DB=True
DATABASE_NAME=onigies-local
FRONTEND_SITE_URL=https://localhost:3018
```

## Apps

| App | Responsibility |
|-----|---------------|
| `ies` | User (custom AbstractUser), Institution, Period (`cp_open_at` opens cp answers), InvitationToken, PasswordRecoveryToken |
| `indicator` | Axis → Component → Observable hierarchy; Sector, GeneralGroup |
| `question` | Question definitions by type; `QuestionType` catalog and the observable↔type bridge with weights |
| `survey` | Survey per Institution-Period; AxisValue, ComponentValue, PopulationQuantity |
| `answer` | cp capture: ObservableResponse → GroupResponse (eager, one per bridge row) → typed responses (lazy). Domain rules in `answer/services.py` (init «No» → `cp_not_present` tree, reviewer waits for the axis), completion rules in `answer/group_validation.py`, response gate in `survey/cp_gate.py` |
| `example` | Good practices: GoodPracticePackage → GoodPractice → Feature → FeatureGoodPractice |
| `ps_schema` | Schema/collection metadata for dynamic catalog and filter configuration |
| `email_send` | EmailProfile, TemplateBase, EmailRecord. Services: `send_template_email`, `send_simple_email` |
| `flow` | Validation-flow engine: Status catalog (groups `bp`/`cp`/`gen`), FlowEvent timeline, generic Attachment. Hierarchy registry in `flow/registry.py`. `ComponentValue` does NOT participate in the flow. The only status system |

Settings in `core/settings/__init__.py`; root URLs in `core/urls.py`; API routes in `api/urls.py`.

**`Institution.is_test`:** test institutions see every section and ignore
period deadlines, but the cp response gate (`survey/cp_gate.py`) applies
to them too. Any calculation, indicator or export must exclude them
(`institution__is_test=False`). None exists yet — do not introduce one.

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