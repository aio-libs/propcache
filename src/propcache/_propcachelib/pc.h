#ifndef __PC_H__
#define __PC_H__

/* PC is short for propcache in this case... */

#include "propcache_objects.h"
#include "pythoncapi_compat.h"
#include "state.h"
#ifdef __cplusplus
extern "C" {
#endif


/************* under_cached_property / cached_property methods ********************/

/* OTHER NOTES: 
 * - Made sense to not use -1 to express failure and rather handle everything in 
 *  True/False Fashion don't see the day this gets requested to be wrapped as a c-api
 *  module but incase requested this is why true/false is utilized
 */

static inline PyObject*
__propcache_get_func_doc(PyObject* func){
    PyObject* result;
    PyObject_GetOptionalAttrString(func, "__doc__", &result);
    if (result == NULL){
        Py_RETURN_NONE;
    }
    Py_INCREF(result);
    return result;
}

static inline int
__propcache_set_func_doc(PyObject* func, PyObject* doc){
    return PyObject_SetAttrString(func, "__doc__", doc);
}

// cached / under_cached use the same caching mechanism
// so combining the two under an inlined funciton made 
// perfect sense...

static inline PyObject*
__propcache_get_value(PyObject* name, PyObject* func, PyObject* inst, const char* attr_name){
    PyObject* cache = PyObject_GetAttrString(inst, attr_name);
    if (cache == NULL){
        return NULL;
    }
    PyObject* val = PyDict_GetItem(cache, name);
    if (val == NULL){
        val = PyObject_CallOneArg(func, inst);
        if (PyDict_SetItem(cache, name, val) < 0){
            return NULL;
        }
    } else {
        Py_INCREF(val);
    }
    // TODO: Try Looking into returning val with Py_NewRef 
    return val;
}


/************* under_cached_property methods ********************/

static inline int
uc_prop_init(UnderCachedPropertyObject* self, PyObject* wrapped){
    PyObject* name = PyObject_GetAttrString(wrapped, "__name__");
    if (name == NULL){
        return 0;
    }
    if (!PyCallable_Check(wrapped)){
        PyErr_Format(
            PyExc_TypeError,
            "wrapped method named %R must be callable", 
            name
        );
        return 0;
    }
    self->name = name;
    self->wrapped = wrapped;
    self->doc = NULL;
    return 1;
}




static inline PyObject* 
uc_prop__get__(UnderCachedPropertyObject* self, PyObject* inst){
    if (inst == NULL || Py_IsNone(inst)){
        return (PyObject*)self;
    }
    return __propcache_get_value(self->name, self->wrapped, inst, "_cache");
}




/************************ cached_property *********************** */

static inline void
c_prop_init(CachedPropertyObject* self, PyObject* func){
    /* In the old cython version we used None This time 
    We can now utilize NULL to speedup checking in __set_name__ */
    self->func = func;
    self->name = NULL;
}


static inline int
c_prop__set_name__(CachedPropertyObject* self, PyObject* name){
    if (self->name == NULL){
        self->name = name;
        return 1;
    } else {
        switch (PyObject_RichCompareBool(self->name, name, Py_EQ)){
            case 1: {
                /* Success */
                return 1;
            }
            case 0: {
                /* Error */
                PyErr_Format(
                    PyExc_TypeError,
                    "Cannot assign the same cached_property to two different names %R and %R",
                    self->name, 
                    name
                );
                return 0;
            }
            
            default : {
                /* Error but likely for a different reason */
                return 0;
            }
        }
    }
}

static inline PyObject* 
c_prop__get__(CachedPropertyObject* self, PyObject* inst){
    if (inst == NULL || (Py_IsNone(inst))){
        return (PyObject*)self;
    }
    if (self->name == NULL || (Py_IsNone(self->name))) {
        PyErr_SetString(
            PyExc_TypeError,
            "Cannot use cached_property instance"
            " without calling __set_name__ on it."
        );
        return NULL;
    }
    /* Incase object was using __slots__ instead of __dict__ 
     * PyObject_GetAttrString will catch it and throw an error */
    return __propcache_get_value(self->name, self->func, inst, "__dict__");
}


#ifdef __cplusplus
}
#endif


#endif // __PC_H__