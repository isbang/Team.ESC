import json
import requests
try:
    import shortid
except:
    import lib.shortid as shortid

base_headers = {}
base_headers['X-M2M-RI'] = ""
base_headers['Accept'] = "application/"
base_headers['X-M2M-Origin'] = ""
base_headers['Locale'] = "en"


class createAE(object):
    """docstring for createAE."""

    def __init__(self, conf):
        super(createAE, self).__init__()
        self.headers = base_headers
        self.ae = conf.AE
        self.cse = conf.CSE

        self.body = {}
        self.body["m2m:ae"] = {}
        self.body["m2m:ae"]["rn"] = self.ae.name
        self.body["m2m:ae"]["api"] = self.ae.appid
        self.body["m2m:ae"]["rr"] = True

        self.bodyString = json.dumps(self.body)

        self.headers["X-M2M-RI"] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers['X-M2M-Origin'] = self.ae.id
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + self.ae.bodytype + ";ty=" + conf.Type.AE
        self.headers['Content-Length'] = str(len(self.bodyString))

    def send(self):
        url = 'http://' + self.cse.host + ':' + self.cse.port + self.cse.id + '?rcn=3'
        # print("Try Create AE:", url)

        self.res = requests.post(url, data=self.bodyString, headers=self.headers)
        return self.res


class retrieveAE(object):
    """docstring for retrieveAE."""

    def __init__(self, conf):
        super(retrieveAE, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE

        self.headers = base_headers
        self.headers["X-M2M-RI"] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers['X-M2M-Origin'] = self.ae.id

    def send(self):
        url = 'http://' + self.cse.host + ':' + self.cse.port + self.cse.id + self.ae.id
        self.res = requests.get(url, headers=self.headers)

        return self.res


class createCNT(object):
    """docstring for createCNT."""

    def __init__(self, conf, cnt):
        super(createCNT, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE
        self.cnt = cnt

        self.body = {}
        self.body["m2m:cnt"] = {}
        self.body["m2m:cnt"]["rn"] = self.cnt['name']
        self.body["m2m:cnt"]["lbl"] = [self.cnt['name']]

        self.bodyString = json.dumps(self.body)

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers["X-M2M-Origin"] = self.ae.id
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + self.ae.bodytype + ";ty=" + conf.Type.CNT
        self.headers["Content-Length"] = str(len(self.bodyString))

    def send(self):
        url = "http://" + self.cse.host + ":" + self.cse.port + self.cnt["parent"] + '?rcn=3'
        self.res = requests.post(url, data=self.bodyString, headers=self.headers)

        return self.res


class retrieveCI(object):
    """docstring for retrieveCI."""

    def __init__(self, conf, cnt):
        super(retrieveCI, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE
        self.cnt = cnt

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers["X-M2M-Origin"] = self.ae.id

    def send(self):
        url = 'http://' + self.cse.host + ":" + self.cse.port + self.cnt['parent'] + "/" + self.cnt['name'] + "/latest"
        print(url)
        self.res = requests.get(url, headers=self.headers)
        print("success")

        return self.res


class discovery(object):
    """docstring fo discovery."""

    def __init__(self, conf):
        super(discovery, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers["X-M2M-Origin"] = self.ae.name

    def send(self):
        url = 'http://' + self.cse.host + ':' + self.cse.port + self.cse.id + "?fu=1&ty=2"
        self.res = requests.get(url, headers=self.headers)

        return self.res


class createCI(object):
    """docstring for createCI."""

    def __init__(self, sender, target, con, bodytype="json", type="4"):
        super(createCI, self).__init__()
        self.url = target
        self.con = con

        self.body = {}
        self.body["m2m:cin"] = {}
        self.body["m2m:cin"]["con"] = con
        self.bodyString = json.dumps(self.body)

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers["Accept"] += bodytype
        self.headers["X-M2M-Origin"] = sender
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + bodytype + ";ty=" + type
        self.headers["Content-Length"] = str(len(self.bodyString))

    def send(self):
        url = "http://" + self.url
        self.res = requests.post(url, data=self.bodyString, headers=self.headers)

        return self.res
