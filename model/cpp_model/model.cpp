#ifndef _MYNN_H_
#define _MYNN_H_
#include <Python.h>
#include <math.h>
#include <vector>
#include <algorithm>
#include "neuron.h"
#include <boost/python.hpp>
#endif _MYNN_H_

using namespace std;

BOOST_PYTHON_MODULE(hello_ext)
{
    using namespace boost::python;
    def("greet", greet);
}


