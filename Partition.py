from glob import iglob
from PyNasHelpers import rewrite_attributes, lazy_attributes_compare
__author__ = 'm'


class Partition:
    __doc__ = """

    """

    @staticmethod
    def listall():
        """
        List all available partition handles in the file system
        :return: generator object - list of strings representing unix handles
                 to existing partitions on the machine
        """
        return iglob(r'/dev/sd[a-z][0-9]')

    @staticmethod
    def findpart(
            uuid=None,
            name=None,
            device=None,
            part_number=None,
    ):
        """
        Generator method, locates every existing partition that matches provided
        set of attributes. Call with empty argument list to generate list of all
        available partitions on the machine.
        :param uuid: optional partitions UUID, if not specified, match any UUID
        :param name: optional partitions name, if not specified, match any name
        :param device: optional parent hard drives Disk object, if not specified,
                       match any device
        :param part_number: optional number of the partition of the partition on
                            parent device, if not specified match any
        :return: yield every matched partition
        """

        partition_to_be_found = Partition(
                                            UUID=uuid,
                                            Name=name,
                                            Device=device,
                                            Number=part_number
                                        )

        for partition_handler in Partition.listall():
            partition_found = Partition(partition_handler)
            if partition_found == partition_to_be_found:
                yield partition_found

    __doc__ += ':var _PartitionsAttributes: internal variable used to simplify '\
               'compare and __init__ methods.\n'
    _PartitionsAttributes = frozenset({
                            'UUID', 'Name', 'Device', 'Handler', 'Number',
                            'Size', 'Offset', 'Flags', 'Filesystem'
                            })

    __doc__ += """
    :var UUID: partitions Universally Unique IDentifier, can be None
    :var Name: partitions name, can be None
    :var Device: Disk object representing storage device containing the
                 partition
    :var Handler: path of a unix handler associated with the partition, can
                  None
    :var Number: number of the partition on the storage device, can be None
    :var Size: partitions size in bytes, can be None
    :var offset: offset of the partition on a hard drive, can be None
    :var flags: frozenset containing lowercase strings representing partitions
                flags, can be None
    :var filesystem: lowercase filesystem name, can be None
    """
    UUID = None
    Name = None
    Device = None
    Handler = None
    Number = None
    Size = None
    Offset = None
    Flags = None
    Filesystem = None

    def __init__(
                self,
                UUID=None,
                Name=None,
                Number=None,
                Device=None,
                Size=None,
                Offset=None,
                Flags=None,
                Filesystem=None
                ):
        """
        Construct a Partition object specified by
        :param UUID: optional partitions UUID
        :param Name: optional partitions name
        :param Device: optional parent hard drives Disk object
        :param Number: optional number of the partition of the partition on
                            parent device
        :param Size: not yet supported
        :param Offset: not yet supported
        :param Flags: not yet supported
        :param Filesystem: not yet supported
        :return: not yet supported
        """
        rewrite_attributes(self, self._PartitionsAttributes, locals())

    def __eq__(self, other):
        """
        Compare the instance with other Partition instance. Comparison is based
        on list of specific attributes. If an attribute is set to None, in any
        of the instances, the attribute will not compared
        :param other: Partition class instance to be compared
        :return: False when any of compared attributes in both objects is not
                 None and both objects share the same value of the attribute,
                 otherwise True.
        :raise NotImplemented: when the other object is not instance of the
                               Partition class
        """

        #
        # todo this is not a python way of doing things
        #
        if not isinstance(other, Partition):
            raise NotImplemented

        return lazy_attributes_compare(self, other, self._PartitionsAttributes)


def partition_class_tests():
    empty_part = Partition()
    uuid_part = Partition(UUID="de305d54-75b4-431b-adb2-eb6b9e546014")

    assert empty_part == uuid_part, \
        'comparison of empty partition to any other Partition should always' \
        'match'

    assert uuid_part == empty_part, \
        'comparison of any Partition to an empty Partition should return True' \

    assert empty_part == Partition(), \
        'comparing two empty partitions should always return true'

    return True
