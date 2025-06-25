#ifndef __STATE_H__
#define __STATE_H__

#include <Python.h>
#ifdef __cplusplus
extern "C" {
#endif

/****************** Module State ****************/

typedef struct _mod_state {
    PyTypeObject* UnderCachedPropertyType;
    PyTypeObject* CachedPropertyType;
} mod_state;


// Multidict's library was a really good template so
// no need to revient the wheel here...

static inline mod_state* get_mod_state(PyObject* mod){
    mod_state* state = (mod_state*)PyModule_GetState(mod);
    assert(state != NULL);
    return state;
};

static inline mod_state *
get_mod_state_by_cls(PyTypeObject *cls)
{
    mod_state *state = (mod_state *)PyType_GetModuleState(cls);
    assert(state != NULL);
    return state;
}

#if PY_VERSION_HEX < 0x030b0000
PyObject *
PyType_GetModuleByDef(PyTypeObject *tp, PyModuleDef *def)
{
    PyModuleDef *mod_def;
    if (!PyType_HasFeature(tp, Py_TPFLAGS_HEAPTYPE)) {
        goto err;
    }
    PyObject *mod = NULL;

    mod = PyType_GetModule(tp);
    if (mod == NULL) {
        PyErr_Clear();
    } else {
        mod_def = PyModule_GetDef(mod);
        if (mod_def == def) {
            return mod;
        }
    }

    PyObject *mro = tp->tp_mro;
    assert(mro != NULL);
    assert(PyTuple_Check(mro));
    assert(PyTuple_GET_SIZE(mro) >= 1);
    assert(PyTuple_GET_ITEM(mro, 0) == (PyObject *)tp);

    Py_ssize_t n = PyTuple_GET_SIZE(mro);
    for (Py_ssize_t i = 1; i < n; i++) {
        PyObject *super = PyTuple_GET_ITEM(mro, i);
        if (!PyType_HasFeature((PyTypeObject *)super, Py_TPFLAGS_HEAPTYPE)) {
            continue;
        }
        mod = PyType_GetModule((PyTypeObject *)super);
        if (mod == NULL) {
            PyErr_Clear();
        } else {
            mod_def = PyModule_GetDef(mod);
            if (mod_def == def) {
                return mod;
            }
        }
    }

err:
    PyErr_Format(
        PyExc_TypeError,
        "PyType_GetModuleByDef: No superclass of '%s' has the given module",
        tp->tp_name);
    return NULL;
}
#endif


static PyModuleDef propcache_module;


#ifdef __cplusplus
}
#endif

#endif // __STATE_H__