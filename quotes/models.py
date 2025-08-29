from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name="quotes")
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    weight = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    # счётчики
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.text[:50]} — {self.source}"


class Vote(models.Model):

    # голос конкретной сессии за конкретную цитату.

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="votes")
    session_key = models.CharField(max_length=40, db_index=True)
    value = models.SmallIntegerField(choices=((1, "like"), (-1, "dislike")))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quote", "session_key"], name="unique_vote_per_session_per_quote"
            )
        ]

    def __str__(self):
        return f"{self.session_key} -> {self.quote_id} ({self.value})"
