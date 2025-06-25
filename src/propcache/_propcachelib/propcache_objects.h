#ifndef __PROPCACHE_OBJECTS_H__
#define __PROPCACHE_OBJECTS_H__
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

// IDK Yet...
// #if PY_VERSION_HEX >= 0x030c00f0
// #define MANAGED_WEAKREFS
// #endif



/****************** Propcache Objects ***************/

typedef struct _under_cached_property_object {
    PyObject_HEAD
    PyObject* wrapped;
    PyObject* name;
    PyObject* doc;
    // TODO: Maybe implement __isabstract__ for @abc.abstractmethod()
    // PyObject* isabstract;
} UnderCachedPropertyObject;


typedef struct _cached_property {
    PyObject_HEAD
    PyObject* func;
    PyObject* name;
    PyObject* doc;
    // TBD
    // PyObject* isabstract;
} CachedPropertyObject;


#ifdef __cplusplus
};
#endif

#endif // __PROPCACHE_OBJECTS_H__
