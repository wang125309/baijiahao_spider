from portal.cache.cache import *
from portal.models import *


@singleton
class UserCache(BaseCache):
    def get_cache_obj(self, key):
        u = User.objects.filter(user_id=key)
        if len(u) == 1:
            value = u[0]
            return {
                "user_id":value.user_id,
                "name":value.name,
                "mobile":value.mobile,
                "age":value.age,
                "id_card":value.id_card,
                "real_name":value.real_name,
                "id":value.id,
                "email":value.email,
                "sex":value.sex
            }
        else:
            return {}

    def __init__(self):
        self.init(USER_CACHE_NAME, USER_CACHE_SIZE)
        return


user_cache = UserCache()
