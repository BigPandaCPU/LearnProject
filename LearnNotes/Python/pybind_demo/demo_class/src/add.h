#include<pybind11/pybind11.h>
namespace py = pybind11;

int add(int i, int j);
void swap(int *a, int *b);
struct Pet
{
    Pet(const std::string &name):name(name) {}
    void setName(const std::string &name_){ name = name_; }
    const std::string &getName() const { return name; }
    std::string name;
};

struct Dog:Pet
{
    Dog(const std::string &name):Pet(name) { }
    std::string bark() const { return name; }
};