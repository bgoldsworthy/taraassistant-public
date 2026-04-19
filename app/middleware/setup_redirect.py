"""Middleware to redirect to setup wizard if not configured."""
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.setup.storage import ConfigStorage


class SetupRedirectMiddleware(BaseHTTPMiddleware):
    """Redirect to setup wizard if configuration is missing."""

    # Paths that don't require configuration
    EXEMPT_PATHS = {
        "/setup",
        "/settings",
        "/health",
    }

    EXEMPT_PREFIXES = (
        "/api/setup/",
    )

    async def dispatch(self, request: Request, call_next):
        """Process request, redirecting to setup if not configured."""
        path = request.url.path

        # Allow exempt paths through
        if path in self.EXEMPT_PATHS:
            return await call_next(request)

        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return await call_next(request)

        # Check if configured
        from app.config import is_configured
        if not is_configured():
            ingress_path = request.headers.get("X-Ingress-Path", "")
            # For API requests, return JSON error
            if path.startswith("/api/"):
                return JSONResponse(
                    status_code=503,
                    content={
                        "error": "Application not configured",
                        "message": "Please complete the setup wizard first.",
                        "setup_url": f"{ingress_path}/setup"
                    }
                )
            # For HTML requests, redirect to setup
            return RedirectResponse(url=f"{ingress_path}/setup", status_code=307)

        return await call_next(request)
