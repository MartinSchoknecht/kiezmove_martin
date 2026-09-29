"""
starts the AI client and Interacts with the user in a chat format. The AI model used is "gemini-3.5-flash-lite".
The user can input messages, and the AI will respond in English. The chat continues until the user types 'exit', 'beenden', or 'quit'. If the AI's response contains the word "erledigt", the chat will also end.
"""

from  google import genai
from google.genai import types

import os

import models

user_fields = models.User.model_fields.keys()  # Access the model fields of the User class

def post_welcome_message():
    welcome_message = """
        Hallo, ich bin dein digitaler Concierge, dein Umzugsassistent. Wie kann ich dir helfen?
    """
    return welcome_message.strip()

def get_user_input(user_input: str | None) -> str:
    if not user_input:
        raise ValueError("User input cannot be None.")
    return user_input.strip()

def process_user_input(user_input: str):    
    if not user_input:
        raise ValueError("User input cannot be empty.")
    administrative_input =f"""Übersetze den folgenden Text ins Deutsche und 
    extrahiere diese Informationen: {list(user_fields)}. 
    Fehlt eine Information, frage in der Originalsprache des Users, die er im ersten post verwendet hat, danach nach, statt zu raten. Text: """
    
    processed_input = administrative_input + user_input.strip()
    return processed_input  # In diesem Beispiel geben wir die Eingabe einfach zurück.


def start_chat():

    #just for DEV-phase
    with genai.Client(api_key="AQ.Ab8RN6I5f-lBRvmPGB_ML-jikYrpNYgsrcPNGv_IPEItDJKxAg") as client:


        chat = client.chats.create(
            model = "gemini-3.5-flash-lite", # modell-Auswahl
            history = []
        )

        agent_start_message ="""
        Du bist der digitale Concierge für neu nach Berlin ziehende Menschen.
        Du hilfst freundlich, klar und in kurzen Sätzen. Du stellst IMMER nur
        eine Frage pro Nachricht und fragst so lange nach, bis die benötigten
        Daten vorhanden sind. Du erfindest niemals Behördendaten - wenn
        du etwas nicht sicher weißt, sagst du das offen. Du sprichst die
        Sprache des Users aber Du füllst die Behördendokumente immer in
        deutscher Sprache aus.
        # Alle erhaltenen Daten speicherst Du sicher ab.
        Du bleibst so lange mit dem User in Kommunikation bis alles abgeschlossen ist. 
        Anschließend wiederholst Du die aufgenommenen Daten in der Form '- Feld : Daten' und fragst ob alles korrekt ist.
        Wenn alles korrekt ist, wiederhole die Daten ein letztes mal und beende den Chat.
        """
        chat.send_message(agent_start_message)

        while True:
            user_input = get_user_input(input("Du: "))

            if user_input.lower() in ['exit', 'beenden', 'quit']:
                print("Chat beendet.")
                break
        
            try:
            # Nachricht an das Modell senden
                response = chat.send_message(process_user_input(user_input))
            
            # Antwort ausgeben
                response_text = response.text if hasattr(response, 'text') else str(response)
                           
                if "erledigt" in response_text.lower():
                    print("Concierge: Aufgabe erledigt. Chat wird beendet.")
                    break
            
                print(f"Concierge: {response_text}\n")
            
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
    
    return response_text  # Return the last response for further processing if needed


def process_last_response(response_text: str):
    response_lines = response_text.splitlines()
    data_dict = {}
    for line in response_lines:
        if line.startswith("- "):
            field_data = line[2:].split(":", 1)
            if len(field_data) == 2:
                field_name = field_data[0].strip()
                field_value = field_data[1].strip()
                data_dict[field_name] = field_value
                print(f"{field_name}: {field_value}")
    return data_dict

if __name__ == "__main__":

    print(user_fields)
    print(post_welcome_message())
    print(process_last_response(start_chat()))








# # import main as m

# from google import genai


# client = genai.Client(api_key="AQ.Ab8RN6I5f-lBRvmPGB_ML-jikYrpNYgsrcPNGv_IPEItDJKxAg")

# welcome_text = "Hallo, wie kann ich Dir beim Umzug helfen?"



# if __name__ == "__main__":
#     user_answer = input(welcome_text)
    
#     prompt_erweiterung = "übersetze ins deutsche:" + user_answer

#     response = client.chat.send_message(
#         model="gemini-2.0-flash",
#         contents=input(prompt_erweiterung),
#     )

#     print(response.text)

    