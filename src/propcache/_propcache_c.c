/* _propcache_c.c 
 *
 * A replacement of the cython _helper_c.pyx with a few more optimized
 * parts for better care and speed...
 */


#include <Python.h>

#include "_propcachelib/pc.h"
#include "_propcachelib/propcache_objects.h"
#include "_propcachelib/pythoncapi_compat.h"
#include "_propcachelib/state.h"




/****************** UnderCachedPropertyObject Methods ******************/


static int
under_cached_property_tp_init(UnderCachedPropertyObject *self, PyObject* args, PyObject* kwds){
    static char *kwlist[] = {"wrapped", NULL};
    PyObject* wrapped = NULL;
    if (!PyArg_ParseTupleAndKeywords( args, kwds, "|O", kwlist, wrapped)){
        return -1;
    }
    return uc_prop_init(self, wrapped);
}

static PyObject*
under_cached_property_get__doc__(UnderCachedPropertyObject* self,  PyObject *Py_UNUSED(ignored)){
    if (self->doc == NULL){
        self->doc = __propcache_get_func_doc(self->wrapped);
    }
    return self->doc;
};

static PyObject*
under_cached_property_set__doc__(UnderCachedPropertyObject* self,  PyObject* new_doc){
    self->doc = new_doc;
    return new_doc;
};


static PyObject* 
under_cached_property__get__(UnderCachedPropertyObject* self, PyObject* inst, void* Py_UNUSED(owner)){
    return uc_prop__get__(self, inst);
}

/* under_cached_property is immutable */

static PyObject* 
under_cached_property__set__(UnderCachedPropertyObject* self, void* Py_UNUSED(inst), void* Py_UNUSED(owner)){
    PyErr_SetString(PyExc_AttributeError, "cached property is read-only");
    return NULL;
};





static int
under_cached_property_tp_traverse(UnderCachedPropertyObject *self, visitproc visit, void *arg){
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->wrapped);
    Py_VISIT(self->name);
    Py_VISIT(self->doc);
    return 0;
}

static int
under_cached_property_clear(UnderCachedPropertyObject *self)
{
    Py_CLEAR(self->wrapped);
    Py_CLEAR(self->name);
    Py_CLEAR(self->doc);
    return 0;
}

/************ UnderCachedPropertyObject Type Information ***************/

// TODO: Maybe consider adding __isabstractmethod__ & __name__ using PyGetSetDef

static PyGetSetDef under_cached_property_getsetlist[] = {
    {"__doc__", under_cached_property_get__doc__, under_cached_property_set__doc__, NULL, NULL},
    {0, 0, 0, 0, 0}
};


PyDoc_STRVAR(
    UnderCachedProperty_Doc,
    "Use as a class method decorator.  It operates almost exactly like"
    "the Python `@property` decorator, but it puts the result of the"
    "method it decorates into the instance dict after the first call,"
    "effectively replacing the function it decorates with an instance"
    "variable.  It is, in Python parlance, a data descriptor.");



static PyMemberDef under_cached_property_members[] = {
    {
        "name",
        Py_T_OBJECT_EX,
        offsetof(UnderCachedPropertyObject, name),
        Py_READONLY
    },
    {
        "wrapped",
        Py_T_OBJECT_EX,
        offsetof(UnderCachedPropertyObject, wrapped),
        Py_READONLY,
    },
    {NULL} /* Sentinel */
}; 

static PyMethodDef under_cached_property_methods[] = {
    {"__class_getitem__", (PyCFunction)Py_GenericAlias, METH_O | METH_CLASS,NULL},
    {NULL}
};


static PyType_Slot under_cached_property_type_slots[] = {
    {Py_tp_descr_get, under_cached_property__get__},
    {Py_tp_descr_set, under_cached_property__set__},
    {Py_tp_init, under_cached_property_tp_init},
    {Py_tp_traverse, under_cached_property_tp_traverse},
    {Py_tp_doc, UnderCachedProperty_Doc},
    {Py_tp_members, under_cached_property_members},
    {Py_tp_clear, under_cached_property_clear},
    {Py_tp_new, PyType_GenericNew},
    {Py_tp_del, PyObject_GC_Del},
    {Py_tp_methods, under_cached_property_methods},
    {Py_tp_getset, under_cached_property_getsetlist},
    {0, NULL}
};

static PyType_Spec UnderCachedPropertySpec = {
    .basicsize = sizeof(UnderCachedPropertyObject),
    .flags = Py_TPFLAGS_DEFAULT|Py_TPFLAGS_HAVE_VERSION_TAG|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_HAVE_GC,
    .itemsize = 0,
    .name = "propcache._propcache_c.under_cached_property",
    .slots = under_cached_property_type_slots
};



/*************************** CachedPropertyObject **************************/
/* An optimized version of functool's cached-property */
/* For more info on how this object works it's recommended to see 
 * Either functool's version or _propcache/pc.h */


static int
cached_property_tp_init(CachedPropertyObject *self, PyObject* args, PyObject* kwds){
    static char *kwlist[] = {"func", NULL};
    PyObject* func = NULL;
    if (!PyArg_ParseTupleAndKeywords( args, kwds, "|O", kwlist, func)){
        return -1;
    }
    c_prop_init(self, func);
    return 0;
}

static int
cached_property__set_name__(CachedPropertyObject* self, PyObject *const *args, Py_ssize_t nargs){
    if (nargs < 2){
        PyErr_Format(PyExc_TypeError, "__set_name__ requires 2 positional arguments not %zu", nargs);
    }
    return c_prop__set_name__(self, args[0]);
}

static PyObject* 
cached_property__get__(CachedPropertyObject* self, PyObject* inst, void* Py_UNUSED(owner)){
    return c_prop__get__(self, inst);
};


static PyObject*
cached_property_get__doc__(CachedPropertyObject* self,  void *Py_UNUSED(ignored)){
    if (self->doc == NULL){
        self->doc = __propcache_get_func_doc(self->func);
    }
    return self->doc;
};

static PyObject*
cached_property_set__doc__(CachedPropertyObject* self,  PyObject* new_doc){
    self->doc = new_doc;
    return new_doc;
};


static int
cached_property_tp_traverse(CachedPropertyObject *self, visitproc visit, void *arg){
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->func);
    Py_VISIT(self->name);
    Py_VISIT(self->doc);
    return 0;
}


static int
cached_property_tp_clear(CachedPropertyObject *self, visitproc visit, void *arg){
    Py_CLEAR(self->func);
    Py_CLEAR(self->name);
    Py_CLEAR(self->doc);
    return 0;
}



/************ CachedPropertyObject Type Information ***************/

PyDoc_STRVAR(
    CachedProperty_Doc,
    "Use as a class method decorator.  It operates almost exactly like"
    "the Python `@property` decorator, but it puts the result of the"
    "method it decorates into the instance dict after the first call,"
    "effectively replacing the function it decorates with an instance"
    "variable.  It is, in Python parlance, a data descriptor."
);


static PyGetSetDef cached_property_getsetlist[] = {
    {"__doc__", cached_property_get__doc__, cached_property_set__doc__, NULL, NULL},
    {0, 0, 0, 0, 0}
};

static PyMemberDef cached_property_members[] = {
    {
        "name",
        Py_T_OBJECT_EX,
        offsetof(CachedPropertyObject, name),
        Py_READONLY
    },
    {
        "func",
        Py_T_OBJECT_EX,
        offsetof(CachedPropertyObject, func),
        Py_READONLY,
    },
    {NULL} /* Sentinel */
};

static PyMethodDef cached_property_methods[] = {
    {"__class_getitem__", (PyCFunction)Py_GenericAlias, METH_O | METH_CLASS,NULL},
    {"__set_name__", (PyCFunction)cached_property__set_name__, METH_FASTCALL, NULL},
    {NULL}
};


static PyType_Slot cached_property_type_slots[] = {
    {Py_tp_descr_get, cached_property__get__},
    // {Py_tp_descr_set, cached_property__set__}, <- TBD
    {Py_tp_init, under_cached_property_tp_init},
    {Py_tp_traverse, under_cached_property_tp_traverse},
    {Py_tp_doc, (char*)CachedProperty_Doc},
    {Py_tp_members, cached_property_members},
    {Py_tp_clear, cached_property_tp_clear},
    {Py_tp_new, PyType_GenericNew},
    {Py_tp_del, PyObject_GC_Del},
    {Py_tp_methods, cached_property_methods},
    {Py_tp_getset, cached_property_getsetlist},
    {0, NULL}
};



static PyType_Spec CachedPropertySpec = {
    .basicsize = sizeof(CachedPropertyObject),
    .flags = Py_TPFLAGS_DEFAULT|Py_TPFLAGS_HAVE_VERSION_TAG|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_HAVE_GC,
    .itemsize = 0,
    .name = "propcache._propcache_c.cached_property",
    .slots = cached_property_type_slots
};


static int
module_exec(PyObject *mod)
{
    mod_state *state = get_mod_state(mod);
    state->CachedPropertyType = (PyTypeObject*)PyType_FromModuleAndSpec(mod, &CachedPropertySpec, NULL);;
    if (state->CachedPropertyType == NULL){
        return -1;
    }
    if (PyModule_AddType(mod, state->CachedPropertyType) < 0){
        return -1;
    };

    state->UnderCachedPropertyType = (PyTypeObject*)PyType_FromModuleAndSpec(mod, &UnderCachedPropertySpec, NULL);
    if (state->UnderCachedPropertyType == NULL){
        Py_CLEAR(state->CachedPropertyType);
        return -1;
    }
    if (PyModule_AddType(mod, state->UnderCachedPropertyType) < 0){
        return -1;
    };
    return 0;
}


static int
module_traverse(PyObject *mod, visitproc visit, void *arg)
{
    mod_state *state = get_mod_state(mod);
    Py_VISIT(state->CachedPropertyType);
    Py_VISIT(state->UnderCachedPropertyType);
    return 0;
}

static int
module_clear(PyObject *mod)
{
    mod_state *state = get_mod_state(mod);
    Py_CLEAR(state->CachedPropertyType);
    Py_CLEAR(state->UnderCachedPropertyType);
    return 0;
}

static void
module_free(void *mod)
{
    (void)module_clear((PyObject *)mod);
}


static struct PyModuleDef_Slot module_slots[] = {
    {Py_mod_exec, module_exec},
#if PY_VERSION_HEX >= 0x030c00f0
    {Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#endif
#if PY_VERSION_HEX >= 0x030d00f0
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0, NULL},
};



static PyModuleDef propcache_c_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_propcache_c",
    .m_size = sizeof(mod_state),
    .m_slots = module_slots,
    .m_traverse = module_traverse,
    .m_clear = module_clear,
    .m_free = (freefunc)module_free, 
};

PyMODINIT_FUNC
PyInit__propcache_c(void)
{
    return PyModuleDef_Init(&propcache_c_module);
}