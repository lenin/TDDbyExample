require 'testing'

class WasRun < Testing::TestCase
	attr_reader :log
	
	def setup
		@log = 'setUp '
	end
	
	def testMethod
		@log += 'testMethod '
	end
	
	def testBrokenMethod
		raise
	end
	
	def teardown
		@log += 'tearDown '
	end
end

class TestCaseTest < Testing::TestCase
	def setup
		@result = Testing::TestResult.new
	end
	
	def testTemplateMethod
		test = WasRun.new 'testMethod'
		test.run @result
		assert 'setUp testMethod tearDown ' == test.log
	end
	
	def testResult
		test = WasRun.new 'testMethod'
		test.run @result
		assert '1 run, 0 failed' == @result.summary
	end

	def testFailedResultFormatting
		@result.testStarted
		@result.testFailed
		assert '1 run, 1 failed' == @result.summary
	end
	
	def testFailedResult
		test = WasRun.new 'testBrokenMethod'
		test.run @result
		assert '1 run, 1 failed' == @result.summary
	end
	
	def testSuite
		tests = [WasRun.new('testMethod'), WasRun.new('testBrokenMethod')]
		suite = Testing::TestSuite.new tests
		suite.run @result
		assert '2 run, 1 failed' == @result.summary
	end
	
	def testSuiteAddTestList
		tests = [WasRun.new('testMethod'), WasRun.new('testBrokenMethod')]
		suite = Testing::TestSuite.new
		suite.addTests tests
		suite.run @result
		assert '2 run, 1 failed' == @result.summary
	end
	
	def testLoaderGetTestNames
		assert ['testBrokenMethod', 'testMethod'] == Testing::TestLoader.getTestNames(WasRun)
	end
	
	def testLoaderFromTestCase
		Testing::TestLoader.loadTestsFromTestCase(WasRun).run @result
		assert '2 run, 1 failed' == @result.summary
	end
end

Testing::TestRunner.run TestCaseTest
