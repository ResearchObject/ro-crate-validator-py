import module

class TestClass:

    def test_function_1(self):
        # Override the Python built-in input method 
        module.input = lambda: 'aaa'
        # Call the function you would like to test (which uses input)
        output = module.function1()  
        assert output == 'aaa'

    def test_function_2(self):
        module.input = lambda: 'bbb'
        output = module.function2()  
        assert output == 'bbb'        

    def teardown_method(self, method):
        # This method is being called after each test case, and it will revert input back to original function
        module.input = input