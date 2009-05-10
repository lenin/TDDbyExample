module Testing
	class TestResult
		def initialize
			@runCount = 0
			@errorCount = 0
		end
		
		def testStarted
			@runCount += 1
		end
		
		def testFailed
			@errorCount += 1
		end
		
		def summary
			"#{@runCount} run, #{@errorCount} failed"
		end
	end

	class TestCase
		def initialize name
			@name = name
		end
		
		def setup
		end
		
		def teardown
		end
		
		def run result
			result.testStarted
			setup
			begin
				self.send @name
			rescue
				result.testFailed
			end
			teardown
		end
		
		def assert boolean
			boolean or raise
		end
	end

	class TestSuite
		def initialize tests=[]
			@tests = []
			addTests tests
		end
		
		def addTest test
			@tests.push test
		end
		
		def addTests tests
			tests.each { |test| addTest test }
		end
		
		def run result
			@tests.each { |test| test.run(result) }
		end
	end

	class TestLoader
		def TestLoader.loadTestsFromTestCase testCaseClass
			tests = []
			getTestNames(testCaseClass).each { |name|
				tests.push testCaseClass.new(name)
			}
			TestSuite.new tests
		end
		
		def TestLoader.getTestNames testCaseClass
			testNames = []
			testCaseClass.public_instance_methods.each { |name|
				if name.match /^test/ then testNames.push name end
			}
			testNames.sort
		end
	end

	class TestRunner
		def TestRunner.run testCaseClass
			result = TestResult.new
			TestLoader.loadTestsFromTestCase(testCaseClass).run result
			puts result.summary
		end
	end
end
