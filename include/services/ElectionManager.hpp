#pragma once
#include "../models/Voter.hpp"
#include "../models/Candidate.hpp"
#include <vector>
#include <string>
#include <mutex>

class ElectionManager {
private:
    std::vector<Voter> voters;
    std::vector<Candidate> candidates;
    std::mutex sysMutex;
    const std::string voterFile = "data/voters.txt";
    const std::string candidateFile = "data/candidates.txt";

public:
    ElectionManager();
    
    std::vector<Voter>& getVoters();
    bool castVote(const std::string& voterId, const std::string& candidateId);
    std::vector<Candidate> getResults();
};