from copy import copy
import json

class Reporter(object):
    """
    The goal of this class is to have an object with dot acccess that can
    keep track of data that happens during a program's execution.

    Additionally it should be able to reset itself to the original template
    and serialize itself

    This class is principally used with hawk_eye_notify so it abides by the
    {source, output} convention used by the templating there.
    """

    def __init__(self, source, output_dict, no_reset=[]):
        """
        The output_dict is what will generate the template and be serialized
        as well as being dot accessible from the runtime Reporter instance

        The no reset keys are there to stop the reset function
        from deleting data in particular keys on the report object
        """
        self.__template = {}
        self.__source = source
        self.__no_reset = no_reset
        for key, value in output_dict.items():
            self.add_key_value(key, value)

    def serialize(self, sort_keys=True, indent=4):
        """
        Serializes the report for writing to a file.

        It should only serialize things that were defined in the template
        """
        acc = {
            'source': self.__source,
            'output': {}
        }
        for key in self.__template.keys():
            acc['output'][key] = getattr(self, key)
        return json.dumps(copy(acc), sort_keys=sort_keys, indent=indent)

    def add_key_value(self, key, value):
        """
        Builds the __template one key value at a time.

        This will copy every key value pair so that changes that happen
        in the reporter and different instances from the same template
        will not affect one another
        """
        key_copy = copy(key)
        value_copy = copy(value)
        self.__template[key_copy] = value_copy
        setattr(self, key_copy, value_copy)
        return self

    def get_template(self):
        return copy(self.__template)

    def reset(self, force=False):
        """
        For every key in the template, this function should set them back to their
        initial state unless the key was in the no_reset list passed at init.

        If force is passed this function will ignore the no_reset list
        """
        for key in self.__template.keys():
            if force:
                setattr(self, key, self.__template.get(key))
            elif key in self.__no_reset:
                pass
            else:
                setattr(self, key, self.__template.get(key))
        return self

