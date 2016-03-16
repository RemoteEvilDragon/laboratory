cmake_minimum_required (VERSION 2.8)
project (CMakeOpenCV)

set (CMakeOpenCV_VERSION_MAJOR 1)
set (CMakeOpenCV_VERSION_MINOR 0)

include_directories(/usr/local/include)

add_executable (CMakeOpenCV Smoothing.cpp)

find_library(OPENCV_CORE opencv_core)
find_library(OPENCV_IMGPROC opencv_imgproc)
find_library(OPENCV_IMGCODECS opencv_imgcodecs)
find_library(OPENCV_HIGHGUI opencv_highgui)
find_library(OPENCV_FEATURES2D opencv_features2d)

target_link_libraries (CMakeOpenCV ${OPENCV_CORE} ${OPENCV_IMGPROC} ${OPENCV_IMGCODECS} ${OPENCV_HIGHGUI} ${OPENCV_FEATURES2D})

#install (TARGETS CMakeOpenCV DESTINATION bin)
