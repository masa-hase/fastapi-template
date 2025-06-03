from src.domain.value_objects.personalized_greeting import PersonalizedGreeting


class CreatePersonalizedGreetingUseCase:
    """Use case for creating personalized greetings."""
    
    def execute(self, name: str, language: str) -> PersonalizedGreeting:
        """
        Execute the use case to create a personalized greeting.
        
        Args:
            name: The name of the person to greet
            language: The language for the greeting
            
        Returns:
            PersonalizedGreeting value object
        """
        # Create domain value object
        greeting = PersonalizedGreeting(
            name=name,
            language=language
        )
        
        # In a real application, you might:
        # - Save to a repository
        # - Trigger domain events
        # - Apply business rules
        # - Integrate with other services
        
        return greeting