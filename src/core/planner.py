from langchain_core.messages import HumanMessage, AIMessage
from src.chains.itinerary_chain import generate_itineary
from src.utils.logger import get_logger
from src.utils.custom_exception import CustomException

logger = get_logger(__name__)

class TravelPlanner:
    def __init__(self):
        self.messages = []
        self.city = ""
        self.interests = []
        self.days = 3  # ✅ default number of days
        self.itineary = ""

        logger.info("Initialized TravelPlanner instance")

    def set_city(self, city: str):
        try:
            self.city = city
            self.messages.append(HumanMessage(content=city))
            logger.info("City set successfully")
        except Exception as e:
            logger.error(f"Error while setting city: {e}")
            raise CustomException("Failed to set city", e)

    def set_interests(self, interests_str: str):
        try:
            self.interests = [i.strip() for i in interests_str.split(",")]
            self.messages.append(HumanMessage(content=interests_str))
            logger.info("Interests set successfully")
        except Exception as e:
            logger.error(f"Error while setting interests: {e}")
            raise CustomException("Failed to set interests", e)

    def set_days(self, days: int):
        try:
            self.days = days
            self.messages.append(HumanMessage(content=f"Trip duration: {days} days"))
            logger.info("Days set successfully")
        except Exception as e:
            logger.error(f"Error while setting days: {e}")
            raise CustomException("Failed to set days", e)

    def create_itineary(self):
        try:
            logger.info(f"Generating itinerary for {self.city}, Days: {self.days}, Interests: {self.interests}")
            itineary = generate_itineary(self.city, self.interests, self.days)  # ✅ updated to include days
            self.itineary = itineary
            self.messages.append(AIMessage(content=itineary))
            logger.info("Itinerary generated successfully")
            return itineary
        except Exception as e:
            logger.error(f"Error while creating itinerary: {e}")
            raise CustomException("Failed to create itinerary", e)