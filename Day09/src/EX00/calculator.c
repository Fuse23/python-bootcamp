#include <Python.h>

static PyObject *add_method(PyObject *self, PyObject args[]) {
    double number1, number2 = 0;
    if (!PyArg_ParseTuple(args, "dd", &number1, &number2)) {
        return NULL;
    }
    return PyFloat_FromDouble(number1 + number2);
}

static PyObject *sub_method(PyObject *self, PyObject args[]) {
    double number1, number2 = 0;
    if (!PyArg_ParseTuple(args, "dd", &number1, &number2)) {
        return NULL;
    }
    return PyFloat_FromDouble(number1 - number2);
}

static PyObject *mul_method(PyObject *self, PyObject args[]) {
    double number1, number2 = 0;
    if (!PyArg_ParseTuple(args, "dd", &number1, &number2)) {
        return NULL;
    }
    return PyFloat_FromDouble(number1 * number2);
}

static PyObject *div_method(PyObject *self, PyObject args[]) {
    double number1, number2 = 0;
    if (!PyArg_ParseTuple(args, "dd", &number1, &number2)) {
        return NULL;
    }
    if (number2 == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
        return NULL;
    }
    return PyFloat_FromDouble(number1 / number2);
}

static PyMethodDef CalculatorMethods[] = {
    {"add", add_method, METH_VARARGS, "Additional function"},
    {"sub", sub_method, METH_VARARGS, "Subtraction function"},
    {"mul", mul_method, METH_VARARGS, "Multiplication function"},
    {"div", div_method, METH_VARARGS, "Division function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef CalculatorModule = {
    PyModuleDef_HEAD_INIT,
    "calculator",
    "My C calculator",
    -1,
    CalculatorMethods
};

PyMODINIT_FUNC
PyInit_calculator(void) {
    return PyModule_Create(&CalculatorModule);
}
