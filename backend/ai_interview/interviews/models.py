from django.db import models

class InterviewQuestion(models.Model):
    domain = models.CharField(max_length=255)
    skills = models.CharField(max_length=255 , default="Unknown")
    experience = models.CharField(max_length=50)
    question = models.TextField()
    expected_answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question
