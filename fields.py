"""fields helper module"""


class FieldsHelper():
    """class that helps tho get fields configuration"""
    def __init__(self):
        self.mandatory_fields = ['username', 'password']
        self.password_types = ['Email Password', 'Website Password']
        self.fields_conf = {'Email Password':
                            {'email': {'mandatory': True, 'enabled': True}},
                            'Website Password':
                            {'link': {'mandatory': True, 'enabled': True}}}

    def get_password_types(self):
        """gets password types"""
        return self.password_types

    def get_fields_conf(self, password_type):
        """returns configuration for given password_type"""
        conf = self.fields_conf[password_type]
        for field in self.mandatory_fields:
            conf[field] = {'mandatory': True, 'enabled': True}
        return conf
