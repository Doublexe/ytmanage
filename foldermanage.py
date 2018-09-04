import os


class Folder(object):
    """Construct or take a folder with ops.

    Ops:
        add_children
        visit children (added)
        show_content
        save
        load

    """
    def __init__(self, name, parent_path):
        self.name = name
        if not os.path.exists(parent_path):
            raise IOError("Parent path doesn't exist for {}.".format(self.name))
        self.path = os.path.realpath(os.path.join(parent_path, self.name))

        self.parent_path = parent_path
        self.children = []

        self._make()

    @property
    def children_name(self):
        return [child.name for child in self.children]

    def __getattr__(self, item):
        for child in self.children:
            if child.name == item:
                return child

    def add_children(self, name):
        self.children.append(Folder(name, parent_path=self.path))

    def save(self, writer, name):
        """add file to list and use writer function to create them"""
        try:
            writer(os.path.realpath(os.path.join(self.path, name)))
        except:
            print("Fail to add the file using writer.")
            raise

    def load(self, reader, name):
        """Read file information."""
        try:
            reader(os.path.realpath(os.path.join(self.path, name)))
        except:
            print("Fail to extract the file using writer.")
            raise


    @staticmethod
    def _list_files(startpath, limit=None):
        """print all the files in a directory with limit to non-directorial files."""
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            count = 1
            for f in files:
                if limit is not None:
                    if f[-1] != r'/':
                        if count <= limit:
                            count += 1
                            print('{}{}'.format(subindent, f))
                        elif count == limit + 1:
                            count += 1
                            print('{}{}'.format(subindent, '......'))
                    else:
                        print('{}{}'.format(subindent, f))
                else:
                    print('{}{}'.format(subindent, f))

    def show_content(self, limit=None):
        self._list_files(self.path, limit)

    def _make(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            print("Already exists: {}.".format(self.path))


class FolderManager(object):
    """Construct or take a structure, under a 'name' folder.

    STRUCTURE:
        name/ <- [root]
            main_structure_1/
                sub_structure_1/
                sub_structure_2/
                ...
            main_structure_2/
                sub_structure_1/
                sub_structure_2/
                ...
            ...
    """

    def __init__(self, name, parent, struct_dict, Folder, construct = True):
        """Give the working directory.
        :param parent: str
        """
        self.FLAG = 0
        self.parent = parent  # todo
        self.root = None
        self.structure = struct_dict
        self.Folder = Folder
        self.name = name
        if(construct):
            self._construct_structure()
        else:
            self._check_construct_structure()

    def _check_construct(self, structure, parent):
        for key, item in structure.items():
            assert parent.__getattr__(key) is not None, "The structure doesn't hold!"
            if isinstance(item, dict):
                self._check_construct(item, parent.__getattr__(key))

    def _construct(self, structure, parent):
        for key, item in structure.items():
            parent.add_children(key)
            if isinstance(item, dict):
                self._construct(item, parent.__getattr__(key))

    def _set_root_node(self,name,path):
        return self.Folder(name, path)

    def _construct_structure(self):
        self.root = self._set_root_node(self.name,self.parent)
        self._construct(self.structure, self.root)

    def _check_construct_structure(self):
        exit("Unfinished method.")
