from urllib.parse import urlparse
from pydantic import Field
from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    """Configuración de variables de entorno para Django."""

    # Configuración básica de Django
    debug: bool = True
    secret_key: str = "4_53vwpxo#7t6@ld@#5xefg^f6_liq7lxwu4g9wb7+=g"
    allowed_hosts: str = "localhost,127.0.0.1"
    redis_url: str = "redis://localhost:6379"

    # Base de datos PostgreSQL
    database_url: str = Field("postgres://postgres:postgres@localhost:5432/postgres")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    @property
    def allowed_hosts_list(self) -> list[str]:
        """Convierte ALLOWED_HOSTS string en lista."""
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    @property
    def database_name(self) -> str:
        """Extrae el nombre de la base de datos de la URL."""
        parsed = urlparse(self.database_url)
        return parsed.path[1:]  # Remove leading slash

    @property
    def database_user(self) -> str:
        """Extrae el usuario de la base de datos de la URL."""
        parsed = urlparse(self.database_url)
        return parsed.username

    @property
    def database_password(self) -> str:
        """Extrae la contraseña de la base de datos de la URL."""
        parsed = urlparse(self.database_url)
        return parsed.password

    @property
    def database_host(self) -> str:
        """Extrae el host de la base de datos de la URL."""
        parsed = urlparse(self.database_url)
        return parsed.hostname

    @property
    def database_port(self) -> int:
        """Extrae el puerto de la base de datos de la URL."""
        parsed = urlparse(self.database_url)
        return parsed.port

    @property
    def redis_host(self) -> str:
        """Extrae el host de Redis de la URL."""
        parsed = urlparse(self.redis_url)
        return parsed.hostname

    @property
    def redis_port(self) -> int:
        """Extrae el puerto de Redis de la URL."""
        parsed = urlparse(self.redis_url)
        return parsed.port

    # Stripe Configuration
    stripe_publishable_key: str = Field(default="", env="STRIPE_PUBLISHABLE_KEY")
    stripe_secret_key: str = Field(default="", env="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str = Field(default="", env="STRIPE_WEBHOOK_SECRET")

    # PayPal Configuration
    paypal_client_id: str = Field(default="", env="PAYPAL_CLIENT_ID")
    paypal_client_secret: str = Field(default="", env="PAYPAL_CLIENT_SECRET")
    paypal_sandbox: bool = Field(default=True, env="PAYPAL_SANDBOX")

    # Frontend URL for redirects
    frontend_url: str = Field(default="http://localhost:3000", env="FRONTEND_URL")

    # Cloudinary Configuration
    cloudinary_cloud_name: str = Field(default="", env="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(default="", env="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(default="", env="CLOUDINARY_API_SECRET")

    # Firebase Configuration
    firebase_type: str = Field(default="service_account", env="FIREBASE_TYPE")
    firebase_project_id: str = Field(default="", env="FIREBASE_PROJECT_ID")
    firebase_private_key_id: str = Field(default="", env="FIREBASE_PRIVATE_KEY_ID")
    firebase_private_key: str = Field(default="", env="FIREBASE_PRIVATE_KEY")
    firebase_client_email: str = Field(default="", env="FIREBASE_CLIENT_EMAIL")
    firebase_client_id: str = Field(default="", env="FIREBASE_CLIENT_ID")
    firebase_auth_uri: str = Field(
        default="https://accounts.google.com/o/oauth2/auth", env="FIREBASE_AUTH_URI"
    )
    firebase_token_uri: str = Field(
        default="https://oauth2.googleapis.com/token", env="FIREBASE_TOKEN_URI"
    )
    firebase_auth_provider_x509_cert_url: str = Field(
        default="https://www.googleapis.com/oauth2/v1/certs",
        env="FIREBASE_AUTH_PROVIDER_X509_CERT_URL",
    )
    firebase_client_x509_cert_url: str = Field(
        default="", env="FIREBASE_CLIENT_X509_CERT_URL"
    )
    firebase_universe_domain: str = Field(
        default="googleapis.com", env="FIREBASE_UNIVERSE_DOMAIN"
    )
