#pragma once
#include <string>
#include <sstream>

class Candidate {
private:
    std::string candidateId;
    std::string candidateName;
    int voteCount;

public:
    Candidate(std::string id, std::string name, int votes = 0);

    std::string getId() const;
    std::string getName() const;
    int getVoteCount() const;
    void addVote();
    
    std::string serialize() const;
    static Candidate deserialize(const std::string& line);
};