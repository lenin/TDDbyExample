import types

class TestResult:
	def __init__(self):
		self.runCount = 0
		self.errorCount = 0
	
	def testStarted(self):
		self.runCount += 1
		
	def testFailed(self):
		self.errorCount += 1
	
	def summary(self):
		return '%d run, %d failed' % (self.runCount, self.errorCount)

class TestCase:
	def __init__(self, name):
		self.name = name
	
	def setUp(self):
		pass
	
	def run(self, result):
		result.testStarted()
		self.setUp()
		try:
			getattr(self, self.name)()
		except:
			result.testFailed()
		self.tearDown()
	
	def tearDown(self):
		pass
	
	def __repr__(self):
		return '<%s %s>' % (self.__class__, self.name)

class TestSuite:
	def __init__(self, tests=[]):
		self.tests = []
		self.addTests(tests)
	
	def addTest(self, test):
		self.tests.append(test)
	
	def addTests(self, tests):
		for test in tests:
			self.addTest(test)
	
	def run(self, result):
		for test in self.tests:
			test.run(result)

class TestLoader:
	def loadTestsFromTestCase(self, testCaseClass):
		return TestSuite(map(testCaseClass, self.getTestNames(testCaseClass)))
	
	def loadTestsFromModule(self, module):
		tests = []
		for name in dir(module):
			class_obj = getattr(module, name)
			if isinstance(class_obj, (type, types.ClassType)) and issubclass(class_obj, TestCase):
				tests.append(self.loadTestsFromTestCase(class_obj))
		return TestSuite(tests)
	
	def getTestNames(self, testCaseClass):
		testNames = filter(lambda name: name.startswith('test'), dir(testCaseClass))
		testNames.sort()
		return testNames

def main(module='__main__'):
	if type(module) == type(''):
		module_name = module
		module = __import__(module_name)
		for part in module_name.split('.')[1:]:
			module = getattr(module, part)
	result = TestResult()
	TestLoader().loadTestsFromModule(module).run(result)
	print result.summary()
