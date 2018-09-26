/* copied from python/cpython@c87d9f40 Python/bltinmodule.c Python/sysmodule.c
 * and modified for compat
 */

#include <Python.h>

#if PY_MAJOR_VERSION >= 3
#define BUILTINS_MOD "builtins"
#else
#define BUILTINS_MOD "__builtin__"
#endif

static PyObject* _breakpoint(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject* retval;
    PyObject *hook = PySys_GetObject("breakpointhook");

    if (hook == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.breakpointhook");
        return NULL;
    }
    Py_INCREF(hook);
    retval = PyObject_Call(hook, args, kwds);
    Py_DECREF(hook);
    return retval;
}

PyDoc_STRVAR(_breakpoint_doc,
"breakpoint(*args, **kws)\n\
\n\
Call sys.breakpointhook(*args, **kws).  sys.breakpointhook() must accept\n\
whatever arguments are passed.\n\
\n\
By default, this drops you into the pdb debugger.");

static PyObject* _breakpointhook(PyObject* self, PyObject* args, PyObject* kwds) {
    char *envar;
    PyObject *envar_obj, *modulepath, *module, *hook, *retval, *msg;
    const char *last_dot, *attrname;
    int status;

    assert(!PyErr_Occurred());
    envar = Py_GETENV("PYTHONBREAKPOINT");

    if (envar == NULL || strlen(envar) == 0) {
        envar = "pdb.set_trace";
    }
    else if (!strcmp(envar, "0")) {
        /* The breakpoint is explicitly no-op'd. */
        Py_RETURN_NONE;
    }
    /* According to POSIX the string returned by getenv() might be invalidated
     * or the string content might be overwritten by a subsequent call to
     * getenv().  Since importing a module can performs the getenv() calls,
     * we need to save a copy of envar. */
    envar_obj = PyBytes_FromString(envar);
    if (envar_obj == NULL) {
        return NULL;
    }
    envar = PyBytes_AS_STRING(envar_obj);
    last_dot = strrchr(envar, '.');
    attrname = NULL;
    modulepath = NULL;

    if (last_dot == NULL) {
        /* The breakpoint is a built-in, e.g. PYTHONBREAKPOINT=int */
        modulepath = PyUnicode_FromString(BUILTINS_MOD);
        attrname = envar;
    }
    else {
        /* Split on the last dot; */
        modulepath = PyUnicode_FromStringAndSize(envar, last_dot - envar);
        attrname = last_dot + 1;
    }
    if (modulepath == NULL) {
        Py_DECREF(envar_obj);
        return NULL;
    }

    module = PyImport_Import(modulepath);
    Py_DECREF(modulepath);

    if (module == NULL) {
        goto error;
    }

    hook = PyObject_GetAttrString(module, attrname);
    Py_DECREF(module);

    if (hook == NULL) {
        goto error;
    }
    Py_DECREF(envar_obj);
    retval = PyObject_Call(hook, args, kwds);
    Py_DECREF(hook);
    return retval;

  error:
    /* If any of the imports went wrong, then warn and ignore. */
    PyErr_Clear();

    msg = PyBytes_FromFormat(
        "Ignoring unimportable $PYTHONBREAKPOINT: \"%s\"", envar);
    if (msg == NULL) {
        return NULL;
    }
    status = PyErr_Warn(PyExc_RuntimeWarning, PyBytes_AS_STRING(msg));
    Py_DECREF(msg);
    Py_DECREF(envar_obj);
    if (status < 0) {
        /* Printing the warning raised an exception. */
        return NULL;
    }
    /* The warning was (probably) issued. */
    Py_RETURN_NONE;
}

PyDoc_STRVAR(_breakpointhook_doc,
"breakpointhook(*args, **kws)\n"
"\n"
"This hook function is called by built-in breakpoint().\n"
);

static struct PyMethodDef methods[] = {
    {
        "breakpoint",
        (PyCFunction)_breakpoint,
        METH_VARARGS | METH_KEYWORDS,
        _breakpoint_doc
    },
    {
        "breakpointhook",
        (PyCFunction)_breakpointhook,
        METH_VARARGS | METH_KEYWORDS,
        _breakpointhook_doc
    },
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_future_breakpoint",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit__future_breakpoint(void) {
    return PyModule_Create(&module);
}
#else
PyMODINIT_FUNC init_future_breakpoint(void) {
    Py_InitModule3("_future_breakpoint", methods, NULL);
}
#endif
