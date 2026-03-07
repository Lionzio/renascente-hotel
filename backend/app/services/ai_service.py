import json
from typing import Dict, Any
from google import genai
from google.genai import types

from app.core.config import settings


class AiService:
    @staticmethod
    def parse_consumption_text(text: str) -> Dict[str, Any]:
        """
        Lê uma frase natural e devolve um dicionário Python estruturado.
        """
        raw_key = settings.GEMINI_API_KEY
        if not raw_key or raw_key.strip() == "":
            raise ValueError(
                "A chave GEMINI_API_KEY não foi encontrada. Por favor, utilize a inserção manual."
            )

        clean_api_key = raw_key.strip()
        client = genai.Client(api_key=clean_api_key)

        system_instruction = """
        Você é um algoritmo de extração de dados de um sistema hoteleiro (Renascente Hotel).
        Sua ÚNICA função é extrair informações de consumo de um texto e retornar um JSON estrito.
        O JSON deve ter exatamente este formato:
        {
            "room_number": "string",
            "items": [
                {
                    "item_name": "string",
                    "price": 0.0,
                    "quantity": 1
                }
            ]
        }
        Regras de Negócio:
        1. Se o preço não for mencionado, assuma 0.0.
        2. Se a quantidade não for mencionada, assuma 1.
        3. Converta valores monetários para float (ex: "5 reais" vira 5.0).
        4. NUNCA retorne textos amigáveis, saudações ou formatação markdown. Apenas o objeto JSON puro.
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )

            data = json.loads(response.text)
            return data

        except Exception as e:
            error_msg = str(e)
            # Tratamento amigável para cotas excedidas ou chaves bloqueadas pelo Google
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                raise ValueError(
                    "A cota da IA foi bloqueada pelo Google. Por favor, utilize o 'Lançamento Manual'."
                )
            elif "400" in error_msg or "API_KEY_INVALID" in error_msg:
                raise ValueError(
                    "A chave da IA é inválida ou expirou. Por favor, utilize o 'Lançamento Manual'."
                )
            else:
                raise ValueError(f"Falha na IA: {error_msg}")
