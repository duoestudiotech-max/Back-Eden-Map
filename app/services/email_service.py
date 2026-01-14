# app/services/email_service.py
import requests
import logging
from typing import Optional
from app.core.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('app.services.email_service')

class BrevoEmailService:
    """Serviço para enviar emails através da API do Brevo"""
    
    BASE_URL = "https://api.brevo.com/v3"
    
    def __init__(self, api_key: str):
        """
        Inicializa o serviço Brevo
        
        Args:
            api_key: Chave de API do Brevo
        """
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key
        }
    
    def enviar_email_simples(
        self,
        destinatario: str,
        assunto: str,
        corpo_html: str,
        remetente_email: str = None,
        remetente_nome: str = None
    ) -> bool:
        """
        Envia um email simples através do Brevo
        
        Args:
            destinatario: Email do destinatário
            assunto: Assunto do email
            corpo_html: Corpo do email em HTML
            remetente_email: Email de origem (usa settings se None)
            remetente_nome: Nome de quem envia (usa settings se None)
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            url = f"{self.BASE_URL}/smtp/email"
            
            payload = {
                "sender": {
                    "name": remetente_nome or settings.BREVO_SENDER_NAME,
                    "email": remetente_email or settings.BREVO_SENDER_EMAIL
                },
                "to": [
                    {
                        "email": destinatario,
                        "name": destinatario.split("@")[0]
                    }
                ],
                "subject": assunto,
                "htmlContent": corpo_html
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)

            if response.status_code in [200, 201]:
                logger.info(f"✅ Email enviado com sucesso para {destinatario}")
                logger.debug(f"Response: {response.json()}")
                return True
            else:
                logger.error(f"❌ Erro ao enviar email: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro de conexão com Brevo: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao enviar email: {str(e)}")
            return False
    
    def enviar_boas_vindas(
        self,
        email: str,
        login: str,
        plan: str = "trial"
    ) -> bool:
        """
        Envia email de boas-vindas para novo usuário
        
        Args:
            email: Email do usuário
            login: Login do usuário
            plan: Plano contratado
            
        Returns:
            True se enviado com sucesso
        """
        planos_nomes = {
            "trial": "Teste Grátis (15 dias)",
            "mensal": "Mensal",
            "trimestral": "Trimestral", 
            "semestral": "Semestral",
            "anual": "Anual",
            "admin": "Administrador"
        }
        
        plano_nome = planos_nomes.get(plan.lower(), plan)
        
        assunto = f"Bem-vindo ao Eden Map, {login}! 🌿"
        
        corpo_html = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bem-vindo ao Eden Map</title>
            </head>

            <body style="margin:0;padding:0;background:#212224;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#212224;padding:40px 20px;">
            <tr>
            <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="background:#3A3A3A;border-radius:20px;overflow:hidden;max-width:100%;box-shadow:0 20px 60px rgba(0,0,0,0.5);">

            <tr>
            <td align="center" style="background:#7a3ed427;padding:50px 40px;">
            <img src="https://i.imgur.com/27UnNn7.png" alt="Eden Map" style="max-width:200px;height:auto;display:block;margin-bottom:20px;">
            <h1 style="color:#ffffff;font-size:32px;font-weight:700;margin:0;">Bem-vindo!</h1>
            </td>
            </tr>

            <tr>
            <td style="padding:50px 40px;">

            <p style="color:#e2e8f0;font-size:18px;line-height:1.8;text-align:center;margin:0 0 30px 0;">
            Olá <strong style="color:#ffffff;font-size:20px;">{login}</strong>,
            </p>

            <p style="color:#cbd5e0;font-size:16px;line-height:1.8;text-align:center;margin:0 0 30px 0;">
            É com grande satisfação que damos as boas-vindas ao
            <strong style="color:#8a4aed;">Eden Map</strong>!
            Sua conta foi criada com sucesso e você já pode começar a explorar todas as funcionalidades da nossa plataforma.
            </p>

            <table width="100%" cellpadding="0" cellspacing="0" style="background:rgba(26,29,41,0.5);border-radius:12px;border:1px solid rgba(138,74,237,0.2);margin:30px 0;">
            <tr>
            <td style="padding:25px;">
            <h3 style="color:#ffffff;font-size:18px;margin:0 0 20px 0;">📋 Informações da Conta</h3>

            <table width="100%" cellpadding="8" cellspacing="0">
            <tr>
            <td style="color:#94a3b8;font-size:14px;">Login:</td>
            <td style="color:#ffffff;font-size:14px;font-weight:600;text-align:right;">{login}</td>
            </tr>
            <tr>
            <td style="color:#94a3b8;font-size:14px;">Email:</td>
            <td style="color:#ffffff;font-size:14px;font-weight:600;text-align:right;">{email}</td>
            </tr>
            <tr>
            <td style="color:#94a3b8;font-size:14px;">Plano:</td>
            <td style="color:#8a4aed;font-size:14px;font-weight:600;text-align:right;">{plano_nome}</td>
            </tr>
            </table>

            </td>
            </tr>
            </table>

            <div style="background:rgba(255,170,46,0.1);border-left:4px solid #ffaa2e;padding:20px;border-radius:8px;margin:30px 0;">
            <p style="color:#ffaa2e;font-size:15px;line-height:1.6;margin:0;">
            <strong>💡 Dica de Segurança:</strong><br>
            Mantenha suas credenciais seguras e nunca compartilhe com terceiros.
            Seu token de acesso é pessoal e intransferível.
            </p>
            </div>

            </td>
            </tr>

            <tr>
            <td style="background:rgba(26,29,41,0.8);padding:30px 40px;text-align:center;border-top:1px solid rgba(138,74,237,0.2);">
            <p style="color:#94a3b8;font-size:14px;margin:0 0 10px 0;">
            <strong style="color:#ffffff;">Eden Map</strong>
            </p>
            <p style="color:#64748b;font-size:13px;margin:0 0 10px 0;">
            © 2025 Eden Map. Todos os direitos reservados.
            </p>
            <p style="color:#64748b;font-size:12px;margin:0;line-height:1.6;">
            Este é um email automático, não responda.<br>
            Se você não criou esta conta, ignore este email.
            </p>
            </td>
            </tr>

            </table>

            </td>
            </tr>
            </table>
            </body>
            </html>
        """

        return self.enviar_email_simples(
            destinatario=email,
            assunto=assunto,
            corpo_html=corpo_html
        )
    
    def enviar_tempkey(
        self,
        email: str,
        login: str,
        tempkey: str
    ) -> bool:
        """
        Envia o tempkey (senha temporária) por email
        
        Args:
            email: Email do usuário
            login: Login do usuário
            tempkey: Código de 4 dígitos
            
        Returns:
            True se enviado com sucesso
        """
        # Separar os 4 dígitos
        digito1, digito2, digito3, digito4 = list(tempkey)
        
        assunto = "🔐 Seu Código de Recuperação de Senha - Eden Map"
        
        corpo_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eden Map - Recuperação de Senha</title>
        </head>

        <body style="margin:0;padding:0;background:#212224;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#212224;padding:40px 20px;">
        <tr>
        <td align="center">

        <table width="600" cellpadding="0" cellspacing="0" style="background:#3A3A3A;border-radius:20px;overflow:hidden;max-width:100%;box-shadow:0 20px 60px rgba(0,0,0,0.5);">

        <tr>
        <td align="center" style="background:#7a3ed427;padding:50px 40px;">
        <img src="https://raw.githubusercontent.com/Dieghonm/Eden-Map/refs/heads/main/assets/Logo2.png" alt="Eden Map Logo" style="max-width:200px;height:auto;display:block;margin-bottom:20px;">
        <h1 style="color:#ffffff;font-size:32px;font-weight:700;margin:0;">Recuperação de Senha 🔐</h1>
        </td>
        </tr>

        <tr>
        <td style="padding:50px 40px;">

        <div style="background:rgba(255,170,46,0.1);border-left:4px solid #ffaa2e;padding:20px;border-radius:8px;margin:0 0 30px 0;">
        <p style="color:#ffaa2e;font-size:15px;line-height:1.6;margin:0;text-align:center;">
        <strong>Se você <span style="color:#ff6b6b;">não solicitou</span> o token, <span style="color:#ff6b6b;">basta ignorar</span> esse email.</strong>
        </p>
        </div>

        <p style="color:#e2e8f0;font-size:18px;line-height:1.8;text-align:center;margin:0 0 30px 0;">
        Olá <strong style="color:#ffffff;font-size:20px;">{login}</strong>,
        </p>

        <p style="color:#cbd5e0;font-size:16px;line-height:1.8;text-align:center;margin:0 0 40px 0;">
        Use o código abaixo para redefinir sua senha:
        </p>

        <div style="background:linear-gradient(-145deg, #1d1e20 0%, #746d7740 38%, #ffffff3b 50%, #746d7740 62%, #1d1e20 100%);border-radius:16px;padding:40px 30px;text-align:center;margin:0 0 30px 0;">
        <p style="color:#94a3b8;font-size:14px;text-transform:uppercase;letter-spacing:1px;margin:0 0 15px 0;">Seu Código</p>

        <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
        <td align="center">
        <table cellpadding="0" cellspacing="0">
        <tr>
        <td style="width:70px;height:90px;background:#d9d9d98c;text-align:center;vertical-align:middle;">
        <span style="color:#ffffff;font-size:48px;font-weight:700;font-family:'Courier New',monospace;">{digito1}</span>
        </td>
        <td style="width:15px;"></td>
        <td style="width:70px;height:90px;background:#d9d9d98c;text-align:center;vertical-align:middle;">
        <span style="color:#ffffff;font-size:48px;font-weight:700;font-family:'Courier New',monospace;">{digito2}</span>
        </td>
        <td style="width:15px;"></td>
        <td style="width:70px;height:90px;background:#d9d9d98c;text-align:center;vertical-align:middle;">
        <span style="color:#ffffff;font-size:48px;font-weight:700;font-family:'Courier New',monospace;">{digito3}</span>
        </td>
        <td style="width:15px;"></td>
        <td style="width:70px;height:90px;background:#d9d9d98c;text-align:center;vertical-align:middle;">
        <span style="color:#ffffff;font-size:48px;font-weight:700;font-family:'Courier New',monospace;">{digito4}</span>
        </td>
        </tr>
        </table>
        </td>
        </tr>
        </table>

        <p style="color:#ff6b6b;font-size:15px;font-weight:600;margin:20px 0 0 0;">⏱️ Expira em 15 minutos</p>
        </div>

        <div style="background:rgba(255,107,107,0.1);border-left:4px solid #ff6b6b;padding:20px;border-radius:8px;margin:0 0 30px 0;">
        <p style="color:#ff6b6b;font-size:15px;line-height:1.6;margin:0;">
        <strong>⚠️ Importante:</strong><br>
        Nunca compartilhe este código com ninguém. A equipe do Eden Map nunca pedirá este código por email ou telefone.
        </p>
        </div>

        <p style="color:#94a3b8;font-size:14px;text-align:center;line-height:1.6;margin:0;">
        Precisa de ajuda?<br>
        Entre em contato: <a href="mailto:duo.estudio.tech@gmail.com" style="color:#8a4aed;text-decoration:none;">duo.estudio.tech@gmail.com</a>
        </p>

        </td>
        </tr>

        <tr>
        <td style="background:rgba(26,29,41,0.8);padding:30px 40px;text-align:center;border-top:1px solid rgba(138,74,237,0.2);">
        <p style="color:#94a3b8;font-size:14px;margin:0 0 10px 0;">
        <strong style="color:#ffffff;">Eden Map</strong>
        </p>
        <p style="color:#64748b;font-size:13px;margin:0 0 10px 0;">
        © 2025 Eden Map. Todos os direitos reservados.
        </p>
        <p style="color:#64748b;font-size:12px;margin:0;line-height:1.6;">
        Este é um email automático, não responda.<br>
        Se você não solicitou esta recuperação, ignore este email.
        </p>
        </td>
        </tr>

        </table>

        </td>
        </tr>
        </table>
        </body>
        </html>
        """

        return self.enviar_email_simples(
            destinatario=email,
            assunto=assunto,
            corpo_html=corpo_html
        )


def get_email_service() -> Optional[BrevoEmailService]:
    """
    Cria uma instância do BrevoEmailService se a API key estiver configurada
    
    Returns:
        BrevoEmailService ou None se não configurado
    """
    api_key = settings.BREVO_API_KEY
    
    if not api_key or api_key == "sua-api-key-aqui":
        logger.warning("⚠️  BREVO_API_KEY não configurada no .env")
        return None
    
    logger.info("✅ Brevo Email Service inicializado")
    logger.debug(f"API Key (primeiros 10 chars): {api_key[:10]}...")
    
    return BrevoEmailService(api_key)


# Função legada para manter compatibilidade
def send_recovery_code_email(to_email: str, user_login: str, recovery_code: str) -> bool:
    """
    Função de compatibilidade - Envia email de recuperação
    
    Args:
        to_email: Email de destino
        user_login: Login do usuário
        recovery_code: Código de 4 dígitos
    
    Returns:
        bool: True se enviado com sucesso
    """
    email_service = get_email_service()
    
    if not email_service:
        logger.warning("=" * 60)
        logger.warning("📧 MODO SIMULAÇÃO - Email não será enviado")
        logger.warning("=" * 60)
        logger.warning("Configure o Brevo para enviar emails reais")
        logger.warning("=" * 60)
        print("\n" + "="*60)
        print("📧 EMAIL SIMULADO (Brevo não configurado)")
        print("="*60)
        print(f"Para: {to_email}")
        print(f"Usuário: {user_login}")
        print(f"Código: {recovery_code}")
        print("="*60 + "\n")
        return True
    
    return email_service.enviar_tempkey(
        email=to_email,
        login=user_login,
        tempkey=recovery_code
    )
