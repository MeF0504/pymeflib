# vim: set noexpandtab
#  https://zenn.dev/yagiyuki/articles/b5545c3b546bbeb662bf
CC  = gcc
CFLAGS  = -lXaw -lXmu -lXt -lXpm -lX11
TARGET  = xpm_loader
SRCS    = xpm_loader.c
OBJS    = xpm.so
INCDIR  = -I/usr/X11R6/include
LIBDIR  = -L/usr/X11R6/lib
LIBS    = 
$(TARGET): $(SRCS)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBDIR) $(INCDIR)
	
$(OBJS): $(SRCS)
	$(CC) $(SRCS) -shared -o $(OBJS) $(CFLAGS) $(LIBDIR) $(INCDIR)
all: clean $(OBJS) $(TARGET)
clean:
	-rm -f $(OBJS) $(TARGET) *.d
