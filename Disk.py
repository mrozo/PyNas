from glob import iglob

from HdParm import HdParm
from Parted import PartedWrapper
from Partition import Partition
from PyNasHelpers import rewrite_attributes, lazy_attributes_compare

__author__ = 'm'


class Disk:
    __doc__ = """

    """

    __doc__ += ":var _DiskAttributes: internal helper variable used mainly to" \
               "simplify object initialization and lazy compare method."
    _DiskAttributes = ['Type', 'SerialNumber', 'DeviceHandle', 'Name',
                       'Partitions']

    __doc__ += """
    :var Type: type of the drive, can be None.
    :var SerialNumber: string containing hard drives serial number, can be None.
    :var DeviceHandle: string containing linux path of the devices handle in the
                       filesystem, can be None.
    :var Partitions: list containing Partition objects representing drives
                     partition table.
    """
    Type = None
    SerialNumber = None
    DeviceHandle = None
    HdParm = None
    Partitions = None
    Name = None

    @staticmethod
    def list_all_handles():
        """
        List all available storage devices handles existing in the file system.
        :return: generator object.
        """
        return iglob("/dev/sd[a-z]")

    @staticmethod
    def disk_factory():
        for disk in Disk.list_all_handles():
            yield Disk(disk)

    def __init__(
                    self,
                    DeviceHandle=None,
                    SerialNumber=None,
                    Partitions=None,
                    Name=None
                ):
        if DeviceHandle is not None:
            self.construct_from_handle(DeviceHandle)
        else:
            rewrite_attributes(self, self._DiskAttributes, locals())

    def construct_from_handle(self, device_handle) -> None:
        """
        Initialize the using gathered data about existing, physical storage
        device specified by device_handle.
        :param device_handle: unix device handle, in most cases looks like
        r"/dev/sdX".
        """
        self.DeviceHandle = device_handle
        self.HdParm = HdParm(self.DeviceHandle)
        self.SerialNumber = self.HdParm.SerialNumber
        parted_info = PartedWrapper.get_disk_info(self.DeviceHandle)

        partitions_list = []
        for partition in parted_info['Partitions']:
            partitions_list.append(
                Partition(
                    Number=partition['Number'],
                    Offset=partition['Start'],
                    Size=partition['Size'],
                    Flags=partition['Flags']
                )
            )

        self.Partitions = partitions_list

    def __eq__(self, other):
        # todo not a pythons way of doing things
        if not isinstance(other, Disk):
            raise NotImplemented

        return lazy_attributes_compare(self, other, self._DiskAttributes)

    def __repr__(self):
        return "<StorageDevice " + str(self.DeviceHandle) + ", SN: " + \
               str(self.SerialNumber) + ">"

    def __str__(self):
        return repr(self)


def disk_class_tests():
    empty_disk = Disk()
    disk_from_handle = Disk(r'/dev/sda')
    disk_from_data = Disk(
        SerialNumber='12345678abcd',
        Name='hd1'
    )

    assert empty_disk == disk_from_handle,\
        'comparison with an empty disk should match any hard drive.'
    assert empty_disk == disk_from_data,\
        'comparison with an empty disk should match any hard drive.'
    assert disk_from_data != disk_from_handle,\
        'comparison of real disk with a fake one should return false.'
    return True
