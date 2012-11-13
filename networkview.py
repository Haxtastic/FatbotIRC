class NetworkView():

	#----------------------------------------------------------------------
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener( self )
		self.client = None

	#----------------------------------------------------------------------
	def Notify(self, event):
		pass
