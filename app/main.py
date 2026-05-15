import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import tempfile
from pathlib import Path

from app.services import GeminiService
from app.utils import ImageProcessor

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa FastAPI
app = FastAPI(
    title="Extrator de Etiquetas",
    description="API para extração de dados de etiquetas usando Google Gemini",
    version="1.0.0"
)

# Inicializa serviço Gemini
gemini_service = GeminiService(api_key=os.getenv('GOOGLE_API_KEY'))

# Cria pasta temporária se não existir
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './temp')
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Endpoint raiz - retorna informações da API"""
    return {
        "nome": "Extrator de Etiquetas",
        "versão": "1.0.0",
        "endpoints": {
            "POST /extract": "Extrai dados de uma etiqueta (POST com arquivo)",
            "POST /extract-url": "Extrai dados com prompt customizado",
            "GET /health": "Verifica saúde da API"
        }
    }


@app.get("/health")
async def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "ok", "message": "API funcionando normalmente"}


@app.post("/extract")
async def extract_label(file: UploadFile = File(...)):
    """
    Extrai dados de uma etiqueta de envio
    
    - **file**: Arquivo de imagem (JPG, PNG, GIF, WebP)
    
    Retorna: JSON com dados extraídos (destinatario, endereco)
    """
    try:
        # Valida tipo de arquivo
        if file.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
            raise HTTPException(
                status_code=400,
                detail="Formato de imagem não suportado. Use JPG, PNG, GIF ou WebP"
            )
        
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(file.filename).suffix,
            dir=UPLOAD_FOLDER
        ) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            temp_path = tmp_file.name
        
        try:
            # Valida imagem
            if not ImageProcessor.validate_image(temp_path):
                raise HTTPException(
                    status_code=400,
                    detail="Arquivo inválido ou muito grande (máx 10MB)"
                )
            
            # Extrai dados
            result = gemini_service.extract_label_data(temp_path)
            
            # Retorna resultado
            if result["success"]:
                return JSONResponse(
                    status_code=200,
                    content=result
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content=result
                )
        
        finally:
            # Limpa arquivo temporário
            ImageProcessor.cleanup(temp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erro interno: {str(e)}"
            }
        )


@app.post("/extract-custom")
async def extract_custom(file: UploadFile = File(...), prompt: str = None):
    """
    Extrai dados com um prompt customizado
    
    - **file**: Arquivo de imagem
    - **prompt**: Prompt customizado (opcional)
    
    Retorna: Resposta customizada da IA
    """
    try:
        if file.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
            raise HTTPException(
                status_code=400,
                detail="Formato de imagem não suportado"
            )
        
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(file.filename).suffix,
            dir=UPLOAD_FOLDER
        ) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            temp_path = tmp_file.name
        
        try:
            if not ImageProcessor.validate_image(temp_path):
                raise HTTPException(status_code=400, detail="Arquivo inválido")
            
            custom_prompt = prompt or "Descreva o que você vê nesta imagem."
            result = gemini_service.extract_custom(temp_path, custom_prompt)
            
            return JSONResponse(
                status_code=200 if result["success"] else 400,
                content=result
            )
        
        finally:
            ImageProcessor.cleanup(temp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)}
        )


@app.get("/docs")
async def get_docs():
    """Retorna documentação da API"""
    return {
        "titulo": "Extrator de Etiquetas - API Documentation",
        "versao": "1.0.0",
        "endpoints": {
            "GET /": "Informações da API",
            "GET /health": "Status da API",
            "POST /extract": "Extrai dados padrão de etiqueta",
            "POST /extract-custom": "Extrai com prompt customizado"
        },
        "exemplo_uso": {
            "curl": "curl -X POST -F 'file=@etiqueta.jpg' http://localhost:8000/extract",
            "python": "requests.post('http://localhost:8000/extract', files={'file': open('etiqueta.jpg', 'rb')})"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )