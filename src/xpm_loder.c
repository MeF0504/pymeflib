#define PY_SSIZE_T_CLEAN

/* #include "Python.h" */
#include <stdio.h>
#include <X11/xpm.h>

int main(int argc, char **argv)
{
    int err;
    char **data;
    err = XpmReadFileToData(argv[1], &data);
    if( err ){
        fprintf(stderr,"%s: %s\n",argv[0],XpmGetErrorString(err));
        return 1;
    }
    printf("size: %lu, %lu, %lu\n", sizeof(data), sizeof(*data), sizeof(**data));
    printf("AA=%s=AA\n", data[9]);
}
