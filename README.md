# Extrator de Etiquetas 📦

API FastAPI para extração de dados de etiquetas de envio usando Google Gemini 2.5 Flash.

## Características

✅ Extração automática de dados de etiquetas  
✅ Suporte a múltiplos formatos de imagem (JPG, PNG, GIF, WebP)  
✅ API REST com documentação automática  
✅ Docker support  
✅ Processamento de imagens otimizado  
✅ Prompt customizável

## Estrutura do Projeto

```
extrator-etiquetas/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Entry point da API
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py      # Lógica de integração com Gemini
│   └── utils/
│       ├── __init__.py
│       └── image_processor.py     # Processamento de imagens
├── temp/                          # Pasta para uploads temporários
├── .env                           # Variáveis de ambiente
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Instalação

### 1. Clone o repositório

```bash
git clone <seu-repo>
cd extrator-etiquetas
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` e adicione sua chave da Google Gemini API:

```env
GOOGLE_API_KEY=sua_chave_aqui
UPLOAD_FOLDER=./temp
MAX_UPLOAD_SIZE=10485760
```

### 3. Instalação Local (sem Docker)

```bash
# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python -m uvicorn app.main:app --reload
```

### 4. Com Docker

```bash
# Build e execute com docker-compose
docker-compose up --build

# Ou manualmente
docker build -t extrator-etiquetas .
docker run -p 8000:8000 -e GOOGLE_API_KEY=sua_chave extrator-etiquetas
```

## Uso da API

### Health Check

```bash
curl http://localhost:8000/health
```

### Extrair Dados de Etiqueta

```bash
curl -X POST -F "file=@etiqueta.jpg" \
  http://localhost:8000/extract
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "destinatario": {
      "nome": "João Silva",
      "pedido": "PED123456"
    },
    "endereco": {
      "cep": "01310-100",
      "bairro": "Centro"
    }
  },
  "message": "Extração realizada com sucesso"
}
```

### Extração com Prompt Customizado

```bash
curl -X POST -F "file=@etiqueta.jpg" \
  -F "prompt=Extraia apenas o código de rastreamento" \
  http://localhost:8000/extract-custom
```

## Documentação Automática

Acesse a documentação interativa:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Como Obter a Chave da Google Gemini API

1. Acesse [Google AI Studio](https://aistudio.google.com/)
2. Clique em "Get API key"
3. Crie uma nova chave de API
4. Copie e cole em `.env`

## Estrutura de Resposta

### Sucesso (200)

```json
{
  "success": true,
  "data": {
    "destinatario": {
      "nome": "string",
      "pedido": "string"
    },
    "endereco": {
      "cep": "string",
      "bairro": "string"
    }
  },
  "message": "Extração realizada com sucesso"
}
```

### Erro (400/500)

```json
{
  "success": false,
  "data": null,
  "message": "Descrição do erro"
}
```

## Endpoints

| Método | Endpoint          | Descrição                     |
| ------ | ----------------- | ----------------------------- |
| GET    | `/`               | Informações da API            |
| GET    | `/health`         | Status da API                 |
| GET    | `/docs`           | Documentação                  |
| POST   | `/extract`        | Extrai dados padrão           |
| POST   | `/extract-custom` | Extrai com prompt customizado |

## Limitações

- Tamanho máximo: 10MB
- Formatos: JPG, PNG, GIF, WebP
- Timeout: 30 segundos

## Troubleshooting

### Erro: "GOOGLE_API_KEY não configurada"

- Verifique se o arquivo `.env` está preenchido
- Reinicie a aplicação

### Erro: "Arquivo inválido"

- Confirme que é uma imagem válida
- Tente converter para JPG
- Verifique o tamanho (máx 10MB)

### Erro de JSON

- Verifique se a etiqueta é legível
- Tente aumentar a qualidade da imagem
- Use o endpoint `/extract-custom` com um prompt mais descritivo

## Variáveis de Ambiente

| Variável          | Padrão     | Descrição                         |
| ----------------- | ---------- | --------------------------------- |
| `GOOGLE_API_KEY`  | -          | Chave da API Gemini (obrigatória) |
| `UPLOAD_FOLDER`   | `./temp`   | Pasta para uploads temporários    |
| `MAX_UPLOAD_SIZE` | `10485760` | Tamanho máximo em bytes           |

## Desenvolvimento

Para adicionar novos modelos ou melhorar a extração:

1. Edite o `EXTRACTION_PROMPT` em `app/services/gemini_service.py`
2. Teste com o endpoint `/extract-custom`
3. Após validar, atualize o prompt padrão

## Performance

- **Modelo**: Gemini 2.5 Flash (rápido e barato)
- **Tempo médio**: 1-2 segundos por imagem
- **Taxa**: ~100 requisições/minuto (depende do plano de API)

## Licença

MIT

## Suporte

Para dúvidas ou issues, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando FastAPI e Google Gemini**
"# extrator_etiquetas" 
