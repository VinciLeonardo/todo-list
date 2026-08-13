from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Categoria para organização de tarefas.

    Cada categoria pertence a um usuário (owner) — cada usuário gerencia
    suas próprias categorias, que podem ser aplicadas às suas tarefas.
    """
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text='Cor em hexadecimal, ex: #3B82F6',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'
        # Evita categorias duplicadas com o mesmo nome para o mesmo usuário
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'owner'],
                name='unique_category_name_per_owner',
            )
        ]

    def __str__(self):
        return self.name