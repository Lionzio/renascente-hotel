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
        # Trava de Segurança: Verifica se o .env foi carregado corretamente
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "A chave GEMINI_API_KEY não foi encontrada. Verifique seu arquivo .env!"
            )

        # Inicializa o cliente moderno da IA
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # O "System Prompt" de ferro
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
        4. NUNCA retorne textos amigáveis, saudações ou formatação markdown (```json). Apenas o objeto JSON puro.
        """

        try:
            # Faz a chamada para a IA forçando a saída em formato JSON
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # <-- MODELO ATUALIZADO AQUI
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,  # Temperatura baixa = Respostas altamente determinísticas e precisas
                ),
            )

            # Transforma a resposta estrita em um Dicionário Python
            data = json.loads(response.text)
            return data

        except Exception as e:
            raise ValueError(f"Falha de comunicação com o Cérebro: {str(e)}")
