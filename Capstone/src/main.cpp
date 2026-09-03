#include "../include/external/httplib.h"
#include "../include/services/ElectionManager.hpp"
#include "../include/services/AuthManager.hpp"
#include "../include/web/Router.hpp"
#include <iostream>
#include <cstdlib>

int main() {
    system("if not exist data mkdir data");
    
    httplib::Server svr;
    ElectionManager election;
    AuthManager auth(election);

    Router::setupRoutes(svr, auth, election);

    std::cout << "Server starting at http://localhost:18080\n";
    svr.listen("0.0.0.0", 18080);
}