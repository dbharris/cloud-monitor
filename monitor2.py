import web
import xmlrpclib
import httplib
from web import httpserver

render = web.template.render('templates/')
server = xmlrpclib.ServerProxy("http://canfarpool.phys.uvic.ca:8111")
urls = (
	'/', 'index', 'error')

app = web.application(urls, globals())

class index:
	def GET(self):
                try: 
			cloudInfo = [server.get_cluster_resources(),server.get_highjobs(),server.get_newjobs(),server.get_schedjobs(),server.get_cluster_vm_resources()]
			return render.index(cloudInfo)
		
		except httplib.socket.error,e:
			return render.error(e)	



if __name__ == "__main__": 
	myfunc=app.wsgifunc()
	web.httpserver.runsimple(myfunc,server_address=("142.104.60.42",8080))
	

