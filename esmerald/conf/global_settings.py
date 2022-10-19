from typing import (
    TYPE_CHECKING,
    Any,
    AsyncContextManager,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)

from pydantic import BaseSettings

from esmerald import __version__
from esmerald.conf.enums import EnvironmentType
from esmerald.config import (
    CORSConfig,
    CSRFConfig,
    OpenAPIConfig,
    SessionConfig,
    StaticFilesConfig,
    TemplateConfig,
)
from esmerald.config.asyncexit import AsyncExitConfig
from esmerald.permissions.types import Permission
from esmerald.schedulers import AsyncIOScheduler
from esmerald.types import (
    APIGateHandler,
    Dependencies,
    ExceptionHandlers,
    LifeSpanHandler,
    Middleware,
    ResponseCookies,
    ResponseHeaders,
    ResponseType,
    SchedulerType,
)

if TYPE_CHECKING:
    from esmerald.applications import Esmerald


class EsmeraldAPISettings(BaseSettings):
    debug: bool = False
    environment: Optional[str] = EnvironmentType.PRODUCTION
    app_name: str = "Esmerald"
    title: str = "My awesome Esmerald application"
    description: str = "Highly scalable, performant, easy to learn and for every application."
    contact: Optional[Dict[str, Union[str, Any]]] = {
        "name": "admin",
        "email": "admin@myapp.com",
    }
    terms_of_service: Optional[str] = None
    license_info: Optional[Dict[str, Union[str, Any]]] = None
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None
    openapi_path: Optional[str] = "docs"
    secret: str = "my secret"
    version: str = __version__
    allowed_hosts: Optional[List[str]] = ["*"]
    allow_origins: Optional[List[str]] = None
    response_class: Optional[ResponseType] = None
    response_cookies: Optional[ResponseCookies] = None
    response_headers: Optional[ResponseHeaders] = None
    scheduler_class: SchedulerType = AsyncIOScheduler
    include_in_schema: bool = True
    tags: Optional[List[str]] = None
    timezone: str = "UTC"
    use_tz: bool = False
    root_path: Optional[str] = ""
    enable_sync_handlers: bool = True
    enable_scheduler: bool = False

    @property
    def reload(self) -> bool:
        """
        Returns reloading for dev and test environments.
        """
        if self.environment in [EnvironmentType.DEVELOPMENT, EnvironmentType.TESTING]:
            return True
        return False

    @property
    def password_hashers(self) -> List[str]:
        return [
            "esmerald.contrib.auth.hashers.PBKDF2PasswordHasher",
            "esmerald.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        ]

    @property
    def routes(self) -> List[APIGateHandler]:
        """
        Property that can be used as an entrypoint for the base app routes and to start the application.

        Example:
            from esmerald import Include

            class MySettings(EsmeraldAPISettings):
                @property
                def routes(self):
                    return Include(path='/api/v1/', namespace='myapp.routes')
        """
        return []

    @property
    def csrf_config(self) -> CSRFConfig:
        """
        Initial Default configuration for the CSRF.
        This can be overwritten in another setting or simply override `secret` or then override
        the `def csrf_config()` property to change the behavior of the whole csrf_config.

        Default:
            None

        Example:

            class MySettings(EsmeraldAPISettings):
                secret: str = "n(0t=%_amauq1m&6sde4z#3mkdmfcad1942ny&#sjp1oygk-5_"

                @property
                def csrf_config(self) -> CSRFConfig:
                    if not self.secret:
                        raise ImproperlyConfigured("`secret` setting not configured.")
                    return CSRFConfig(secret=self.secret)
        """
        return None

    @property
    def async_exit_config(self) -> AsyncExitConfig:
        """
        Initial Default configuration for the CSRF.
        This can be overwritten in another setting or simply override `secret` or then override
        the `def async_exit_config()` property to change the behavior of the whole async_exit_config.

        This replaces the classic:
        `async_exit_config: Optional[AsyncExitConfig] = None`.

        Default:
            AsyncExitConfig

        Example:

            class MySettings(EsmeraldAPISettings):
                @property
                def async_exit_config(self) -> AsyncExitConfig:
                    ...
        """
        return AsyncExitConfig()

    @property
    def template_config(self) -> TemplateConfig:
        """
        Initial Default configuration for the TemplateConfig.
        This can be overwritten in another setting or simply override `template_config` or then override
        the `def template_config()` property to change the behavior of the whole template_config.

        Esmerald can also support other engines like mako, Diazo, Cheetah. Currently natively
        only supports jinja2 and mako.

        Default:
            JinjaTemplateEngine

        Example:

            class MySettings(EsmeraldAPISettings):
                @property
                def template_config(self) -> TemplateConfig:
                    TemplateConfig(directory='templates', engine=MakoTemplateEngine)
        """
        return None

    @property
    def static_files_config(self) -> StaticFilesConfig:
        """
        Simple configuration indicating where the statics will be placed in
        the application.

        Default:
            None

        Example:

            class MySettings(EsmeraldAPISettings):
                @property
                def static_files_config(self) -> StaticFilesConfig:
                    StaticFilesConfig(path='/', directories=...)
        """
        return None

    @property
    def cors_config(self) -> CORSConfig:
        """
        Initial Default configuration for the CORS.
        This can be overwritten in another setting or simply override `allow_origins` or then override
        the `def cors_config()` property to change the behavior of the whole cors_config.

        Default:
            CORSConfig

        Example:

            class MySettings(EsmeraldAPISettings):
                allow_origins: List[str] = ['www.example.com', 'www.foobar.com']

                @property
                def cors_config(self) -> CORSConfig:
                    ...
        """
        if not self.allow_origins:
            return None
        return CORSConfig(allow_origins=self.allow_origins)

    @property
    def session_config(self) -> SessionConfig:
        """
        Initial Default configuration for the SessionConfig.
        This can be overwritten in another setting or simply override `session_config` or then override
        the `def session_config()` property to change the behavior of the whole session_config.

        Default:
            None

        Example:

            class MySettings(EsmeraldAPISettings):
                @property
                def session_config(self) -> SessionConfig:
                    SessionConfig(engine=MakoTemplateEngine)
        """
        return None

    @property
    def openapi_config(self) -> OpenAPIConfig:
        """
        Initial Default configuration for the CORS.
        This can be overwritten in another setting or simply override `allow_origins` or then override
        the `def openapi_config()` property to change the behavior of the whole cors_config.

        Default:
            OpenAPIConfig

        Example:

            class MySettings(EsmeraldAPISettings):

                @property
                def openapi_config(self) -> CORSConfig:
                    ...
        """
        return OpenAPIConfig(
            path=self.openapi_path,
            title=self.title,
            contact=self.contact,
            version=self.version,
            terms_of_service=self.terms_of_service,
            license=self.license_info,
            servers=self.servers,
            app_name=self.app_name,
        )

    @property
    def middleware(self) -> List[Middleware]:
        """
        Initial Default configuration for the middleware.
        This can be overwritten in another setting or simply override `def middleware()`.

        Example:

            class MySettings(EsmeraldAPISettings):

                @property
                def middleware(self) -> List[Middleware]:
                    return [EsmeraldMiddleware]
        """
        return None

    @property
    def scheduler_tasks(self) -> Dict[str, str]:
        """Returns a list of tasks for run with `scheduler_class`.

        Where the tasks are placed is not linked to the name of
        the file itself. They can be anywhere. What is imoprtant
        is that in the dictionary the name of the task and the
        location of the file where the task is.

        Returns:
            Dict[str, str]: A list of tasks.

        Example:

            class MySettings(EsmeraldAPISettings):

                @property
                def scheduler_tasks(self) -> Dict[str, str]:
                    tasks = {
                        "send_newslettters": "accounts.tasks",
                        "check_balances": "finances.balance_tasks",
                    }

        """

        return {}

    @property
    def permissions(self) -> List[Permission]:
        """
        Returns the default permissions of Esmerald.
        """
        return None

    @property
    def dependencies(self) -> Dependencies:
        """
        Returns the dependencies of Esmerald main app.
        """
        return None

    @property
    def exception_handlers(self) -> ExceptionHandlers:
        """
        Default exception handlers to be loaded when the application starts
        """
        return None

    @property
    def on_startup(self) -> List[LifeSpanHandler]:
        """
        List of events/actions to be done on_startup.
        """
        return None

    @property
    def on_shutdown(self) -> List[LifeSpanHandler]:
        """
        List of events/actions to be done on_shutdown.
        """
        return None

    @property
    def lifespan(self) -> Callable[["Esmerald"], AsyncContextManager]:
        """
        Custom lifespan that can be passed instead of the default Starlette.

        The lifespan context function is a newer style that replaces
        on_startup / on_shutdown handlers. Use one or the other, not both.
        """
        return None
