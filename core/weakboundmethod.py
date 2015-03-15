# encoding: UTF-8
import weakref

class WeakBoundMethod:
	"""
	Wrapper around a method bound to a class instance. As opposed to bare
	bound methods, it holds only a weak reference to the `self` object,
	allowing it to be deleted.
	
	This can be useful when implementing certain kinds of systems that
	manage callback functions, such as an event manager.
	"""
	def __init__(self, meth):
		"""
		Initializes the class instance. It should be ensured that methods
		passed through the `meth` parameter are always bound methods. Static
		methods and free functions will produce an `AttributeError`.
		"""		
		self._self = weakref.ref(meth.__self__)
		if self._self is None:
			raise AttributeError("Method does not have __self__")
		
		self._func = meth.__func__
		if self._func is None:
			raise AttributeError("Method does not have __function__")
		
		
	
	"""
	Calls the bound method and returns whatever object the method returns.
	Any arguments passed to this will also be forwarded to the method.

	Raises a weakref.ReferenceError if self has been collected.
	"""
	def __call__(self, *args, **kw):
		      
		_self = self._self()
		if _self is None:
			raise weakref.ReferenceError()

		return self._func(_self, *args, **kw)