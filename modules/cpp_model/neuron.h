#include <math.h>
#include <vector>

class neuron {
public:
    neuron();
    vector<int> weights;
    int compute_sum (vector <int> &input);
};

class layer
{
public:
    layer();
    vector <neuron> nrns;
    vector<int> compute_layer (vector <int> &input);
};

