import testing

class Test(testing.TestCase):
	def setUp(self):
		self.a_string = "Test"
	
	def testName(self):
		assert("Test" == self.a_string)
	
	def tearDown(self):
		self.a_string = ""

if __name__ == "__main__":
	testing.main()
