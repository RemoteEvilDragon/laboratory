cmake_minimum_required (VERSION 2.8)
project (curlTest)

set(SYSTEM_INCLUDE_PATH /usr/include/)

include_directories(${SYSTEM_INCLUDE_PATH})

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")

#add_library(PtHttp STATIC HttpClientDef.cpp)

add_executable (curlTest test.cpp)

find_library(CURL_LIB NAMES curl PATHS ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(curlTest ${CURL_LIB})
