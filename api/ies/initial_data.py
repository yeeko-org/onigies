from ies.models import Period


class InitPeriod:
    def __init__(self):
        Period.objects.get_or_create(year=2025)

