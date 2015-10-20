from Disk import Disk
__author__ = 'm'

#
# todo listowanie dysków
#

#
# todo pobieranie ramu
#

#
# todo pobieranie stanu cpu
#

#
# todo metoda zwracająca różnicę między dwiema konfiguracjami (np między starą, a nową)
#

class Hardware:
    __doc__ = """
A base class representing hardware configuration. This is not an approach to
create a class representing every device in the system.

:var Ram:
:var Storage:
"var
"""
    Ram = None
    Storage = None
    Cpu = None
    Network = None

    def __init__(self):
        self.refresh()
        pass

    def refresh(self):
        """
        Rediscover currently installed hardware
        """
        self.Storage = list(Disk.disk_factory())
        pass


def test_hardware_class():
    assert Hardware(), "General initialization error"

    return True
