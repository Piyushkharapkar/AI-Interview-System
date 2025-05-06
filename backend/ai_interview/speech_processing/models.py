from django.db import models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from interviews.models import InterviewQuestion

class UserAnswer(models.Model):
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    spoken_answer = models.TextField()
    similarity_score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def calculate_similarity(self):
        """Calculate Cosine Similarity between expected and spoken answer."""
        expected_answer = self.question.expected_answer
        user_answer = self.spoken_answer

        if not expected_answer or not user_answer:
            return 0.0  # No answer available

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([expected_answer, user_answer])
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

        return round(similarity * 10, 2)  # Scale similarity to 0-10 range

    def generate_feedback(self):
        """Generate polite and precise feedback based on similarity score (1-10)."""
        if self.similarity_score is None or self.similarity_score < 1:
            return "Thank you for your effort. Please review the material and try to provide a more detailed answer next time."

        score = self.similarity_score

        if score >= 9:
            return "Outstanding answer! Your response is nearly perfect. Excellent work!"
        elif score >= 8:
            return "Excellent answer! Your response is very close to the expected one. Keep up the great work!"
        elif score >= 7:
            return "Great answer! There are just a few minor areas that could be refined."
        elif score >= 6:
            return "Good answer! With a bit more detail, you could make it even better."
        elif score >= 5:
            return "Your answer is fair. Consider adding a few more details for clarity."
        elif score >= 4:
            return "Your answer is average. A bit more detail might enhance your response."
        elif score >= 3:
            return "Your answer could be clearer. Adding more details would be beneficial."
        elif score >= 2:
            return "Your answer seems to be missing some important points. Please consider expanding your response."
        elif score >= 1.5:
            return "Your answer is minimal. A little more detail could make a significant difference."
        elif score >= 1:
            return "Your answer is quite limited. Significant improvement is possible with additional detail."
        else:
            return "Thank you for your effort. Please review the material and try to provide a more detailed answer next time."

    def save(self, *args, **kwargs):
        """Compute similarity and feedback before saving."""
        self.similarity_score = self.calculate_similarity()
        self.feedback = self.generate_feedback()
        super(UserAnswer, self).save(*args, **kwargs)

    def __str__(self):
        return f"Answer for: {self.question.question[:30]} - Score: {self.similarity_score}"
