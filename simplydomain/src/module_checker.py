#!/usr/bin/python3.6


"""
SimplyDomainChecker.python
Author: Brad Crawford

Takes JSON input from SimplyDomain and resolves subdomain CNAMES
looking for possible subdomain takeover opportunities.

"""

import sys
import json
import requests
import argparse
import asyncio
import aiodns
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from simplydomain.src.module_provider import PROVIDER_LIST

class HttpChecker(object):
	
	def __init__(self, url_obj):
		"""
		url_obj=DICT: url:cname
		"""
		self.url_obj = url_obj

	async def fetch(self, sem, url, cname, session):
		async with sem:
			response_obj = {}
			response_obj['subdomain'] = "http://" + url
			response_obj['cname'] = cname
			response_obj['takeover'] = False
			for obj in PROVIDER_LIST:
				if all(key in cname for key in obj['cname']):
					try:
						async with session.get(response_obj['subdomain']) as response:
							print("Testing: {}".format(url))
							print("URL: {} Status: {}".format(response.url, response.status))
							data = await response.read()							
							for r in obj['response']:
								if r in str(data):
									response_obj['takeover'] = True
									response_obj['type'] = {}
									response_obj['type']['confidence'] = "HIGH"
									response_obj['type']['provider'] = obj['name']
									response_obj['type']['response'] = r
									response_obj['type']['response_status'] = response.status
									print("Got one: {}".format(response_obj))
									return response_obj
							return response_obj
					except ClientConnectorError as e:
						print("Connection Error: {} CNAME: {}".format(e,cname))
						response_obj['takeover'] = True
						response_obj['type'] = {}
						response_obj['type']['confidence'] = "MEDIUM"
						response_obj['type']['provider'] = obj['name']
						response_obj['type']['response'] = e
						response_obj['type']['response_status'] = None
						return response_obj
					except Exception as e:
						print("Doh!: {} ErrorType: {} CNAME: {}".format(e, type(e),cname))
			return None

	async def tasker(self):
		tasks = []
		sem = asyncio.Semaphore(512)
		async with ClientSession(conn_timeout=3) as session:
			for url,cname in self.url_obj.items():
				task = asyncio.ensure_future(self.fetch(sem, url, cname, session))
				tasks.append(task)
			responses = asyncio.gather(*tasks)
			await responses
			return responses.result()

	def run(self):
		loop = asyncio.get_event_loop()
		future = asyncio.ensure_future(self.tasker())
		loop.run_until_complete(future)
		return [x for x in future.result() if x is not None]

			
class DnsChecker(object):
	
	def __init__(self, url_list, dns_server_count = 20):
		"""
		url_list=LIST: urls to check for CNAME
		:return: cname_results DICT: url:cname
		"""
		self.url_list = url_list
		self.sem = asyncio.Semaphore(512)
		self.loop = asyncio.get_event_loop()
		self.dns_servers = get_dns_servers(dns_server_count)
		self.resolver = aiodns.DNSResolver(loop=self.loop, servers=self.dns_servers, timeout=2, tries=2, rotate=True)
		self.cname_results = {}

	async def fetch(self, url):
		async with self.sem:
			try:
				response = await self.resolver.query(url,'CNAME')
				self.cname_results.update({url:response.cname})
				return { "url": url, "cname": response.cname } if response.cname is not None else None
			except Exception as e:
				print("Error: {}".format(e))
				return None

	async def tasker(self):
		tasks = []
		for url in self.url_list:
			task = asyncio.ensure_future(self.fetch(url))
			tasks.append(task)
		responses = asyncio.gather(*tasks, return_exceptions=True, loop=self.loop)
		await responses
		
	def run(self):
		print("DNS servers: {}".format(self.dns_servers))
		future = asyncio.ensure_future(self.tasker())
		self.loop.run_until_complete(future)
		return self.cname_results

def get_dns_servers(count):
	try:
		r = requests.get('https://public-dns.info/nameserver/us.json')
		data = json.loads(r.text)
		servers = [i['ip'] for i in data if (i['reliability'] == 1)]
		servers_prune = servers[:count]
		return(servers_prune)
	except Exception as e:
		print("get_dns_servers error: {}".format(e))
#TODO return None or something