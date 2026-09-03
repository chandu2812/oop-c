#pragma once
#include "User.hpp"
#include <sstream>

class Voter : public User {
private:
    int age;
    bool hasVoted;

public:
    Voter(std::string id, std::string pwd, std::string n, int a, bool voted = false);

    bool isEligible() const;
    bool getVoteStatus() const;
    void markVoted();
    
    std::string serialize() const;
    static Voter deserialize(const std::string& line);
};