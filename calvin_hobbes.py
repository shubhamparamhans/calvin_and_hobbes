import xml.etree.ElementTree as ET
import urllib2
import urllib
import os
from threading import Thread

def find_and_download(ids, folder_name, day, month, year):
	req_url = "http://www.gocomics.com/api/feature/"+ids+"/item.xml?client_code=KAJS6R5FJAS3"
	
	req = urllib2.Request(url=req_url, headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"', 'User-agent':'Mozilla/5.0'})
	f = urllib2.urlopen(req)
	data = f.read()

	new_line = data.find('\n');
	new_data = data[new_line+1:len(data)]

	id_file = ids+".xml"
	a = file(id_file,'w')
	a.write(new_data)
	a.close()

	data_tree = ET.parse(id_file)

	data_root = data_tree.getroot()
	data_objects = data_root.findall('image-link')

	name = day+"-"+month+"-"+year+'.png'

	print("********************Download initiated for "+day+"-"+month+"-"+year+"********************\n")

	urllib.urlretrieve(data_objects[0].text, folder_name+name+".gif")

	print("********************Download completed for "+day+"-"+month+"-"+year+"********************\n")
	os.remove(id_file)


year_data = raw_input("Enter year(yyyy): ")
month_data = raw_input("Enter month(mm): ")
directory_path = year_data+'/'+month_data+'/';

if not os.path.exists(directory_path):
    os.makedirs(directory_path)

req_url = "http://www.gocomics.com/api/feature/32/year/"+year_data+"/month/"+month_data+"/calendar.xml?client_code=KAJS6R5FJAS3"
req = urllib2.Request(url=req_url, headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"', 'User-agent':'Mozilla/5.0'})
f = urllib2.urlopen(req)
data = f.read()
new_line = data.find('\n');
new_data = data[new_line+1:len(data)]

b = file('new_calvin.xml','w')
b.write(new_data)
b.close()

tree = ET.parse('new_calvin.xml')
root = tree.getroot()
objects = root.findall('object')
index = 1
for obj in objects:
	id_is = obj.findall('id')[0].text
	try:
		t= Thread(target=find_and_download, args=(id_is,directory_path, str(index), month_data, year_data))
		t.start()
		index = index+1
	except:
		date = index+"-"+month_data+"-"+year_data
		print("unable to fetch for "+date) 
