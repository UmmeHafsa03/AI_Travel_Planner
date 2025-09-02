from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config.config import GROQ_API_KEY

# ✅ Groq LLM setup
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",  # or "llama-3.3-70b-versatile" if that's correct
    temperature=0.3
)

# ✅ Dynamic Prompt Template with city, interests, and days
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful travel assistant. Create a {days}-day trip itinerary for {city} based on the user's interests: {interests}. "
     "Give a clear day-wise plan using bullet points. Add local experiences and a realistic flow."),
    ("human", "Create an itinerary for my trip.")
])

# ✅ Main function to generate itinerary
def generate_itineary(city: str, interests: list[str], days: int) -> str:
    formatted_msg = itinerary_prompt.format_messages(
        city=city,
        interests=", ".join(interests),
        days=days
    )

    response = llm.invoke(formatted_msg)
    return response.content