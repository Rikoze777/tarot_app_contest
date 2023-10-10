from uuid import uuid4
from django.db import models


class User(models.Model):
    tg_id = models.CharField(
        'Telegram ID',
        max_length=20,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.tg_id}'


class Card(models.Model):
    card = models.CharField("Card", max_length=20, db_index=True)
    image = models.ImageField('Image', null=True, blank=True,)
    finance = models.TextField('finance description')
    love = models.TextField('love description')
    day = models.TextField('day description')
    advise = models.TextField('advise description')
    yes_or_no = models.TextField('yes or no description')

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def str(self):
        return f'{self.card}'
    
    def getDescription(card, prediction_type: str):
        if prediction_type == 'yes_or_no':
            return card.yes_or_no
        elif prediction_type == 'advise':
            return card.advise
        elif prediction_type == 'day':
            return card.day
        elif prediction_type == 'love':
            return card.love
        elif prediction_type == 'finance':
            return card.finance
        return card.day


class Prediction(models.Model):
    user = models.ForeignKey(User,
                             related_name='predictions',
                             on_delete=models.CASCADE)
    card = models.ForeignKey(Card,
                                  related_name='predictions',
                                  on_delete=models.CASCADE)
    date = models.DateTimeField('Date')
    prediction = models.CharField("Prediction", max_length=15, db_index=True,)

    class Meta:
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return f'{self.user.tg_id}'


class Subscription(models.Model):
    user = models.ForeignKey(User,
                                related_name='subscriptions',
                                on_delete=models.CASCADE)
    date_from = models.DateTimeField('Subscription start', null=True, blank=True)
    date_end = models.DateTimeField('Subscription end', null=True, blank=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.user.tg_id}"


class Invoice(models.Model):
    user = models.ForeignKey(User,
                             related_name='Invoices',
                             on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return f"{self.user.tg_id} {self.uuid}"
