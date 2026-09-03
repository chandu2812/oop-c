#include "../../include/models/User.hpp"

User::User(std::string id, std::string pwd, std::string n)
    : userId(id), password(pwd), name(n) {}

std::string User::getUserId() const { return userId; }
std::string User::getName() const { return name; }
bool User::verifyPassword(const std::string& inputPwd) const { return password == inputPwd; }