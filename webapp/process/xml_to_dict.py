from lxml import etree

def xmltodict(file='new.xml'):
	root = etree.ElementTree(file=file).getroot()
	hosts = root.findall('host')
	if hosts:
		result = []
	else:
		return []
	for host in hosts:
		if host.find('status').get('state') == 'up':
			# port info
			if host.find('ports') is not None:
				ports = host.find('ports').findall('port')
				if ports is not None:
					portinfo = []
					for port in ports:
						pi = {}
						pi['portid'] = port.get('portid')
						pi['state'] = port.find('state').get('state')
						pi['service'] = port.find('service').get('name')
						if port.find('script') is not None:
							pi['banner'] = port.find('script').get('output')
						portinfo.append(pi)
				else:
					portinfo = []
			else:
				portinfo = []

			address = host.find('address').get('addr')
			result.append({
				'host': address,
				'portinfo': portinfo
			})
			# result.append({
			# 	'portinfo':portinfo,
			# 	'address':address
			# })
	# print(result)
	return result

if __name__ == '__main__':
	xmltodict()
