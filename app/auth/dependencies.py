# app/auth/dependencies.py
from fastapi import Request, HTTPException, status
from app.auth.rate_limiter import rate_limiter
from app.core.config import settings


def rate_limit_register(request: Request):
    """Dependency para limitar requisições em /users (cadastro)"""
    is_allowed, info = rate_limiter.check_rate_limit(
        request=request,
        route="register",
        max_requests=settings.RATE_LIMIT_REGISTER
    )
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Too many registration attempts. Try again later.",
                "retry_after": info["retry_after"],
                "reset_at": info["reset_at"].isoformat()
            }
        )
    
    return info


def rate_limit_login(request: Request):
    """Dependency para limitar requisições em /auth/login"""
    is_allowed, info = rate_limiter.check_rate_limit(
        request=request,
        route="login",
        max_requests=settings.RATE_LIMIT_LOGIN
    )
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Too many login attempts. Try again later.",
                "retry_after": info["retry_after"],
                "reset_at": info["reset_at"].isoformat()
            }
        )
    
    return info


def rate_limit_refresh(request: Request):
    """Dependency para limitar requisições em /auth/refresh"""
    is_allowed, info = rate_limiter.check_rate_limit(
        request=request,
        route="refresh",
        max_requests=settings.RATE_LIMIT_REFRESH
    )
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Too many token refresh attempts. Try again later.",
                "retry_after": info["retry_after"],
                "reset_at": info["reset_at"].isoformat()
            }
        )
    
    return info


def rate_limit_password_recovery(request: Request):
    """Dependency para limitar requisições em /auth/password-recovery"""
    is_allowed, info = rate_limiter.check_rate_limit(
        request=request,
        route="password_recovery",
        max_requests=settings.RATE_LIMIT_PASSWORD_RECOVERY
    )
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Too many password recovery attempts. Try again later.",
                "retry_after": info["retry_after"],
                "reset_at": info["reset_at"].isoformat()
            }
        )
    
    return info