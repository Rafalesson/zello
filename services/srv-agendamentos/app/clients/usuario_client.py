# app/clients/usuario_client.py
import httpx
import uuid
from typing import Dict, Any

# Usaremos um serviço "singleton" para reutilizar o cliente HTTP
class UsuarioClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        # Usamos um cliente assíncrono para não bloquear a aplicação
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def validate_user_by_id(self, user_id: uuid.UUID) -> Dict[str, Any] | None:
        """
        Valida um ID de usuário ligando para o srv-usuarios.
        Retorna os detalhes do usuário se for válido e ativo, caso contrário None.
        """
        try:
            # O srv-usuarios não precisa de token para esta validação interna,
            # pois a comunicação ocorre na rede privada do Docker.
            # Em produção, usaríamos mTLS ou um token de serviço.
            response = await self.client.get(f"/usuarios/validate/{user_id}")
            response.raise_for_status() # Lança exceção para status 4xx ou 5xx
            return response.json()
        except httpx.HTTPStatusError as e:
            # Se o usuário não for encontrado (404), retorna None
            if e.response.status_code == 404:
                return None
            # Para outros erros, podemos querer logar ou relançar
            raise
        except httpx.RequestError:
            # Erro de conexão com o serviço de usuários
            return None

# Instância única do cliente
usuario_client = UsuarioClient(base_url="http://usuarios-service:8000/api/v1")