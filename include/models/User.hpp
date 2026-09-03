#pragma once
#include <string>

class User {
protected:
    std::string userId;
    std::string password;
    std::string name;

public:
    User(std::string id, std::string pwd, std::string n);
    virtual ~User() = default;

    std::string getUserId() const;
    std::string getName() const;
    bool verifyPassword(const std::string& inputPwd) const;
};