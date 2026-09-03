#pragma once
#include "ElectionManager.hpp"
#include <string>

class AuthManager {
private:
    ElectionManager& election;

public:
    AuthManager(ElectionManager& e);
    
    bool registerUser(const std::string& id, const std::string& pwd, const std::string& name, int age);
    bool authenticate(const std::string& id, const std::string& pwd);
};