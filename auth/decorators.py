from functools import wraps

from flask_jwt_extended import get_current_user

def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = get_current_user()
            print("user", user)
            print("user object", user.__dict__)
            if not user.has_role(role):
                return {"message": "You do not have permission to access this resource"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper