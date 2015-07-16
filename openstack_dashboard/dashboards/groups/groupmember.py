class Member():

    def __init__(self,member_name=None,member_type='instance',member_group_names=[]):

        self.id = member_name
        self.member_type = member_type
        self.member_group_names = member_group_names 

class Group():

    def __init__(self,member_group_name=None,members=[]):

        self.id = member_group_name
        self.members = members
