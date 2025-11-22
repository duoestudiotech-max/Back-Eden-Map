from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import HTTPException, status, Request
import hashlib

class RateLimiter:
    """
    Sistema de Rate Limiting em memória
    
    Armazena tentativas de acesso por IP + rota
    Reseta automaticamente após 1 hora
    """
    
    def __init__(self):
        # Estrutura: {identifier: {"count": int, "reset_at": datetime}}
        self.requests: Dict[str, Dict] = {}
    
    def _get_identifier(self, ip: str, route: str) -> str:
        """Cria identificador único para IP + rota"""
        return hashlib.sha256(f"{ip}:{route}".encode()).hexdigest()
    
    def _clean_expired(self):
        """Remove registros expirados (otimização)"""
        now = datetime.utcnow()
        expired = [k for k, v in self.requests.items() if v["reset_at"] < now]
        for key in expired:
            del self.requests[key]
    
    def check_rate_limit(self, request: Request, route: str, max_requests: int) -> Tuple[bool, Dict]:
        """
        Verifica se o IP excedeu o limite de requisições
        
        Args:
            request: Request do FastAPI
            route: Nome da rota (ex: "register", "login")
            max_requests: Número máximo de requisições por hora
        
        Returns:
            Tuple[bool, dict]: (is_allowed, info)
        """
        # Limpar registros expirados periodicamente
        self._clean_expired()
        
        # Obter IP do cliente
        ip = request.client.host if request.client else "unknown"
        identifier = self._get_identifier(ip, route)
        
        now = datetime.utcnow()
        
        # Se não existe registro, criar
        if identifier not in self.requests:
            self.requests[identifier] = {
                "count": 1,
                "reset_at": now + timedelta(hours=1)
            }
            return True, {
                "remaining": max_requests - 1,
                "reset_at": self.requests[identifier]["reset_at"]
            }
        
        record = self.requests[identifier]
        
        # Se passou 1 hora, resetar contador
        if now >= record["reset_at"]:
            record["count"] = 1
            record["reset_at"] = now + timedelta(hours=1)
            return True, {
                "remaining": max_requests - 1,
                "reset_at": record["reset_at"]
            }
        
        # Verificar se excedeu limite
        if record["count"] >= max_requests:
            return False, {
                "remaining": 0,
                "reset_at": record["reset_at"],
                "retry_after": int((record["reset_at"] - now).total_seconds())
            }
        
        # Incrementar contador
        record["count"] += 1
        
        return True, {
            "remaining": max_requests - record["count"],
            "reset_at": record["reset_at"]
        }
    
    def get_info(self, request: Request, route: str) -> Dict:
        """Retorna informações sobre o rate limit atual (sem incrementar)"""
        ip = request.client.host if request.client else "unknown"
        identifier = self._get_identifier(ip, route)
        
        if identifier not in self.requests:
            return {"count": 0, "reset_at": None}
        
        return self.requests[identifier]


# Instância global do rate limiter
rate_limiter = RateLimiter()