#include "../../include/models/Voter.hpp"

Voter::Voter(std::string id, std::string pwd, std::string n, int a, bool voted)
    : User(id, pwd, n), age(a), hasVoted(voted) {}

bool Voter::isEligible() const { return age >= 18; }
bool Voter::getVoteStatus() const { return hasVoted; }
void Voter::markVoted() { hasVoted = true; }

std::string Voter::serialize() const {
    return userId + "," + password + "," + name + "," + std::to_string(age) + "," + (hasVoted ? "1" : "0");
}

Voter Voter::deserialize(const std::string& line) {
    std::stringstream ss(line);
    std::string id, pwd, name, ageStr, votedStr;
    std::getline(ss, id, ',');
    std::getline(ss, pwd, ',');
    std::getline(ss, name, ',');
    std::getline(ss, ageStr, ',');
    std::getline(ss, votedStr, ',');
    return Voter(id, pwd, name, std::stoi(ageStr), votedStr == "1");
}