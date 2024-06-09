#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        myinput = 'tests/test_models/test_engine/test_db_storage.py'
        result = pep8s.check_files([myinput])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_obj = {"name": "Sandton"}
        new_state = State(**state_obj)
        models.storage.new(new_state)
        models.storage.save()
        session = models.storage._DBStorage__session
        objs = session.query(State).all()
        self.assertTrue(len(objs) > 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state_obj = {"name": "Pretoria"}
        new_state = State(**state_obj)
        models.storage.new(new_state)
        session = models.storage._DBStorage__session
        queried_state = session.query(State).filter_by(id=new_state.id).first()
        self.assertEqual(queried_state.id, new_state.id)
        self.assertEqual(queried_state.name, new_state.name)
        self.assertIsNotNone(queried_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_obj = {"name": "Mbombela"}
        new_state = State(**state_obj)
        models.storage.new(new_state)
        models.storage.save()
        session = models.storage._DBStorage__session
        queried_state = session.query(State).filter_by(id=new_state.id).first()
        self.assertEqual(queried_state.id, new_state.id)
        self.assertEqual(queried_state.name, new_state.name)
        self.assertIsNotNone(queried_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves an item from db properly"""
        storage = models.storage
        storage.reload()
        state_obj = {"name": "Kaapstad"}
        state_ins = State(**state_obj)
        storage.new(state_ins)
        storage.save()
        queried_state = storage.get(State, state_ins.id)
        self.assertEqual(state_ins, queried_state)
        fake_id = storage.get(State, 'test_id')
        self.assertEqual(fake_id, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the right number of elements from the db"""
        storage = models.storage
        storage.reload()
        state_obj = {"name": "Carolina"}
        state_ins = State(**state_obj)
        storage.new(state_ins)
        city_data = {"name": "Ermelo", "state_id": state_ins.id}
        city_ins = City(**city_data)
        storage.new(city_ins)
        storage.save()
        states_count = storage.count(State)
        self.assertEqual(states_count, len(storage.all(State)))
