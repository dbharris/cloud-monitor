import web
import xmlrpclib
import httplib
try: 
    import json
except:
    import simplejson as json
from web import httpserver

render = web.template.render('templates/')
server = xmlrpclib.ServerProxy("http://canfarpool.phys.uvic.ca:8111")
urls = ('/', 'index', '/info','info')

app = web.application(urls, globals())

class index:
    def GET(self):
        try: 
            cluster_resource_lines = server.get_cluster_resources().split('\n')
            cluster_list = [ item.split() for item in cluster_resource_lines ]
            json_resources = json.loads(server.get_json_resource())
            resources = parse_resources(json_resources,cluster_list)
            json_jobs = json.loads(server.get_json_jobpool())
            newjobs = parse_newjobs(json_jobs)
            schedjobs = parse_schedjobs(json_jobs)
            
            return render.index(resources, newjobs, schedjobs)
        except Exception,e:
            return render.error(e)	

if __name__ == "__main__": 
    myfunc=app.wsgifunc()
    web.httpserver.runsimple(myfunc,server_address=("142.104.60.42",80))
	
def parse_resources(json_resources, cluster_list):
    cluster_list_len = len(cluster_list)
    cluster_list.remove(cluster_list[cluster_list_len - 1])
    cluster_list.remove(cluster_list[cluster_list_len - 2])
    cluster_list.remove(cluster_list[0])
    for item in json_resources['resources'][0]['vms']:
        del item['mementry']
        del item['name']
        del item['cloudtype']
    no_vms = len(json_resources['resources'][0]['vms'])
    cpu_archs = json_resources['resources'][0]['cpu_archs']
    cloud_type = json_resources['resources'][0]['cloud_type']
    name = json_resources['resources'][0]['name']
    network_pools = json_resources['resources'][0]['network_pools']
    cpu_cores = json_resources['resources'][0]['cpu_cores']
    memory = json_resources['resources'][0]['memory']
    storageGB = json_resources['resources'][0]['storageGB']
    vms = json_resources['resources'][0]['vms']
    vms_headings = vms[0].keys()
    id_list = []
    status_set = set([vm['status'] for vm in json_resources['resources'][0]['vms']])
    status = [0]*len(status_set)
    for i in xrange(len(status_set)):
        status[i] = status_set.pop()
        status_no = [0]*len(status)
    vmtype_set = set([vm['vmtype'] for vm in json_resources['resources'][0]['vms']])
    vmtype = [0]*len(vmtype_set)
    for i in xrange(len(vmtype_set)):
        vmtype[i] = vmtype_set.pop()
    vmtype_no = [0]*len(vmtype)
    image_set = set([vm['image'] for vm in json_resources['resources'][0]['vms']])
    image = [0]*len(image_set)
    for i in xrange(len(image_set)):
        image[i] = image_set.pop()
    image_no = [0]*len(image)
    for item in json_resources['resources'][0]['vms']:
        id_list.append(item['id'])
        for i in xrange(len(status)):
            if item['status'] == status[i]:
                status_no[i] += 1
        for i in xrange(len(vmtype)):
            if item['vmtype'] == vmtype[i]:
                vmtype_no[i] += 1
        for i in xrange(len(image)):
            if item['image'] == image[i]:
                image_no[i] += 1
    vm_data = json_resources['resources'][0]['vms']
    #for item in vm_data:
    #    id_list.append(item['id'])
    #id_list.sort()
    cluster_list_len = len(cluster_list)
    cluster_list.remove(cluster_list[cluster_list_len - 1])
    cluster_list.remove(cluster_list[cluster_list_len - 2])
    resources = {'cluster_list': cluster_list, 'no_vms': no_vms, 'cpu_archs': cpu_archs, 'cloud_type': cloud_type, 'name': name, 'network_pools': network_pools, 'cpu_cores': cpu_cores, 'memory': memory, 'storageGB': storageGB, 'vms': vms, 'vms_headings': vms_headings, 'id_list': id_list, 'vm_data': vm_data, 'status': status, 'status_no': status_no, 'vmtype': vmtype, 'vmtype_no': vmtype_no, 'image': image, 'image_no': image_no, 'headings': json_resources['resources'][0]['vms'][0].keys()}

    return resources

def parse_newjobs(json_jobs):
    headings = json.loads(json_jobs['new_jobs'][0]).keys()
    newjobinfo = [0]*len(json_jobs['new_jobs'])
    
    for i in xrange(len(json_jobs['new_jobs'])):
        newjobinfo[i] = eval(json_jobs['new_jobs'][i])
    status_set = set([newjob['status'] for newjob in newjobinfo])
    status = [0]*len(status_set)
    user_set = set([newjob['user'] for newjob in newjobinfo])
    user = [0]*len(user_set) 

    for i in xrange(len(status_set)):
        status[i] = status_set.pop()
    status_no = [0]*len(status)

    for i in xrange(len(user_set)):
        user[i] = user_set.pop()
    user_no = [0]*len(user)

    for item in newjobinfo:
        for i in xrange(len(status)):
            if item['status'] == status[i]:
                status_no[i] += 1
        for i in xrange(len(user)):
            if item['user'] == user[i]:
                user_no[i] += 1

    newjobs = {'headings': headings, 'newjobinfo': newjobinfo, 'status': status, 'status_no': status_no, 'user': user, 'user_no': user_no}
    return newjobs

def parse_schedjobs(json_jobs):
    headings = json.loads(json_jobs['sched_jobs'][0]).keys()
    schedjobinfo = [0]*len(json_jobs['sched_jobs'])

    for i in xrange(len(json_jobs['sched_jobs'])):
        schedjobinfo[i] = eval(json_jobs['sched_jobs'][i])
    status_set = set([schedjob['status'] for schedjob in schedjobinfo])
    status = [0]*len(status_set)
    user_set = set([schedjob['user'] for schedjob in schedjobinfo])
    user = [0]*len(user_set)

    for i in xrange(len(status_set)):
        status[i] = status_set.pop()
    status_no = [0]*len(status)

    for i in xrange(len(user_set)):
        user[i] = user_set.pop()
    user_no = [0]*len(user)

    for item in schedjobinfo:
        for i in xrange(len(status)):
            if item['status'] == status[i]:
                status_no[i] += 1
        for i in xrange(len(user)):
            if item['user'] == user[i]:
                user_no[i] += 1

    schedjobs = {'headings': headings, 'schedjobinfo': schedjobinfo, 'status': status, 'status_no': status_no, 'user': user, 'user_no': user_no}
    return schedjobs
