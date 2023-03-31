import logging
from flask import Flask, request
from multiply import MultiplyNumbers

app = Flask(__name__)


@app.route('/stringPrinter',  methods=['GET'])
def string_printer():
    try:
        text_entered = request.args.get('text_entered')
        response = {"Text entered:": text_entered}
        logging.info("string printer has been called")
        return response
    except Exception as e:
        logging.error(e)


@app.route('/multiply', methods=['GET'])
def multiply():
    try:
        # this method should multiply two numbers passed in and return the result
        first_number = validate_int_parameter_type(request.args.get('first_number', None))
        second_number = validate_int_parameter_type(request.args.get('second_number', None))
        # validate that the integers are valid, if not throw a value error
        if type(first_number) == int and type(second_number) == int:
            mn = MultiplyNumbers()
            result = mn.multiply(first_number, second_number)
            response = {"status_code": 200, "multiplication_result": result}
            return response
        else:
            raise ValueError
    except ValueError:
        logging.error("failed to convert user input value to integer, user values: " + str(first_number)
                      + str(second_number))
        return {"status_code": 400, "multiplication_result": "please check the values you input are integers"}
    except Exception as e:
        logging.error(e)
        return {"status_code": 500, "multiplication_result": ""}


def validate_int_parameter_type(value):
    try:
        if type(value) == int:
            return value
        else:
            return int(value)
    except ValueError:
        logging.error("failed to convert user input value to integer, user value: " + value)
        return {"status_code": 400, "multiplication_result": "please check the values you input are integers"}

