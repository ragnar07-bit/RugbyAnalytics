import json

class Packet:
    # Costruttore di default che rappresenta un pacchetto di rete standard del protocolo RugbyAnalytics
    def __init__(self, action: str, data: str, dict = None):
        self.action = action
        self.data = data if data is not None else{}
    
    #Metodo che converte il pacchetto in stringa JSON per l'invio su Socket TCP
    def to_json_string(self) -> str:
        payload = {
            "Action": self.action,
            "Data": self.data
        }

        return json.dumps(payload) + "\n"
    
    #Metodo factory che converte una stringa JSON in un oggetto
    @staticmethod
    def from_json_string(json_str: str):
        try:
            parsed = json.loads(json_str)

            action = parsed.get("Action", "UNKNOWN")
            data = parsed.get("Data", {})
            
            return Packet(action, data)
        except json.JSONDecodeError as e:
            print(f"[PACKET ERROR] Parsing JSON fallito: {e}")
            return None