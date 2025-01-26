#include <stdio.h>
#include <X11/xpm.h>

int loader(char *filename, char ***data, int *width, int *height)
{
    int err;
    int w = 0;
    int h = 0;
    err = XpmReadFileToData(filename, data);
    if( err ){
        fprintf(stderr,"%s\n", XpmGetErrorString(err));
        return 1;
    }
    return 0;
}

int main(int argc, char **argv)
{
    int err;
    char **data;
    int width = 0;
    int height = 0;
    err = loader(argv[1], &data, &width, &height);
    height = 13;

    /* printf("size: %lu, %lu, %lu\n", sizeof(data), sizeof(data[0]), sizeof(data[0][0])); */
    /* printf("len: %lu\n", strlen(*data[0])); */
    printf("AA=%s=AA\n", data[0]);
    int i;
    for (i = 0; i < height; i++)
    {
        printf("BB=~%s=~\n", data[i]);
    }
}

int add(int x, int y)
{
    return x+y;
}

void out(const char* adrs, const char* name)
{
    printf("Hello I am %s at %s.\n", name, adrs);
}
