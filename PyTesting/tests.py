from testing import TestCase, TestResult, TestSuite, TestLoader

class WasRun(TestCase):
	def setUp(self):
		self.log = "setUp "
	
	def testMethod(self):
		self.log += "testMethod "
	
	def testBrokenMethod(self):
		raise Exception
		
	def tearDown(self):
		self.log += "tearDown "

class TestCaseTest(TestCase):
	def setUp(self):
		self.result = TestResult()
	
	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert(test.log == "setUp testMethod tearDown ")
	
	def testResult(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("1 run, 0 failed" == self.result.summary())
	
	def testFailedResult(self):
		test = WasRun("testBrokenMethod")
		test.run(self.result)
		assert("1 run, 1 failed" == self.result.summary())
	
	def testFailedResultFormatting(self):
		self.result.testStarted()
		self.result.testFailed()
		assert("1 run, 1 failed" == self.result.summary())
	
	def testSuite(self):
		tests = [WasRun('testMethod'), WasRun('testBrokenMethod')]
		suite = TestSuite(tests)
		suite.run(self.result)
		assert("2 run, 1 failed" == self.result.summary())
	
	def testSuiteAddTestList(self):
		tests = [WasRun('testMethod'), WasRun('testBrokenMethod')]
		suite = TestSuite()
		suite.addTests(tests)
		suite.run(self.result)
		assert("2 run, 1 failed" == self.result.summary())
	
	def testLoaderGetTestNames(self):
		loader = TestLoader()
		assert(['testBrokenMethod', 'testMethod'] == loader.getTestNames(WasRun))
	
	def testLoaderFromTestCase(self):
		loader = TestLoader()
		loader.loadTestsFromTestCase(WasRun).run(self.result)
		assert("2 run, 1 failed" == self.result.summary())
	
	def testLoaderFromModule(self):
		import test_module
		loader = TestLoader()
		loader.loadTestsFromModule(test_module).run(self.result)
		assert("1 run, 0 failed" == self.result.summary())
	
if __name__ == "__main__":
	result = TestResult()
	TestLoader().loadTestsFromTestCase(TestCaseTest).run(result)
	print result.summary()
