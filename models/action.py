import requests
from pathlib import Path

from core.models import action
from core import helpers

class _api(action._action):
	headers = dict()
	url = str()
	method = str()
	ca = str()
	postData = str()
	cookies = dict()
	timeout = int()
	proxy = dict()
	returnsJson = bool()

	def __init__(self):
		pass

	def run(self,data,persistentData,actionResult):
		headers = helpers.evalDict(self.headers,{"data" : data})
		url = helpers.evalString(self.url,{"data" : data})
		method = helpers.evalString(self.method,{"data" : data}).upper()
		postData = helpers.evalString(self.postData,{"data" : data})

		kwargs={}
		kwargs["headers"] = headers
		if self.timeout == 0:
			kwargs["timeout"] = 5
		else:
			kwargs["timeout"] = self.timeout
		if self.ca:
			kwargs["verify"] = Path(self.ca)
		if self.proxy:
			kwargs["proxies"] = self.proxy
		else:
			kwargs["proxies"] = { "http": None, "https": None }
		if self.cookies:
			cookies = helpers.evalDict(self.cookies,{"data" : data})
			kwargs["cookies"] = cookies

		try:
			if method == "GET":
				response = requests.get(url,**kwargs)
			elif method == "POST":
				kwargs["data"] = postData
				response = requests.post(url,**kwargs)
			elif method == "PUT":
				kwargs["data"] = postData
				response = requests.put(url,**kwargs)
			elif method == "DELETE":
				response = requests.delete(url,**kwargs)

			text = response.text
			if self.returnsJson:
				try:
					text = response.json()
				except:
					text = response.text		

			actionResult["result"] = True
			actionResult["rc"] = response.status_code
			actionResult["data"] = { "headers" : dict(response.headers), "text" : text }
		
		except:
			actionResult["result"] = False
			actionResult["rc"] = 404

		return actionResult

