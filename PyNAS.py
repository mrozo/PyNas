try:
    from DevelopmentConfig import NasConf
    print("Loaded DevelopementConf file")
except ImportError:
    from Config import NasConf
    print("Loaded Conf file")

from ConfigParser import ConfigParser
from Partition import partition_class_tests
from Disk import disk_class_tests

__author__ = 'm'


# todo .gitignore
# todo learn a proper unit tests
def py_nas_tests():
    try:
        ConfigParser(NasConf)
    except Exception as E:
        assert False, 'Failed to parse NasConfig\n' + str(E)

    assert partition_class_tests(), 'Partition class tests have failed.'
    assert disk_class_tests(), 'Disk class tests have failed.'

    # todo parted tests
    # todo hdparm tests

py_nas_tests()

# todo blkid wrapper
