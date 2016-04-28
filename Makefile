CUDA=/usr/local/cuda-6.5

NVCC=$(CUDA)/bin/nvcc
INCLUDES=-I$(CUDA)/include
NVFLAGS=
LDFLAGS=

SRC=GPUvectSum2.cu

OBJ=$(SRC:.cu=.o)

TARGET=main


%.cu.o: %.cu
	$(NVCC) -c $(INCLUDES) $(NVFLAGS) $< -o $@ 

$(TARGET): $(OBJ)
	$(NVCC) $(NVFLAGS) $(LDFLAGS) $(INCLUDES) -o $@ $^

all: $(TARGET)


#clean:
#	rm *.cu.o || true
#	rm $(TARGET) || true
