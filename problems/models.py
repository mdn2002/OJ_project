from django.db import models
import os
# Create your models here.

def problem_directory_path(instance, filename):
    return os.path.join("problems", instance.problem_code, filename)

class Problem(models.Model):
    problem_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to=problem_directory_path, help_text="Upload the problem statement as a PDF file.")
    checker = models.FileField(upload_to=problem_directory_path, help_text="Upload a checker script.")
    test_cases = models.JSONField(help_text="List of test cases as dictionaries with 'input' and 'output' keys.")
    time_limit = models.FloatField(help_text="Time limit in seconds", default=1.0)
    memory_limit = models.IntegerField(help_text="Memory limit in MB", default=256)

    def __str__(self):
        return self.title
