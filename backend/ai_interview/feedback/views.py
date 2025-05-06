from django.http import JsonResponse
from speech_processing.models import UserAnswer


def evaluate_answers(request):
    # Fetch the last three UserAnswer records (most recent ones) by ordering by id
    user_answers = UserAnswer.objects.all().order_by('-id')[:5]
    
    if not user_answers.exists():
        return JsonResponse({"message": "No answers found"}, status=400)

    # Reverse to show in chronological order (oldest first)
    user_answers = list(user_answers)[::-1]

    results = [{
        "question": answer.question.question,
        "expected_answer": answer.question.expected_answer,
        "spoken_answer": answer.spoken_answer,
        "similarity_score": answer.similarity_score,
        "feedback": answer.feedback
    } for answer in user_answers]

    avg_rating = sum(
        [answer.similarity_score for answer in user_answers if answer.similarity_score is not None]
    ) / max(len(user_answers), 1)

    return JsonResponse({"results": results, "rating": round(avg_rating, 2)}, safe=False)
