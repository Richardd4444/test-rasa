from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionConsultarFlujoConError(Action):
    def name(self) -> Text:
        return "action_consultar_flujo_con_error"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id_flujo = tracker.get_slot("id_flujo")

        if not id_flujo:
            dispatcher.utter_message(response="utter_pedir_id_flujo")
            return []

        try:
            response = requests.post("https://mi-api-gateway/errors", json={"id_flujo": id_flujo})
            data = response.json()
            mensaje = data.get("mensaje", "No se encontró información para el flujo.")
        except Exception as e:
            mensaje = f"Ocurrió un error al consultar el flujo: {str(e)}"

        dispatcher.utter_message(text=mensaje)
        return []
