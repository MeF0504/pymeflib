CC  = gcc
CFLAGS  = -lXpm -lX11
TARGET  = xpm_loader
SRCS    = xpm_loader.c
OBJS    = xpm.so
INCDIR  = -I/usr/X11R6/include
LIBDIR  = -L/usr/X11R6/lib
LIBS    = 
$(TARGET): $(SRCS)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBDIR) $(INCDIR)
	
$(OBJS): $(SRCS)
	$(CC) $(SRCS) -shared -o lib/$(OBJS) $(CFLAGS) -fPIC $(LIBDIR) $(INCDIR)
all: clean $(OBJS) $(TARGET)
clean:
	-rm -f lib/$(OBJS) $(TARGET) *.d
# vim: set noexpandtab
