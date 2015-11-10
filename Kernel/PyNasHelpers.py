from copy import copy
__author__ = 'm'


def rewrite_attributes(self, attribute_names, variables, skip_none=True):
    """
    Rewrite variables specified in attributes list to the object
    :param self: object to rewrite the values to
    :param attribute_names: list of attributes names acceptable by the object
    :param variables: dictionary containing attribute values
    :param skip_none: when true, method will not copy attribute when its None
    """
    for attribute, value in variables.items():
        value = variables[attribute]

        if attribute in attribute_names:

            if skip_none and value is None:
                continue

            setattr(self, attribute, value)


def lazy_attributes_compare(self, other, attribute_names, skip_none=True):
    """
    Compare the other object to the self object by testing for equality
    attributes specified in attributes_names list
    :param self: left object to compare
    :param other: right object to compare
    :param attribute_names: list of significant attributes names
    :param skip_none: skip comparison of attributes that value is None in any of
                      the objects
    :return: True if no significant difference has been found, otherwise False
    """
    for attribute in attribute_names:

        self_attribute = getattr(self, attribute, None)
        other_attribute = getattr(other, attribute, None)

        if skip_none and (self_attribute is None or other_attribute is None):
            continue
        if self_attribute != other_attribute:
            return False

    return True


def compare_lists(listA, listB):
    """
    Compare tow lists and return differences.
    :param listA:
    :param listB:
    :return: three lists common, added_in_b, removed_in_b, representing
             found differences
    """
    A = copy(listA)
    B = copy(listB)

    common = []
    added_in_b = []
    removed_in_b = []

    for diskA in A:
        for diskB in B:
            if diskA == diskB:
                common.append(diskA)
                B.remove(diskB)
                break
        else:
            removed_in_b.append(diskA)
            A.remove(diskA)
            break

    if len(B):
        added_in_b = B

    return common, added_in_b, removed_in_b


def py_nas_helpers_tests():
    class EmptyClass:
        pass


    #
    # rewrite_attributes tests
    #

    #
    # test 1: basics
    #
    attribute_names = ['a', 'b', 'c']
    attributes = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    obj = EmptyClass()
    rewrite_attributes(obj, attribute_names, attributes)
    for attribute_name in attribute_names:
        assert hasattr(obj,attribute_name),\
            "Method rewrite_attributes didn't create an attribute '" + \
            str(attribute_name) + "'"
        assert getattr(obj, attribute_name) == attributes[attribute_name],\
            "Method rewrite_attributes didn't copy an attribute value '" + \
            str(attribute_name) + "'"

    rewrite_attributes(obj, ['empty_attribute'], {'empty_attribute': None})

    #
    # test 2: skip_none tests
    #
    assert not hasattr(obj, 'empty_attribute'), \
        "by default rewrite_attributes should not copy attribute, when its " \
        "value is None"

    rewrite_attributes(
            obj,
            ['empty_attribute'],
            {'empty_attribute': None},
            skip_none=False
        )

    assert hasattr(obj, 'empty_attribute'), \
        "when skip_none argument is set to False, rewrite_attributes should "\
        "copy even attributes with value set to None"

    #
    # lazy compare tests
    #
    obj = EmptyClass()
    obj.a = 1
    obj.b = 2
    obj.c = 3
    obj.empty_attr = None
    attribute_names = ['a', 'b']
    obj1 = EmptyClass()
    obj1.a = 1
    obj1.b = 2

    assert lazy_attributes_compare(obj, obj1, attribute_names),\
        "lazy_attributes_compare has failed the city"

    attribute_names = ['a', 'b', 'c']
    assert not lazy_attributes_compare(
        obj, obj1, attribute_names, skip_none=False
    ), \
        "If any of the attributes is missing in any of the objects and " \
        "skip_none is False, the method should return false"
    assert lazy_attributes_compare(
        obj, obj1, attribute_names, skip_none=True
    ), \
        "If any of the attributes is missing in any of the objects and " \
        "skip_none is True, the method should treat them as if they were equal"\
        " to None."

    #
    # compare lists tests
    #

    return True
