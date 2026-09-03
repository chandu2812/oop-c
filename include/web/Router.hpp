#pragma once
#include "external/httplib.h"
#include "services/AuthManager.hpp"
#include "services/ElectionManager.hpp"
#include <fstream>
#include <sstream>
#include <iostream>

class Router {
public:
    static void setupRoutes(httplib::Server& svr, AuthManager& auth, ElectionManager& election) {
        
        svr.set_mount_point("/", "./public");

        auto serveFile = [](const std::string& path, httplib::Response& res) {
            std::ifstream file(path);
            if (file.is_open()) {
                std::stringstream buffer;
                buffer << file.rdbuf();
                res.set_content(buffer.str(), "text/html");
            } else {
                std::cout << "Failed to find file at path: " << path << std::endl;
                res.status = 404;
                res.set_content("<h1>404 File Not Found</h1><p>Path: " + path + "</p>", "text/html");
            }
        };

        svr.Get("/", [serveFile](const httplib::Request&, httplib::Response& res) {
            serveFile("public/index.html", res);
        });

        svr.Get("/dashboard", [serveFile](const httplib::Request&, httplib::Response& res) {
            serveFile("public/dashboard.html", res);
        });

        svr.Get("/admin", [serveFile](const httplib::Request&, httplib::Response& res) {
            serveFile("public/admin.html", res);
        });

        svr.Post("/api/register", [&auth](const httplib::Request& req, httplib::Response& res) {
            auto getVal = [&req](const std::string& key) {
                size_t pos = req.body.find("\"" + key + "\":");
                if (pos == std::string::npos) return std::string("");
                pos = req.body.find(":", pos) + 1;
                while (req.body[pos] == ' ' || req.body[pos] == '"') pos++;
                size_t end = req.body.find_first_of("\",}", pos);
                return req.body.substr(pos, end - pos);
            };

            std::string id = getVal("voter_id");
            std::string pwd = getVal("password");
            std::string name = getVal("name");
            std::string ageStr = getVal("age");
            int age = ageStr.empty() ? 0 : std::stoi(ageStr);

            if (auth.registerUser(id, pwd, name, age)) {
                res.set_content("{\"status\":\"Success\"}", "application/json");
            } else {
                res.status = 400;
                res.set_content("{\"status\":\"Failed\"}", "application/json");
            }
        });

        svr.Post("/api/login", [&auth](const httplib::Request& req, httplib::Response& res) {
            auto getVal = [&req](const std::string& key) {
                size_t pos = req.body.find("\"" + key + "\":");
                if (pos == std::string::npos) return std::string("");
                pos = req.body.find(":", pos) + 1;
                while (req.body[pos] == ' ' || req.body[pos] == '"') pos++;
                size_t end = req.body.find_first_of("\",}", pos);
                return req.body.substr(pos, end - pos);
            };

            if (auth.authenticate(getVal("voter_id"), getVal("password"))) {
                res.set_content("{\"status\":\"Success\"}", "application/json");
            } else {
                res.status = 401;
                res.set_content("{\"status\":\"Failed\"}", "application/json");
            }
        });

        svr.Post("/api/vote", [&election](const httplib::Request& req, httplib::Response& res) {
            auto getVal = [&req](const std::string& key) {
                size_t pos = req.body.find("\"" + key + "\":");
                if (pos == std::string::npos) return std::string("");
                pos = req.body.find(":", pos) + 1;
                while (req.body[pos] == ' ' || req.body[pos] == '"') pos++;
                size_t end = req.body.find_first_of("\",}", pos);
                return req.body.substr(pos, end - pos);
            };

            if (election.castVote(getVal("voter_id"), getVal("candidate_id"))) {
                res.set_content("{\"status\":\"Success\"}", "application/json");
            } else {
                res.status = 403;
                res.set_content("{\"status\":\"Failed\"}", "application/json");
            }
        });

        svr.Get("/api/results", [&election](const httplib::Request&, httplib::Response& res) {
            auto candidates = election.getResults();
            std::string json = "[";
            for (size_t i = 0; i < candidates.size(); i++) {
                json += "{\"name\":\"" + candidates[i].getName() + "\",\"votes\":" + std::to_string(candidates[i].getVoteCount()) + "}";
                if (i + 1 < candidates.size()) json += ",";
            }
            json += "]";
            res.set_content(json, "application/json");
        });
    }
};