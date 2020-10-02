import json


class RequestArgs():
    def __init__(self, request_args):
        self.request_args = request_args

    def get(self, name, default='', contain_str=False):
        if contain_str:
            for key, value in self.request_args.items():
                if name in key:
                    return {key: value}
        else:
            value = self.request_args.get(name)
            if value is None:
                return default
            if type(value) == list and len(value) > 0:
                return value[0]
            return value

        return default

    def get_list(self, name, default='', contain_str=False):
        entries = []
        for key, value in self.request_args.items():
            values = dict.__getitem__(self.request_args, key)
            key_fixed = key.replace('[]', '')
            for entry in values:
                if contain_str:
                    if name in key_fixed:
                        entries.append({key_fixed: entry})
                else:
                    if key_fixed == name:
                        entries.append(entry)
        return entries


class RequestHandler():
    def __init__(self, data):
        self.auth_required = data['auth_required']
        self.secret_key = data['secret_key']

        request_obj = data['request_obj']
        self.auth_token = request_obj.headers.get('Authorization')
        if self.auth_token is None:
            self.auth_token = request_obj.headers.get('authorization')
        self.args = request_obj.args

        self.remote_addr = request_obj.remote_addr

        if data['app_type'] == 'flask':
            self.data = request_obj.json
        elif data['app_type'] == 'lambda_proxy':
            try:
                self.data = json.loads(request_obj.data)
            except:
                self.data = {}

        self.customer_token = None
        self.selected_customer_profile = None

        self.adm_cp = request_obj.headers.get('Adm-Cp')
        if self.adm_cp is None:
            self.adm_cp = request_obj.headers.get('adm_cp')

        self.adm_auth_code = request_obj.headers.get('Adm-Auth-Code')
        if self.adm_auth_code is None:
            self.adm_auth_code = request_obj.headers.get('adm_auth_code')

