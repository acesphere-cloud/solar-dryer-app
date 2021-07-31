from django.db import models


def dryer_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/dryers/<size>/<version>/<filename>
    return 'dryers/{0}/{1}/{2}'.format(instance.size, instance.version, filename)


class Dryer(models.Model):
    SMALL = 'SM'
    LARGE = 'LA'
    SIMPLE = 'SI'
    IMPROVED = 'IM'
    SIZE_CHOICES = [(SMALL, 'Small'), (LARGE, 'Large'), ]
    VERSION_CHOICES = [(SIMPLE, 'Simple'), (IMPROVED, 'Improved'), ]
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, )
    version = models.CharField(max_length=2, choices=VERSION_CHOICES, )
    diagram = models.ImageField(upload_to=dryer_directory_path)
    construct = models.ImageField(upload_to=dryer_directory_path, blank=True)
    variation = models.ImageField(upload_to=dryer_directory_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-size', '-version']

    def get_size(self):
        size = [i[1] for i in self.SIZE_CHOICES if i[0] == self.size]
        return size.pop()

    def get_version(self):
        version = [i[1] for i in self.VERSION_CHOICES if i[0] == self.version]
        return version.pop()

    def __str__(self):
        return self.get_size() + " " + self.get_version() + " Dryer"


class Note(models.Model):
    note = models.TextField(max_length=256)
    dryer = models.ForeignKey(Dryer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['dryer', 'created', 'modified']

    def __str__(self):
        return str(self.dryer) + ": " + self.note[:21] + "..."

    def save(self, *args, **kwargs):
        # Remove leading and trailing spaces on notes
        self.note = self.note.strip()
        # Call the "real" save() method.
        super().save(*args, **kwargs)
