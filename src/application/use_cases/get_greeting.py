from loguru import logger
from src.domain.value_objects.greeting_message import GreetingMessage


class GetGreetingUseCase:
    def execute(self) -> GreetingMessage:
        logger.debug("Executing GetGreetingUseCase")
        greeting = GreetingMessage(content="Hello, World!")
        logger.debug(f"Created greeting message: {greeting.content}")
        return greeting