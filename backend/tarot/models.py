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
    card = models.CharField("Card", max_length=40, db_index=True,)
    image = models.ImageField('Image', null=True, blank=True,)
    finance = models.TextField('finance description')
    love = models.TextField('love description')
    day = models.TextField('day description')
    advise = models.TextField('advise description')
    triple = models.TextField('triple description')
    yes_or_no = models.TextField('yes or no description')

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return f'{self.card}'


class Prediction(models.Model):
    user = models.ForeignKey(User,
                             related_name='predictions',
                             on_delete=models.CASCADE)
    card = models.ManyToManyField(Card,
                                  related_name='predictions',)
    date = models.DateTimeField('Date')
    finance_flag = models.PositiveIntegerField('finance_flag')
    love_flag = models.PositiveIntegerField('love_flag')
    day_flag = models.PositiveIntegerField('day_flag')
    advise_flag = models.PositiveIntegerField('advise_flag')
    triple_flag = models.PositiveIntegerField('triple_flag')
    yes_or_no_flag = models.PositiveIntegerField('yes_or_no_flag')

    class Meta:
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return f'{self.user.tg_id}-{self.user.name}'


class Subscription(models.Model):
    class UserRole(models.TextChoices):
        USER = "U", "User"
        LEVEL1 = "L1", "Magic user"

    role = models.CharField(
        'Subscription level',
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    user = models.OneToOneField(User,
                                related_name='subscriptions',
                                on_delete=models.CASCADE)
    is_subscribed = models.BooleanField('Status', default=False)
    date_from = models.DateTimeField('Subscription start', null=True, blank=True)
    date_end = models.DateTimeField('Subscription end', null=True, blank=True)
    price = models.PositiveIntegerField('Price', null=True, blank=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.user.tg_id}"
