import json
import google.generativeai as genai
from PIL import Image
import os

class GeminiService:
    """Serviço para comunicação com Google Generative AI (Gemini)"""
    
    EXTRACTION_PROMPT = """Analise a imagem da etiqueta de envio e extraia os dados EXATAMENTE neste formato JSON:
{
    "destinatario": {
        "nome": "",
        "pedido": ""
    },
    "endereco": {
        "cep": "",
        "logradouro": "",
        "numero": "",
        "bloco": "",
        "apartamento": "",
        "casa": "",
        "lote": "",
        "quadra": "",
        "bairro": "",
        "cidade": "",
        "complemento": "",
        "uf": ""
    }
}

Regras importantes:
- Retorne APENAS o JSON válido, sem textos explicativos
- Se um campo não for encontrado, deixe vazio ""
- Não adicione campos extras
- Valide se o JSON está bem formatado

Responda com o JSON puro."""
    
    def __init__(self, api_key: str):
        """Inicializa o serviço com a chave da API"""
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não configurada")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_label_data(self, image_path: str) -> dict:
        """
        Extrai dados da etiqueta usando Gemini
        
        Args:
            image_path: Caminho para o arquivo de imagem
            
        Returns:
            dict com os dados extraídos
        """
        try:
            # Carrega a imagem
            image = Image.open(image_path)
            
            # Envia para Gemini
            response = self.model.generate_content(
                [self.EXTRACTION_PROMPT, image]
            )
            
            # Extrai o texto da resposta
            response_text = response.text.strip()
            
            # Remove possíveis markdown backticks
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            extracted_data = json.loads(response_text)
            
            return {
                "success": True,
                "data": extracted_data,
                "message": "Extração realizada com sucesso"
            }
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erro ao parsear JSON: {str(e)}",
                "raw_response": response_text
            }
        except FileNotFoundError:
            return {
                "success": False,
                "data": None,
                "message": "Arquivo de imagem não encontrado"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erro na extração: {str(e)}"
            }
    
    def extract_custom(self, image_path: str, custom_prompt: str) -> dict:
        """
        Extrai dados com prompt customizado
        
        Args:
            image_path: Caminho para o arquivo de imagem
            custom_prompt: Prompt customizado
            
        Returns:
            dict com os dados extraídos
        """
        try:
            image = Image.open(image_path)
            response = self.model.generate_content(
                [custom_prompt, image]
            )
            
            return {
                "success": True,
                "data": response.text,
                "message": "Extração com prompt customizado realizada"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erro: {str(e)}"
            }