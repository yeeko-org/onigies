"""Sonda de diagnóstico de Buenas Prácticas anómalas (correr en PRODUCCIÓN).

Uso en el servidor:
    python manage.py shell < .claude/diagnose_bp.py

Busca prácticas con status que el catálogo no resuelve (NULL o nombre no
sembrado), que es lo que hace que la card no muestre chip "borrador" y que
el registro ocupe cupo del límite de 5 sin poder usarse.
"""
from example.models import GoodPractice, GoodPracticePackage
from flow.models import Status

valid = set(Status.objects.values_list("name", flat=True))
print("Status sembrados:", sorted(valid))

# 1) Prácticas con status nulo o no resoluble en el catálogo.
anomalous = [
    g for g in GoodPractice.objects.select_related("package__survey__institution")
    if g.status_id is None or g.status_id not in valid
]
print(f"\nPrácticas con status NULO/desconocido: {len(anomalous)}")
for g in anomalous:
    inst = g.package.survey.institution.acronym if g.package.survey else "?"
    print(f"  id={g.id} inst={inst} pkg={g.package_id} "
          f"status={g.status_id!r} name={g.name[:30]!r}")

# 2) Foco en UADEC: paquete y prácticas en orden.
uadec = GoodPracticePackage.objects.filter(
    survey__institution__acronym__iexact="UADEC")
for pkg in uadec.select_related("survey__period"):
    print(f"\nPaquete UADEC {pkg.id} periodo "
          f"{pkg.survey.period.year if pkg.survey else '?'} "
          f"status={pkg.status_id!r} has_gp={pkg.has_good_practices}")
    for g in pkg.good_practices.order_by("pk"):
        print(f"  practica id={g.id} status={g.status_id!r} "
              f"name={g.name[:40]!r} axis={g.axis_id} desc?={bool(g.description)}")