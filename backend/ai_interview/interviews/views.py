import google.generativeai as genai
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import InterviewQuestion
from .serializer import InterviewQuestionSerializer
import re  # Import regex to clean text
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# Configure Google Gemini API
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)


@permission_classes([AllowAny])
class GenerateQuestionsView(APIView):
    def post(self, request):
        domain = request.data.get("domain")
        skills = request.data.get("skills")
        experience = request.data.get("experience")

        if not domain or not skills or not experience:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Updated prompt to include HR & Scenario-based questions
        prompt = f"""
        You are a senior software engineer
        Generate interview questions for a candidate in the {domain} domain 
        with the following skills: {skills}. The candidate has {experience} years of experience. 
        
        Provide:
        - 3 technical questions relevant to the skills
        - 1 scenario-based questions to test problem-solving skills
        - 1 HR question to assess soft skills 

        Each question should have a short and precise answer (3-4 lines).  
        Format the output as: 'Q: [question] A: [answer]'.
        """

        try:
            # Generate questions using Gemini AI
            model = genai.GenerativeModel("gemini-2.0-flash")  # Ensure this model is available
            response = model.generate_content(prompt)

            # Extract questions and answers using regex
            pattern = r"Q:\s*(.+?)\s*A:\s*(.+)"
            matches = re.findall(pattern, response.text.strip())    

            if not matches:
                return Response({"error": "Failed to extract valid questions and answers"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Store extracted questions and answers
            saved_questions = []
            for question, answer in matches:
                interview_question = InterviewQuestion.objects.create(
                    domain=domain,
                    skills=skills,
                    experience=experience,
                    question=question.strip(),
                    expected_answer=answer.strip()
                )
                saved_questions.append(interview_question)

        except Exception as e:
            return Response({"error": f"Failed to generate questions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return cleaned questions and answers
        serializer = InterviewQuestionSerializer(saved_questions, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
