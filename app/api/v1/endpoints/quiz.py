from fastapi import APIRouter, HTTPException
from app.core.config import get_settings
from app.schemas.quiz import QuizRequest, QuizResponse, QuizQuestion
import json
from openai import OpenAI

router = APIRouter()
settings = get_settings()

@router.post("/generate-quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """
    Generate quiz questions for a specific chapter of a book.

    Parameters:
    - book_name: The name of the book
    - chapter_name: The name or number of the chapter
    - author_name: The name of the book's author

    Returns:
    - A list of 3 multiple choice questions with their correct answers
    
    The questions are generated using OpenAI's GPT model and are designed to test
    comprehension of the chapter's key elements, themes, and developments.
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create a contextual prompt
        prompt = f"""
        Based on your knowledge of the book "{request.book_name}" by {request.author_name}, and the chapter title "{request.chapter_name}," generate 3 multiple-choice questions that reflect the key concepts likely discussed in this chapter. Assume the chapter explores ideas related to "{request.chapter_name}" as part of the book's overarching themes.
        
        Format the response as a JSON array with objects containing:
        - question (string)
        - options (array of 3 strings)
        - correct_answer (number 0-2 indicating the index of correct option)        
        
        Return only the JSON array, without any markdown formatting or code block markers.
        """
        
        # Make API call to OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        # Get and clean the response
        response_content = completion.choices[0].message.content.strip()
        
        # Remove markdown code block if present
        if response_content.startswith("```"):
            response_content = response_content.split("\n", 1)[1]  # Remove first line
        if response_content.endswith("```"):
            response_content = response_content.rsplit("\n", 1)[0]  # Remove last line
        
        # Remove "json" if it appears at the start
        response_content = response_content.removeprefix("json")
        
        response_content = response_content.strip()
        print("Cleaned Response:", response_content)  # Debug print

        try:
            # Parse the response
            questions = json.loads(response_content)
            
            # Validate the structure
            validated_questions = []
            for q in questions:
                # Validate required fields
                if not all(key in q for key in ["question", "options", "correct_answer"]):
                    raise ValueError("Missing required fields in question")
                
                # Validate options array length
                if not isinstance(q["options"], list) or len(q["options"]) != 3:
                    raise ValueError("Options must be an array of 3 strings")
                
                # Validate correct_answer is in range
                if not isinstance(q["correct_answer"], int) or q["correct_answer"] not in [0, 1, 2]:
                    raise ValueError("correct_answer must be 0, 1, or 2")

                validated_questions.append(
                    QuizQuestion(
                        question=q["question"],
                        options=q["options"],
                        correct_answer=q["correct_answer"]
                    )
                )

            return QuizResponse(questions=validated_questions)

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")  # Debug print
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse OpenAI response into JSON: {str(e)}"
            )
        except ValueError as e:
            print(f"Validation Error: {str(e)}")  # Debug print
            raise HTTPException(
                status_code=500,
                detail=f"Invalid question format: {str(e)}"
            )

    except Exception as e:
        print(f"General Error: {str(e)}")  # Debug print
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate quiz: {str(e)}"
        ) 