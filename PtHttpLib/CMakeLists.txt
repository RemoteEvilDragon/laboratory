cmake_minimum_required (VERSION 2.8)
project (PtHttp)

set(SYSTEM_INCLUDE_PATH /usr/include/)
include_directories(${SYSTEM_INCLUDE_PATH})

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")

add_library(PtHttp STATIC HttpClientDef.cpp)

#add_executable (PtHttp HttpClientDef.cpp)

find_library(BOOST_COROTINE  NAMES boost_coroutine PATHS /usr/lib/x86_64-linux-gnu/)
find_library(BOOST_SYSTEM  NAMES boost_system PATHS /usr/lib/x86_64-linux-gnu/)
find_library(BOOST_THREAD  NAMES boost_thread PATHS /usr/lib/x86_64-linux-gnu/)
find_library(CPP_THREAD  NAMES pthread PATHS /usr/lib/x86_64-linux-gnu/)
find_library(BOOST_CONTEXT  NAMES boost_context PATHS /usr/lib/x86_64-linux-gnu/)


target_link_libraries(PtHttp ${CPP_THREAD})

target_link_libraries(PtHttp ${BOOST_THREAD})

target_link_libraries(PtHttp ${BOOST_COROTINE})
target_link_libraries(PtHttp ${BOOST_CONTEXT})

target_link_libraries(PtHttp ${BOOST_SYSTEM})
