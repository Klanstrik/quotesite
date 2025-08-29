import random
from typing import Optional
from .models import Quote

def get_weighted_random_quote() -> Optional[Quote]:
    qs = Quote.objects.filter(is_active=True).only("id", "weight")
    items = list(qs.values_list("id", "weight"))
    if not items:
        return None
    total = sum(w for _, w in items)
    r = random.randint(1, total)
    acc = 0
    for _id, w in items:
        acc += w
        if acc >= r:
            return Quote.objects.select_related("source").get(id=_id)
