from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=128)
    initial_moisture = models.IntegerField()
    final_moisture = models.IntegerField()
    bulk_density = models.IntegerField()


class Temperature(models.Model):
    dimensionless_param = models.DecimalField(max_digits=3, decimal_places=2)
    boiling_point = models.IntegerField()
    freezing_point = models.IntegerField()
    radiation_intensity = models.IntegerField()
    solar_constant = models.IntegerField()


class Pressure(models.Model):
    partial_pressure = models.IntegerField()
    heat_capacity = models.IntegerField()


class Vaporization(models.Model):
    specific_gass_constant = models.DecimalField(max_digits=4, decimal_places=1)
    vapour_gass_constant = models.DecimalField(max_digits=4, decimal_places=1)
    boiling_point = models.IntegerField()
    critical_pressure = models.IntegerField()
    critical_temperature = models.IntegerField()


class Rate(models.Model):
    drying_time = models.DurationField(default="24:00:00")
    air_density = models.DecimalField(max_digits=2, decimal_places=1)


class DryerArea(models.Model):
    efficiency = models.DecimalField(max_digits=4, decimal_places=3)
    thickness = models.DecimalField(max_digits=3, decimal_places=2)













