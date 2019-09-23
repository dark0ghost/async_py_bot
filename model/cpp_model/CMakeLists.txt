find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
target_link_libraries(<your exe or lib> ${PYTHON_LIBRARIES})
