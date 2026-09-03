#include "services/ElectionManager.hpp"
#include "services/PersistenceManager.hpp"

ElectionManager::ElectionManager() {
    candidates = PersistenceManager::loadCandidates("data/candidates.txt");
    
    if (candidates.empty()) {
        candidates.push_back(Candidate("C1", "M. K. Stalin (DMK)", 0));
        candidates.push_back(Candidate("C2", "Edappadi K. Palaniswami (AIADMK)", 0));
        candidates.push_back(Candidate("C3", "K. Annamalai (BJP)", 0));
        candidates.push_back(Candidate("C4", "Vijay (TVK)", 0));
        candidates.push_back(Candidate("C5", "Seeman (NTK)", 0));
        
        PersistenceManager::saveCandidates("data/candidates.txt", candidates);
    }
}
std::vector<Voter>& ElectionManager::getVoters() { 
    return voters; 
}

bool ElectionManager::castVote(const std::string& voterId, const std::string& candidateId) {
    std::lock_guard<std::mutex> lock(sysMutex);
    for (auto& v : voters) {
        if (v.getUserId() == voterId) {
            if (v.getVoteStatus()) return false; // Already voted
            
            for (auto& c : candidates) {
                if (c.getId() == candidateId) {
                    c.addVote();
                    v.markVoted();
                    PersistenceManager::saveVoters(voterFile, voters);
                    PersistenceManager::saveCandidates(candidateFile, candidates);
                    return true;
                }
            }
        }
    }
    return false;
}

std::vector<Candidate> ElectionManager::getResults() {
    std::lock_guard<std::mutex> lock(sysMutex);
    return candidates;
}