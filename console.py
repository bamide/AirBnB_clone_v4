#!/usr/bin/python3
"""command interpreter"""
import cmd
import models
import re
import sys
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage

classes = {
    "BaseModel": BaseModel, "User": User,
    "Place": Place, "State": State,
    "City": City, "Amenity": Amenity,
    "Review": Review,
}
# TODO: add comments under every class and function and before imports


class HBNBCommand(cmd.Cmd):
    """ console class """
    prompt = '(hbnb) '

    def precmd(self, line):
        # Check if the app is running non-interactively
        if not sys.stdin.isatty():
            print()
            return line

        # Use regex to parse the input line
        checks = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if checks:
            class_name, command, args = checks.groups()

            if args is None:
                line = f"{command} {class_name}"
            else:
                args_checks = re.search(r"^\"([^\"]*)\"(?:, (.*))?$", args)
                if args_checks:
                    instance_id, attribute_part = args_checks.groups()
                    if attribute_part:
                        line = (
                            f"{command} "
                            f"{class_name} "
                            f"{instance_id} "
                            f"{attribute_part}"
                        )
                    else:
                        line = f"{command} {class_name} {instance_id}"

        return super().precmd(line)

    def default(self, arg):
        """Default behavior on invalid input"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        match = re.match(r'(\w+)\((.*?)\)', arg)
        if match:
            command, params = match.groups()
            if command in argdict:
                return argdict[command](params)

        print(f"*** Unknown syntax: {arg}")
        return False

    def parse_arg(arg):
        """Handles user input and returns tokens as a list."""
        tokens = re.split(r',|(\[.*?\])|(\{.*?\})', arg)
        return [token.strip(',') for token in tokens if token]

    def do_count(self, arg):
        """Retrieve the number of instances of a given class."""
        _arg = parse_arg(arg)
        cnt = 0
        for obj in storage.all().values():
            if _arg[0] == obj.__class__.__name__:
                cnt += 1
        print(cnt)

    def do_update(self, args):
        """Update instance based on relevant args"""
        _args = args.split()

        if not _args:
            print("** class name missing **")
            return

        class_name = _args[0]

        if class_name not in classes:
            print("** class doesn't exist **")
            return

        if len(_args) < 2:
            print("** instance id missing **")
            return

        instance_id = class_name + "." + _args[1]
        instances = models.storage.all()

        if instance_id not in instances:
            print("** no instance found **")
            return

        if len(_args) < 3:
            print("** attribute name missing **")
            return

        attribute_name = _args[2]

        if len(_args) < 4:
            print("** value missing **")
            return

        new_value = _args[3]

        setattr(instances[instance_id], attribute_name, new_value)
        instances[instance_id].save()

    def do_destroy(self, args):
        """Deletes instance based on class and id"""
        _args = args.split()

        if not _args:
            print("** class name missing **")
            return

        class_name = _args[0]

        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(_args) < 2:
            print("** instance id missing **")
            return

        instance_id = class_name + "." + _args[1]

        instances = models.storage.all()
        if instance_id in instances:
            instances[instance_id].delete()
            models.storage.save()
        else:
            print("** no instance found **")

    def do_show(self, args):
        """Prints instance as string based on the class and id"""
        _args = args.split()

        if not _args:
            print("** class name missing **")
            return

        class_name = _args[0]

        if class_name not in classes:
            print("** class doesn't exist **")
            return

        if len(_args) < 2:
            print("** instance id missing **")
            return

        instance_id = "{}.{}".format(class_name, _args[1])

        all_objects = models.storage.all()
        if instance_id in all_objects:
            obj = all_objects[instance_id]
            print(obj.to_dict())
        else:
            print("** no instance found **")

    def do_create(self, args):
        """Creates a new instance of a class with given parameters."""
        _args = re.split(r'\s(?=\w+=)', args)
        if len(_args) == 0:
            print("** class name missing **")
            return False
        elif _args[0] in classes:
            new_dict = {}
            for arg in _args[1:]:
                key_value = arg.split('=')
                if len(key_value) == 2:
                    key, value = key_value
                    if value[0] == '"' and value[-1] == '"':
                        value = value[1:-1].replace('_', ' ')
                        value = value.replace('\\"', '"')
                    elif '.' in value:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            continue
                    new_dict[key] = value
            instance = classes[_args[0]](**new_dict)
            print(instance.id)
            instance.save()
        else:
            print("** class doesn't exist **")
            return False


    def my_filter(self, objects, class_name):
        filtered_objects = filter(
            lambda item: isinstance(item[1], classes[class_name]),
            objects.items()
        )
        return dict(filtered_objects)


    def do_all(self, args):
        """Prints string representation of instances"""
        _args = args.split()

        if not _args:
            objects = models.storage.all()
        elif _args[0] in classes:
            class_name = _args[0]
            cls = classes[class_name]
            if hasattr(cls, 'all') and callable(getattr(cls, 'all')):
                objects = cls.all()
            else:
                objects = models.storage.all().values()
                objects = [obj for obj in objects if isinstance(obj, cls)]
        else:
            print("** class doesn't exist **")
            return False

        print("[", end="")
        print(", ".join(str(obj) for obj in objects), end="")
        print("]")


    def _parse_dict(self, args):
        """creates dictionary from list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                value = value.strip('"').replace('_', ' ')
                value = value.replace('\\"', '"')
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except (ValueError, TypeError):
                    pass
                new_dict[key] = value
        return new_dict

    def do_EOF(self, args):
        """ exits console """
        return True

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """ override cmd emptyline method """
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
