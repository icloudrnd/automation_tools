class Task():

    def start(self):

        pass

    def kill(self):

        pass

    def state(self):

        pass

    def set_scope(self):

        pass

    def get_scope(self):

        pass

    def is_complete(self):

        pass

    def load_data_from_file():

        pass

    def prepare_sls():

        pass

class ActiveTask(Task):
    """
    Active Task data
    """

    def __init__(self, id, function=None, target=None, user=None, target_type=None, returned=None, running_on=None, arguments=None):
        self.id = id
        self.function = function
        self.target = target
        self.user = user
        self.target_type = target_type
        self.returned = returned
        self.running_on = running_on
        self.arguments = arguments

class CompletedTask(Task):
    """
    Completed Task data
    """

    def __init__(self, id = None, function=None, added=None, success=None, return_field=None, scope=None , collection = None):
        self.id = id
        self.function = function
        self.added = added
        self.success = success
        self.return_field = return_field
        self.scope = scope
        self.collection = collection

    def split_return_field(self):

        # bug

        return [ i for i in str(self.collection.return_field).split("\\n")]

class Instance():

    def __init__(self, id = None, function=None, added=None, success=None ,active_tasks=None):
        self.id = id 
        self.function = function
        self.added = added
        self.success = success
        self.active_tasks = active_tasks


    







class File():

    def __init__(self):

        pass


    def get_file_content():

        pass

    def replace_with_new_content():

        pass

    


class PackageInstallTask(Task):

    def __init__(self):

        pass

    def install():

        pass

    def remove():

        pass

    def add_package_name_to_file():

        pass

    def remove_package_name_from_file():

        pass


class UserTask(Task):

    def add_user():

        pass

    def del_user():

        pass

