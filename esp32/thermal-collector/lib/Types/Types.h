#ifndef TYPES_H
#define TYPES_H

template <typename T>
struct Result
{
    T *value; // Pointer to the object of type T
    bool ok;  // Indicates whether the operation was successful

    Result(T *val) : value(val), ok(true) {}
    Result() : value(nullptr), ok(false) {}
};

#endif