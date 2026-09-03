#include "../../include/models/Candidate.hpp"

Candidate::Candidate(std::string id, std::string name, int votes)
    : candidateId(id), candidateName(name), voteCount(votes) {}

std::string Candidate::getId() const { return candidateId; }
std::string Candidate::getName() const { return candidateName; }
int Candidate::getVoteCount() const { return voteCount; }
void Candidate::addVote() { voteCount++; }

std::string Candidate::serialize() const {
    return candidateId + "," + candidateName + "," + std::to_string(voteCount);
}

Candidate Candidate::deserialize(const std::string& line) {
    std::stringstream ss(line);
    std::string id, name, countStr;
    std::getline(ss, id, ',');
    std::getline(ss, name, ',');
    std::getline(ss, countStr, ',');
    return Candidate(id, name, std::stoi(countStr));
}