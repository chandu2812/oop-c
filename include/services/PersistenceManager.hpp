#pragma once
#include "../models/Voter.hpp"
#include "../models/Candidate.hpp"
#include <vector>
#include <string>

class PersistenceManager {
public:
    static std::vector<Voter> loadVoters(const std::string& file);
    static void saveVoters(const std::string& file, const std::vector<Voter>& voters);
    
    static std::vector<Candidate> loadCandidates(const std::string& file);
    static void saveCandidates(const std::string& file, const std::vector<Candidate>& candidates);
};