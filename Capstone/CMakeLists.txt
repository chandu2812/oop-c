cmake_minimum_required(VERSION 3.14)
project(SecureVotingSystem CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include include/external)

set(SOURCES
    src/main.cpp
    src/models/User.cpp
    src/models/Voter.cpp
    src/models/Candidate.cpp
    src/services/PersistenceManager.cpp
    src/services/ElectionManager.cpp
    src/services/AuthManager.cpp
    src/web/Router.cpp
)

add_executable(VotingServer ${SOURCES})

find_package(Threads REQUIRED)
target_link_libraries(VotingServer PRIVATE Threads::Threads ws2_32 wsock32)