# 1.导包
from django.conf import settings
from django.core.files.storage import Storage


# 2.继承类
class FastDFSStorage(Storage):
    def __init__(self):
        self.base_url = settings.FDFS_BASE_URL

    # 3._open
    def _open(self, name, mode='rb'):
        pass

    # 4._save
    def _save(self, name, content, max_length=None):
        pass

    # 5. url
    def url(self, name):
        # http://192.168.90.172:8888/ ---我们自己添加
        # group1/M00/00/00/CtM3BVnifxeAPTodAAPWWMjR7sE487.jpg == name
        return self.base_url + name
