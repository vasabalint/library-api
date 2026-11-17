import unittest
from flask import Flask
from error_handling import AppError, error_response


class ErrorHandlingTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_app_error_attributes(self):
        err = AppError("custom error message", 409)
        self.assertEqual(err.message, "custom error message")
        self.assertEqual(err.status_code, 409)
        self.assertEqual(str(err), "custom error message")

    def test_error_response_function(self):
        with self.app.test_request_context():
            response, code = error_response("not found error", 404)
            self.assertEqual(code, 404)
            self.assertEqual(response.get_json(), {"error": "not found error"})

    def test_error_response_custom_code(self):
        with self.app.test_request_context():
            response, code = error_response("bad request details", 400)
            self.assertEqual(code, 400)
            self.assertEqual(response.get_json(), {"error": "bad request details"})


if __name__ == "__main__":
    unittest.main()
