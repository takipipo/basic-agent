import requests
import json

class OllamaModel:
    def __init__(self, model, system_prompt, temperature, stop = None) -> None:
        self.model_endpoint = "http://localhost:8000/api/generate"
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.stop = stop

        self.header = {"Content-Type": "application/json"}
        

    def generate_text(self, prompt):

        payload = {
            "model": self.model,
            "format": "json",
            "system": self.system_prompt,
            "prompt": prompt,
            "stream": False,
            "temperature": self.temperature,
            "stop": self.stop
        }

        try:
            print(f"Invoking model {self.model} with payload: {payload}")
            response = requests.post(self.model_endpoint, headers=self.header, json=payload)
            print(f"\n\n Response from Ollama model: {response.json()['response']}")

            return response.json()["response"]
            
            

        except requests.RequestException as e:
            response = {"error": f"Error invoking model! {str(e)}"}
            return response
        