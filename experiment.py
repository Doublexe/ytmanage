from foldermanage import FolderManager, Folder
import os
from abc import ABC, abstractmethod
from functools import reduce
from utils import pic_load, pic_save
import warnings
from os import listdir
from os.path import isfile, join



class ExperimentFolder(Folder):
    """Construct or take a folder with experimental ops.

        Ops:
            add_children
            visit children (added)
            set_writer
            set_reader
            save
            load

        """

    def __init__(self, name, parent_path):
        super().__init__(name, parent_path)
        self.writer = None
        self.reader = None

    def add_children(self, name):
        self.children.append(ExperimentFolder(name, parent_path=self.path))

    def set_writer(self, writer):
        self.writer = writer

    def set_reader(self, reader):
        self.reader = reader

    def save(self, obj, name):
        """Use writer function to create files.

        Only require name, not path.
        """
        path = os.path.realpath(os.path.join(self.path, name))
        if self.writer is None:
            raise TypeError("For {}, the writer has not been set.".format(self.name))
        try:
            self.writer(obj, path)
        except:
            print("Fail to add the file using writer.")
            raise

    def load(self, name):
        """Read file information.

        Only require name, not path.
        """
        path = os.path.realpath(os.path.join(self.path, name))
        if self.reader is None:
            raise TypeError("For {}, the reader has not been set.".format(self.name))
        try:
            self.reader(path)
        except:
            print("Fail to extract the file using writer.")
            raise


class ExperimentManager(FolderManager, ABC):
    """Construct or take a structure, under a 'name' folder. With experimental CONF.
    The 'name_given_by_CONF' also joins the name of pointed experiments.

    STRUCTURE:
        name/
            name_given_by_CONF + name_of_pointed/ <- [root]
                meta/
                    ...
                main_structure_1/
                    sub_structure_1/
                    sub_structure_2/
                    ...
                main_structure_2/
                    sub_structure_1/
                    sub_structure_2/
                    ...
                ...

    Must override:
        extract
        set_meta_reader_writer

    Ops:
        finish_log
        show_structure
        set_meta_reader_writer
        save_meta
        load_meta
    """

    def __init__(self, name, parent, CONF, structure, point_to=None, construct = True):
        """Construct the folder according to path and CONF.

        :param parent: The directory containing the name
        :param CONF: The configuration of this experiment.
        :param point_to: A list
        containing the information sources. The point (reference) information will be automatically added.
        """

        self.CONF = CONF
        self.structure = structure
        self.name = name

        if self.structure is None:
            raise ValueError("Please initiate folder structure within the Experiment Class.")

        self.experiment_name = self.extract(self.CONF)
        self.Folder = ExperimentFolder

        temp = self.Folder(self.name, parent)

        if point_to is not None:
            for experiment in point_to:
                # self.CONF.extend(experiment.CONF)
                self.experiment_name = self.experiment_name + '//' + experiment.experiment_name

        super().__init__(self.experiment_name, temp.path, self.structure, self.Folder,construct)

        # Set the 'meta' file, save some basic configurations and check for repetitions
        self._meta_file()
        self._set_meta_reader_writer()

    def _meta_file(self):
        """Make a meta folder."""
        self.root.add_children('meta')

    def _check_finish_log(self):
        mypath = self.root.meta.path
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        if 'finished' in files:
            warnings.warn('The experiment has been done with the same configuration.')

    def finish_log(self):
        self.save_meta(1, 'finished')

    def show_structure(self):
        print('')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('The structure of experiment: {}'.format(self.name))
        print('')
        self.root.show_content()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('')

    @abstractmethod
    def _set_meta_reader_writer(self):
        self.root.meta.set_writer(lambda obj, name: pic_save(name, obj))
        self.root.meta.set_reader(lambda name: pic_load(name))

    def save_meta(self, obj, name):
        """Set meta information for the experiment."""
        self.root.meta.save(obj, name)

    def load_meta(self, name):
        """Read out meta info from files in meta."""
        self.root.meta.load(name)

    @staticmethod
    @abstractmethod
    def extract(CONF):
        """Extract CONF to get experiment name.

        Please write down what information you want to record from CONF.
        """
        temp = ['some_property']
        todo = []
        for st in temp:
            todo.append(st + '-' + str(CONF[st]))
        return reduce(lambda x, y: x + '__' + y, todo)
