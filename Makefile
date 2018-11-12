LecroyData_C.so: LecroyData.C  LecroyData.h
	echo ".L LecroyData.C++" | root -l

clean:
	rm -f *pcm *.d *.so *# *~
