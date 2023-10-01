#!/usr/bin/env python
"""
Generated by 'esmerald createproject'
"""
import os
import sys
from pathlib import Path

from starlette.middleware import Middleware as StarletteMiddleware

from esmerald import Esmerald, Gateway, Include
from esmerald.conf import settings
from esmerald.contrib.auth.mongoz.middleware import JWTAuthMiddleware


def build_path():
    """
    Builds the path of the project and project root.
    """
    Path(__file__).resolve().parent.parent
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

    if SITE_ROOT not in sys.path:
        sys.path.append(SITE_ROOT)
        sys.path.append(os.path.join(SITE_ROOT, "apps"))


def get_application():
    """
    This is optional. The function is only used for organisation purposes.
    """
    build_path()
    from accounts.models import User
    from accounts.views import create_user, home, login

    app = Esmerald(
        routes=[
            Gateway("/login", handler=login),
            Gateway("/create", handler=create_user),
            Include(
                routes=[Gateway(handler=home)],
                middleware=[
                    StarletteMiddleware(
                        JWTAuthMiddleware, config=settings.jwt_config, user_model=User
                    )
                ],
            ),
        ],
    )
    return app


app = get_application()
