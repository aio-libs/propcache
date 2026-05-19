#ifndef ___HELPERS_H_H__
#define ___HELPERS_H_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "Python.h"


/* Fixes performance regression when generating cython code. */
/* SEE: https://github.com/aio-libs/propcache/issues/244 */
static PyObject*
under_cached_property_get(PyObject* wrapped, PyObject* name, PyObject* cache, PyObject* inst){
    PyObject* val;

    val = PyDict_GetItem(cache, name);
    if (val == NULL){
        val = PyObject_CallOneArg(wrapped, inst);
        if (val == NULL){
            return NULL;
        }
        if (PyDict_SetItem(cache, name, val) < 0){
            Py_CLEAR(val);
            return NULL;
        }
        // NOTE: We do not need to DECREF as we gained a ref already.
        // TODO: Validate if that is true...
    }
    Py_INCREF(val);
    return val;
}




#ifdef __cplusplus
}
#endif
#endif // ___HELPERS_H_H__
