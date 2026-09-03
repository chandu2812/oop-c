#include "../../include/services/AuthManager.hpp"
#include "../../include/services/PersistenceManager.hpp"

AuthManager::AuthManager(ElectionManager& e) : election(e) {}

bool AuthManager::registerUser(const std::string& id, const std::string& pwd, const std::string& name, int age) {
    if (age < 18) return false;
    
    auto& voters = election.getVoters();
    
    for (const auto& v : voters) {
        if (v.getUserId() == id) return false; // ID already exists
    }
    
    voters.push_back(Voter(id, pwd, name, age, false));
    PersistenceManager::saveVoters("data/voters.txt", voters);
    
    return true;
}

bool AuthManager::authenticate(const std::string& id, const std::string& pwd) {
    auto& voters = election.getVoters();
    
    for (const auto& v : voters) {
        if (v.getUserId() == id && v.verifyPassword(pwd)) return true;
    }
    
    return false;
}