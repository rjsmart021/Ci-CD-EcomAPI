from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = limiter(key_func=get_remote_address)
        class Limiter(
                key_func: () -> str,
                *,
                app: Flask | None = None,
                default_limits: List[str | (() -> str) ] | None = None,
                default_limits_per_method: bool | None = None,
                default_limits_exempt_when: (() -> bool) | None = None,
                default_limits_deduct_when:((Response) -> bool) | None = None,
                default_limits_cost: int | (() -> int) | None = None,
                application_limits: List[str | (()  -> str)] | None =None,
                application_limits_per_method: bool | None = None,
                application_limits_exempt_when: (() -> bool) | None = None,
                application_limits deduct when: ((Response) -> bool) | None = None)
