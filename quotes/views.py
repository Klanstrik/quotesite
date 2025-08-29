import random
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Quote, Vote
from .forms import QuoteForm, SourceForm


def _ensure_session_key(request):
    #Гарантируем наличие session_key для идентификации пользователя по сессии
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _weighted_random_quote():

    #Возвращает случайную активную цитату с учётом «веса».

    qs = Quote.objects.filter(is_active=True)
    if not qs.exists():
        return None

    ids_weights = list(qs.values_list("id", "weight"))
    # Упрощённо размножаем id по весу (для начального проекта достаточно)
    population = [qid for qid, w in ids_weights for _ in range(max(int(w or 1), 1))]
    choice_id = random.choice(population)
    return qs.get(id=choice_id)


# ---------- Публичные страницы ----------

def home(request):
    #Случайная цитата + учёт просмотров и инфо о голосе пользователя
    quote = _weighted_random_quote()
    if quote is None:
        return render(request, "quotes/empty.html")

    Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
    quote.refresh_from_db(fields=["views"])

    session_key = _ensure_session_key(request)
    vote = Vote.objects.filter(session_key=session_key, quote=quote).first()
    voted_value = vote.value if vote else 0

    return render(request, "quotes/home.html", {"quote": quote, "voted_value": voted_value})


def popular(request):
    # ТОП-10 популярных цитат
    quotes = list(
        Quote.objects.filter(is_active=True)
        .order_by("-likes", "dislikes", "-views", "-created_at")[:10]
    )

    # Отметим, голосовал ли текущий пользователь за каждую из цитат
    session_key = _ensure_session_key(request)
    votes = Vote.objects.filter(session_key=session_key, quote__in=quotes)
    voted_map = {v.quote_id: v.value for v in votes}
    for q in quotes:
        q.voted_value = voted_map.get(q.id, 0)

    return render(request, "quotes/popular.html", {"quotes": quotes})


# ---------- Формы добавления ----------

def add_quote(request):
    form = QuoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "quotes/add_quote.html", {"qf": form})


def add_source(request):
    form = SourceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("add_quote")
    return render(request, "quotes/add_source.html", {"sf": form})


# ---------- Голосование ----------

@require_http_methods(["GET", "POST"])
def vote(request, pk):
    """
    один голос (лайк или дизлайк) на цитату на сессию.
    оаботает в двух режимах:
      - обычная HTML-форма (POST)
      - HTMX (hx-post/hx-get)
    """
    quote = get_object_or_404(Quote, pk=pk, is_active=True)
    session_key = _ensure_session_key(request)

    existing = Vote.objects.filter(session_key=session_key, quote=quote).first()

    raw = request.POST.get("value", request.GET.get("value", "0"))
    try:
        value = int(raw)
    except ValueError:
        value = 0

    if not existing and value in (1, -1):
        if value == 1:
            Quote.objects.filter(pk=pk).update(likes=F("likes") + 1)
        else:
            Quote.objects.filter(pk=pk).update(dislikes=F("dislikes") + 1)
        Vote.objects.create(quote=quote, session_key=session_key, value=value)

    # Готовим актуальные данные для ответа
    quote.refresh_from_db(fields=["likes", "dislikes"])
    voted_value = existing.value if existing else (value if value in (1, -1) else 0)

    #  вернём кусок рейтинга
    if request.headers.get("HX-Request") == "true":
        return render(request, "quotes/_rating.html", {"quote": quote, "voted_value": voted_value})

    # Обычный запрос
    return redirect(request.META.get("HTTP_REFERER") or reverse("home"))
