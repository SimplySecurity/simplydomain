import multiprocessing as mp


class ModuleRecursion(object):
	"""Class to handle recursion.
	
	Simple class to handle tracking and storing prior 
	sub-domains discovred.
	""" 

	def __init__(self):
		"""class init.
		""" 
		self.recursion_queue = mp.Queue()

	def add_subdomain(self, domain):
		"""add subdomain to Q.
		
		uses a non-blocking call to add to the Q
		to prevent any errors with size. 
		
		Arguments:
			domain {str} -- subdomain to add to Q
		"""  
		self.recursion_queue.put(domain)

	def get_subdomain_list(self, valid_only=True):
		"""build subdomain list.
		
		Using the JSON from the event consumer, we
		can easily build a unique list of 
		subdomains for  module use.
		
		Keyword Arguments:
			valid_only {bool} -- filter only valid subdomains (default: {True})
		
		Returns:
			list -- list of raw subdomains
		"""
		data = []
		refill = []
		while True: 
			try:
				x = self.recursion_queue.get_nowait()
				if valid_only and x.valid:
					data.append(x.subdomain)
				if not valid_only:
					data.append(x.subdomain)
			except Exception as e:
				print(e)
				break
		return set(data)