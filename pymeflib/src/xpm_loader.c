#include <stdio.h>
#include <X11/xpm.h>

int loader(char *filename, char ***data)
{
    int err;
    err = XpmReadFileToData(filename, data);
    if( err ){
        fprintf(stderr, "%s\n", XpmGetErrorString(err));
        return 1;
    }
    return 0;
}

int main(int argc, char **argv)
{
    int err;
    char **data;
    err = loader(argv[1], &data);

    printf("info: [%s]\n", data[0]);
}
