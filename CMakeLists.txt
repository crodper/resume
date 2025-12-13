cmake_minimum_required(VERSION 3.20)

project(resume NONE)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(RESUME_YAML ${CMAKE_SOURCE_DIR}/data/resume.yaml)
set(TEMPLATE     ${CMAKE_SOURCE_DIR}/templates/resume.tex.j2)
set(OUTPUT_DIR   ${CMAKE_BINARY_DIR})
set(OUTPUT_PDF   ${OUTPUT_DIR}/resume.pdf)

add_custom_command(
    OUTPUT ${OUTPUT_PDF}
    COMMAND ${Python3_EXECUTABLE}
            ${CMAKE_SOURCE_DIR}/scripts/build_resume.py
            --data ${RESUME_YAML}
            --template ${TEMPLATE}
            --out ${OUTPUT_DIR}
    DEPENDS
        ${RESUME_YAML}
        ${TEMPLATE}
        ${CMAKE_SOURCE_DIR}/scripts/build_resume.py
    COMMENT "Building resume PDF"
    VERBATIM
)

add_custom_target(resume ALL DEPENDS ${OUTPUT_PDF})
