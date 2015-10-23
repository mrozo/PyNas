from Kernel.ConfigParser import config_parser_class_tests, ConfigParser
from Kernel.PyNasHelpers import py_nas_helpers_tests
from Hardware.Partition import partition_class_tests
from Hardware.Disk import disk_class_tests
from Hardware.Hardware import test_hardware_class
try:
    from DevelopmentConfig import NasConf

    print("Loaded DevelopementConf file")
except ImportError:
    from Config import NasConf

    print("Loaded Conf file")

__author__ = 'm'


def py_nas_tests():
    try:
        try:
            config = ConfigParser(NasConf)
        except Exception as E:
            assert False, 'Failed to parse NasConfig\n' + str(E)

        assert partition_class_tests(), 'Partition class tests have failed.'
        assert disk_class_tests(), 'Disk class tests have failed.'
        assert config_parser_class_tests(), 'Config parser tests have failed'
        assert test_hardware_class(), "Hardware class test have failed"
        assert py_nas_helpers_tests(), "PyNasHelpers tests have failed"

        # todo parted tests
        # todo hdparm tests
    except Exception as E:
        assert False, E.__str__()


py_nas_tests()
