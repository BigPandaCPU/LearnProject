#include"add.h"
int add(int i, int j)
{
	return (i+j);
}

void swap(int *a, int *b)
{
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}