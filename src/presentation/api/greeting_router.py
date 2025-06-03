from fastapi import APIRouter, status
from loguru import logger
from src.application.use_cases.get_greeting import GetGreetingUseCase
from src.application.use_cases.create_personalized_greeting import CreatePersonalizedGreetingUseCase
from src.presentation.api.dtos.greeting_dtos import GreetingResponse, PersonalizedGreetingRequest

router = APIRouter(
    prefix="/greeting",
    tags=["greeting"],
)


@router.get(
    "",
    response_model=GreetingResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a greeting message",
    description="Returns a simple greeting message",
    response_description="Successful greeting response",
)
async def get_greeting() -> GreetingResponse:
    """Get a greeting message."""
    logger.info("Received request to GET /greeting")
    use_case = GetGreetingUseCase()
    greeting = use_case.execute()
    response = greeting.to_dict()
    logger.info(f"Returning response: {response}")
    return GreetingResponse(**response)


@router.post(
    "/personalized",
    response_model=GreetingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a personalized greeting",
    description="Creates a personalized greeting message based on the provided name and language",
    response_description="Personalized greeting response",
)
async def create_personalized_greeting(request: PersonalizedGreetingRequest) -> GreetingResponse:
    """Create a personalized greeting message."""
    logger.info(f"Received request to POST /greeting/personalized")
    
    # Call use case with request data
    use_case = CreatePersonalizedGreetingUseCase()
    greeting = use_case.execute(
        name=request.name,
        language=request.language
    )
    
    # Convert domain object to response DTO
    response = greeting.to_dict()
    logger.info(f"Returning response: {response}")
    return GreetingResponse(**response)