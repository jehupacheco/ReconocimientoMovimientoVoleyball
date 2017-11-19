CXX = g++ -std=c++11 
OBJ = main.o
CXX_FLAGS =  -Wall -O2 -g -DNDEBUG `pkg-config --cflags opencv`
CXX_DEFINES = -DEXAMPLES_WITH_OPENGL_SUPPORT=1 -DRESOURCES_INC
CXX_INCLUDES = \
	-I/home/front-team/libfreenect2/include \
	-I/home/front-team/libfreenect2/include/internal \
	-I/home/front-team/libfreenect2/build \
	-I/home/front-team/libfreenect2/src/tinythread \
	-I/usr/include/libusb-1.0 \
	-I/usr/include/libdrm \
	-I/usr/include/openni2 \
	-I/home/front-team/Downloads/NiTE-Linux-x64-2.2/Include

CXX_LIBS = \
	-rdynamic /home/front-team/freenect2/lib/libfreenect2.so.0.2.0 \
	-rdynamic ./libNiTE2.so \
	-lglfw \
	-lGL \
	-lusb-1.0 \
	-lpthread \
	-lva-drm \
	-lva \
	-ljpeg /usr/lib/x86_64-linux-gnu/libturbojpeg.so.0 \
	-lglfw \
	-lGL \
	-Wl,-rpath,/home/front-team/libfreenect2/build/lib \
	`pkg-config --libs opencv` \
	-L/home/front-team/Downloads/NiTE-Linux-x64-2.2/Redist \
	-lOpenNI2 \
	-lNiTE2

%.o: %.cpp $(DEPS)
	$(CXX) -c -o $@ $< $(CXX_FLAGS) $(CXX_DEFINES) $(CXX_INCLUDES)

main: $(OBJ)
	$(CXX) -o $@ $^ $(CXX_INCLUDES) $(CXX_LIBS)

clean:
	rm -rf *.o
