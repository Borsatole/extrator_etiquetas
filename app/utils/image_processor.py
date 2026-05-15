import os
from PIL import Image
from pathlib import Path

class ImageProcessor:
    """Processa imagens antes de enviar para a API Gemini"""
    
    ALLOWED_FORMATS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    MAX_SIZE_MB = 10
    
    @staticmethod
    def validate_image(file_path: str) -> bool:
        """Valida se o arquivo é uma imagem suportada"""
        try:
            ext = Path(file_path).suffix.lower().lstrip('.')
            if ext not in ImageProcessor.ALLOWED_FORMATS:
                return False
            
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > ImageProcessor.MAX_SIZE_MB:
                return False
            
            img = Image.open(file_path)
            img.verify()
            return True
        except Exception as e:
            print(f"Erro na validação: {e}")
            return False
    
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """Carrega e retorna a imagem"""
        try:
            img = Image.open(file_path)
            return img
        except Exception as e:
            raise ValueError(f"Erro ao carregar imagem: {e}")
    
    @staticmethod
    def resize_if_needed(image: Image.Image, max_width: int = 2048) -> Image.Image:
        """Redimensiona imagem se necessário (otimização)"""
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def cleanup(file_path: str) -> None:
        """Remove arquivo temporário"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Erro ao deletar arquivo: {e}")