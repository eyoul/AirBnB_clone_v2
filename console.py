#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from shlex import split
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <Class name> <param 1> <param 2> <param 3>...
        Display the string representation of a class instance of a given id.
        """
        try:
            if not arg:
                raise SyntaxError()
            my_list = arg.split(" ")

        kwargs = {}
        for i in range(1, len(my_list)):
            key, param = tuple(my_list[i].split("="))
            if param[0] == '"':
                param = param.split('"').replace("_", " ")
            else:
                try:
                    param = eval(param)
                except (SyntaxError, NameError):
                    continue
            kwargs[key] = param
        if kwargs == {}:
            obj =eval(my_list[0])()
        else:
            obj = eval(my_list[0])(**kwargs)
            storage.new(obj)
        print(obj.id)
        obj.save()

    except SyntaxError:
        print("** class name missing **")
    except NameError:
        print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not arg:
                raise SyntaxError()
            my_list = arg.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '-' +my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
    except SyntaxError:
        print("** class Name missing **")
    except NameError:
        print("** Class doesn't exist **")
    except IndexError:
        print("** Instance id missing **")
    except KeyError:
        print("** No Instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not arg:
                raise SyntaxError()
            my_list = arg.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
    except SyntaxError:
        print("** Class Name missing **")
    except NameError:
        print("** Class doesn't exist **")
    except IndexError:
        print("** Instance id missing **")
    except KeyError:
        print("** No Instance found **")

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        if not arg:
        o = storage.all()
        print([o[k].__str__() for k in o])
        return
    try:
        args = arg.split(" ")
        if args[0] not in self.__classes:
            raise NameError()

        o = storage.all(eval(srgs[0]))
        print([o[k].__str__() for k in o])
    except NameError:
        print("*** Class doesn't exist **")

    def do_update(self, arg):
        """Updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        """
        try:
            if not arg:
                raise SyntaxError()
            my_list = split(arg, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                v.__dict__[my_list[2]] = my_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** Instance id missing **")
        except KeyError:
            print("** No Instance found **")
        except AttributeError:
            print("** Attribute name missing **")
        except ValueError:
            print("** Value missing **")

    def do_count(self, arg):
         """count the number of instances of a class
        """
        counter = 0
        try:
            my_list = split(arg, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        new_arg = []
        new_arg.append(args[0])
        try:
            my_dict = eval(args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_arg.append(((new_str.split(", "))[0]).strip('"'))
            new_arg.append(my_dict)
            return new_arg
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_arg.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_arg)

    def default(self, arg):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        my_list = arg.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, arg)

if __name__ == "__main__":
    HBNBCommand().cmdloop()
