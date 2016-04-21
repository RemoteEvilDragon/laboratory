cmake_minimum_required (VERSION 2.8)
project (CMakeAthen)

#version number
set (CMakeAthen_VERSION_MAJOR 1)
set (CMakeAthen_VERSION_MINOR 0)

set(OPENCV_PATH /usr/local/opt/opencv3/include)

include_directories(${OPENCV_PATH})

add_executable (CMakeAthen Smoothing.cpp)


#set(OPENCV_LIB_PATH /usr/local/opt/opencv3/lib)
#include_directories(${OPENCV_LIB_PATH})


find_library(OPENCV_FEATURES2D  NAMES opencv_features2d PATHS /usr/local/opt/opencv3/lib)
find_library(OPENCV_IMGPROC  NAMES opencv_imgproc PATHS /usr/local/opt/opencv3/lib)
find_library(OPENCV_HIGHGUI  NAMES opencv_highgui PATHS /usr/local/opt/opencv3/lib)
find_library(OPENCV_IMGCODECS NAMES opencv_imgcodecs PATHS /usr/local/opt/opencv3/lib)
find_library(OPENCV_CORE  NAMES opencv_core PATHS /usr/local/opt/opencv3/lib)

target_link_libraries(CMakeAthen ${OPENCV_IMGCODECS})
target_link_libraries(CMakeAthen ${OPENCV_FEATURES2D})
target_link_libraries(CMakeAthen ${OPENCV_IMGPROC})
target_link_libraries(CMakeAthen ${OPENCV_HIGHGUI})
target_link_libraries(CMakeAthen ${OPENCV_CORE})


install (TARGETS CMakeAthen DESTINATION bin)
