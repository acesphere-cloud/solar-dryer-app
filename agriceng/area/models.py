from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=128, unique=True)
    initial_moisture = models.IntegerField()
    final_moisture = models.IntegerField()
    bulk_density = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Coefficient(models.Model):
    AIRFLOW = 'airflow'
    AIRVOLUME = 'air volume'
    VAPOURIZATION = 'vaporization'
    FLOWRATE = 'flow rate'
    COLLECTORAREA = 'collector area'
    CHIMNEY = 'chimney'
    DRYINGBED = 'drying bed'
    EQUATION_CHOICES = [
        (AIRFLOW, 'Airflow'),
        (AIRVOLUME, 'Air Volume'),
        (VAPOURIZATION, 'Vaporization'),
        (FLOWRATE, 'Flow Rate'),
        (COLLECTORAREA, 'Collector Area'),
        (CHIMNEY, 'Chimney'),
        (DRYINGBED, 'Drying Bed'),
    ]
    coefficient = models.CharField(max_length=128, )
    units = models.CharField(max_length=64, blank=True)
    symbol = models.CharField(max_length=16)
    equivalent = models.FloatField()
    equation = models.CharField(max_length=16, choices=EQUATION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['coefficient', 'equation'], name='common_coefficients')
        ]
        ordering = ['created', ]

    def __str__(self):
        return str(self.coefficient)

    def save(self, *args, **kwargs):
        # Remove leading and trailing spaces on coefficients
        coefficient = self.coefficient.strip()
        # Remove capital letters on coefficients
        self.coefficient = coefficient.lower()
        # Call the "real" save() method.
        super().save(*args, **kwargs)

