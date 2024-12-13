from care.emr.resources.base import EMRResource
from care.users.models import User


class UserSpec(EMRResource):
    __model__ = User
    id: int
    first_name: str
    username: str
    email: str
    last_name: str
    user_type: str
    last_login: str
    read_profile_picture_url: str
