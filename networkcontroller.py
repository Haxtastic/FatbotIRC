class NetworkController():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.RegisterListener(self)

	#----------------------------------------------------------------------
	def Notify(self, event):
		pass
		