cmake_minimum_required(VERSION 3.6 FATAL_ERROR)
project(libq)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)
option(BUILD_SHARED_LIBS "" ON)

add_library(config_headers INTERFACE)
target_include_directories(config_headers INTERFACE ${CMAKE_BINARY_DIR}/include)

add_custom_target(copy_headers)
add_custom_command(TARGET copy_headers PRE_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/../../include/pg_config.h.win32 ${CMAKE_BINARY_DIR}/include/pg_config.h
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/../../include/pg_config_ext.h.win32 ${CMAKE_BINARY_DIR}/include/pg_config_ext.h
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/../../include/port/win32.h ${CMAKE_BINARY_DIR}/include/pg_config_os.h
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_BINARY_DIR}/pg_config_paths.h ${CMAKE_BINARY_DIR}/include/pg_config_paths.h
  COMMENT "Copying config headers..."
)
add_dependencies(config_headers copy_headers)

add_library(pq
  fe-auth.c
  fe-connect.c
  fe-exec.c
  fe-lobj.c
  fe-misc.c
  fe-print.c
  fe-protocol2.c
  fe-protocol3.c
  fe-secure.c
  fe-secure-openssl.c
  libpq-events.c
  pqexpbuffer.c
  pthread-win32.c
  win32.c
  libpqdll.def
  ../../port/getaddrinfo.c
  ../../port/pgstrcasecmp.c
  ../../port/pqsignal.c
  ../../port/thread.c
  ../../port/inet_aton.c
  ../../port/crypt.c
  ../../port/noblock.c
  ../../port/chklocale.c
  ../../port/inet_net_ntop.c
  ../../backend/libpq/md5.c
  ../../backend/libpq/ip.c
  ../../backend/utils/mb/wchar.c
  ../../backend/utils/mb/encnames.c
  ../../port/snprintf.c
  ../../port/strlcpy.c
  ../../port/dirent.c
  ../../port/dirmod.c
  ../../port/pgsleep.c
  ../../port/open.c
  ../../port/system.c
  ../../port/win32error.c
  ../../port/win32setlocale.c
)

target_compile_options(pq PRIVATE $<$<C_COMPILER_ID:MSVC>:/wd4267 /wd4244>)

set_target_properties(pq PROPERTIES
  PREFIX "lib"
  IMPORT_PREFIX "lib"
  IMPORT_SUFFIX "dll.lib"
)

target_include_directories(pq PRIVATE
  ../../include
  ../../include/port/win32
  ../../include/port/win32_msvc
  ../../port
  ../../backend
  ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_definitions(pq PRIVATE
  $<$<PLATFORM_ID:Windows>:_CRT_SECURE_NO_WARNINGS _CRT_NONSTDC_NO_WARNINGS WIN32 _WINDOWS>
  USE_OPENSSL
  FRONTEND
)

target_link_libraries(pq PRIVATE
  config_headers
  CONAN_PKG::OpenSSL
  $<$<PLATFORM_ID:Windows>:kernel32.lib>
  $<$<PLATFORM_ID:Windows>:user32.lib>
  $<$<PLATFORM_ID:Windows>:advapi32.lib>
  $<$<PLATFORM_ID:Windows>:shell32.lib>
  $<$<PLATFORM_ID:Windows>:ws2_32.lib>
  $<$<PLATFORM_ID:Windows>:secur32.lib>
)
