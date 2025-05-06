import requests
import time
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import InterviewQuestion, UserAnswer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@permission_classes([AllowAny])
class SpeechToTextView(APIView):
    def post(self, request):
        # Get audio file from request
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read audio file bytes
            audio_bytes = audio_file.read()

            # Upload audio to AssemblyAI
            upload_url = "https://api.assemblyai.com/v2/upload"
            headers = {"authorization": settings.ASSEMBLYAI_API_KEY}
            upload_response = requests.post(upload_url, headers=headers, data=audio_bytes, timeout=30)
            upload_response.raise_for_status()  # Raise exception for HTTP errors
            upload_data = upload_response.json()
            audio_url = upload_data.get("upload_url")
            if not audio_url:
                return Response({"error": "Failed to upload audio"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Start transcription
            transcript_url = "https://api.assemblyai.com/v2/transcript"
            transcript_request = {
                "audio_url": audio_url,
                # Optional parameters to potentially speed up processing
                "speed_boost": True  # Enable if your AssemblyAI plan supports it
            }
            transcript_response = requests.post(transcript_url, json=transcript_request, headers=headers, timeout=30)
            transcript_response.raise_for_status()  # Raise exception for HTTP errors
            transcript_data = transcript_response.json()
            transcript_id = transcript_data.get("id")
            if not transcript_id:
                return Response({"error": "Failed to start transcription"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Poll for the transcription result with extended timeout
            polling_url = f"{transcript_url}/{transcript_id}"
            max_retries = 20  # Increased from 5 to allow for longer processing time
            retry_count = 0
            polling_interval = 3  # seconds
            
            while retry_count < max_retries:
                polling_response = requests.get(polling_url, headers=headers, timeout=30)
                polling_response.raise_for_status()  # Raise exception for HTTP errors
                polling_data = polling_response.json()
                status_str = polling_data.get("status")
                
                if status_str == "completed":
                    transcribed_text = polling_data.get("text", "")
                    break
                elif status_str == "error":
                    error_message = polling_data.get("error", "Unknown transcription error")
                    return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif status_str in ["processing", "queued"]:
                    # Continue polling when the transcription is still in progress or queued
                    time.sleep(polling_interval)
                    retry_count += 1
                else:
                    # Handle any other unexpected status
                    return Response(
                        {"error": f"Unexpected transcription status: {status_str}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                # If we exceeded max_retries without a completed transcription
                return Response(
                    {"error": "Transcription timed out, please try again later"},
                    status=status.HTTP_504_GATEWAY_TIMEOUT
                )

            # Save the transcribed text with the associated question (if provided)
            question_id = request.data.get("question_id")
            if not question_id:
                return Response(
                    {"error": "question_id is required", "text": transcribed_text}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Debug logging
                print(f"Received question_id: {question_id}")
                
                # Convert question_id to int and handle potential conversion errors
                try:
                    question_id = int(question_id)
                except (TypeError, ValueError):
                    return Response(
                        {"error": f"Invalid question_id format: {question_id}", "text": transcribed_text},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Try to fetch the question
                try:
                    question = InterviewQuestion.objects.get(id=question_id)
                except InterviewQuestion.DoesNotExist:
                    return Response(
                        {"error": f"Question with id {question_id} not found", "text": transcribed_text},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create and save the user answer
                user_answer = UserAnswer.objects.create(
                    question=question,
                    spoken_answer=transcribed_text
                )
                user_answer.save()
                
                return Response({
                    "text": transcribed_text,
                    "question_id": question_id,
                    "answer_id": user_answer.id
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                print(f"Error processing question_id: {str(e)}")  # Debug logging
                return Response(
                    {"error": f"Error processing answer: {str(e)}", "text": transcribed_text},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except requests.exceptions.Timeout:
            return Response(
                {"error": "Request timed out, the server might be experiencing high load"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"API request failed: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
