import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

API_KEY = "Private_API_TOKEN"

genai.configure(api_key=API_KEY)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="you are an helpfull, courteous, loyal, and submissive assistant who eagers to serve your master",
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        #HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

history = []

chat_session = model.start_chat(
  history=history
)

def generator(input_user):
    global history
    response = chat_session.send_message(input_user)

    history.append(
        {
            "role": "user",
            "parts": [input_user]
        })
    history.append(
        {
            "role": "model",
            "parts": [response.text]
        })
        
    return response.text