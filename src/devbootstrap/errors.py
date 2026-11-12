"""Domain exceptions raised by DevBootstrap."""


class DevBootstrapError(Exception):
    """Base exception for expected DevBootstrap errors."""


class InvalidServiceNameError(DevBootstrapError):
    """Raised when a service name is not a valid project directory name."""


class DestinationExistsError(DevBootstrapError):
    """Raised when generation would overwrite an existing destination."""


class TemplateNotFoundError(DevBootstrapError):
    """Raised when the requested template is unavailable."""


class ProjectPathError(DevBootstrapError):
    """Raised when a project path cannot be validated."""
