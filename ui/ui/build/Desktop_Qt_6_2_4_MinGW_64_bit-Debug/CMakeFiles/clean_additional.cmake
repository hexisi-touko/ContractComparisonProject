# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\ui_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\ui_autogen.dir\\ParseCache.txt"
  "ui_autogen"
  )
endif()
