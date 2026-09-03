#include "../../include/services/PersistenceManager.hpp"
#include <fstream>
#include <iostream>

std::vector<Voter> PersistenceManager::loadVoters(const std::string& file) {
    std::vector<Voter> voters;
    std::ifstream in(file);
    std::string line;
    while (std::getline(in, line)) {
        if (!line.empty()) voters.push_back(Voter::deserialize(line));
    }
    return voters;
}

void PersistenceManager::saveVoters(const std::string& file, const std::vector<Voter>& voters) {
    std::ofstream out(file, std::ios::trunc);
    for (const auto& v : voters) out << v.serialize() << "\n";
}

std::vector<Candidate> PersistenceManager::loadCandidates(const std::string& file) {
    std::vector<Candidate> candidates;
    std::ifstream in(file);
    std::string line;
    while (std::getline(in, line)) {
        if (!line.empty()) candidates.push_back(Candidate::deserialize(line));
    }
    return candidates;
}

void PersistenceManager::saveCandidates(const std::string& file, const std::vector<Candidate>& candidates) {
    std::ofstream out(file, std::ios::trunc);
    for (const auto& c : candidates) out << c.serialize() << "\n";
}