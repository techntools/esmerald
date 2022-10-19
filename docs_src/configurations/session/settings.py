from esmerald import EsmeraldAPISettings, ImproperlyConfigured, SessionConfig


class CustomSettings(EsmeraldAPISettings):
    @property
    def session_config(self) -> SessionConfig:
        """
        Initial Default configuration for the SessionConfig.
        This can be overwritten in another setting or simply override
        `session_config` or then override the `def session_config()`
        property to change the behavior of the whole session_config.
        """
        if not self.secret:
            raise ImproperlyConfigured("`secret` setting not configured.")
        return SessionConfig(
            secret_key=self.secret,
            session_cookie="session",
        )
