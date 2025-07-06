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

        nit = tracker.get_slot("NIT")

        if not nit:
            dispatcher.utter_message(response="utter_pedir_id_flujo")
            return []

        try:
            response = requests.post("https://m1zngptzf5.execute-api.us-east-2.amazonaws.com/dev/test-virtual-assistant", json={"NIT": nit})
            data = response.json()
            mensaje = data.get("mensaje", "No se encontró información para el flujo.")
        except Exception as e:
            mensaje = f"Ocurrió un error al consultar el flujo: {str(e)}"

        dispatcher.utter_message(text=mensaje)
        return []
