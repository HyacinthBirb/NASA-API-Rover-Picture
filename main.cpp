#include <iostream>
#include <string>
#include <curl/curl.h>
#include "json.hpp"
using json = nlohmann::json;

// Project was left at 12:40 march 3 with these issues:
//Missing semicolons — using json = nlohmann::json and one more nearby
//URL malformed — missing / characters between segments and = after ?sol
//response undeclared — needs to be a std::string declared before the curl block
//Callback mismatch — your callback uses FILE* but first curl call needs std::string*
//File open/close in wrong order — fopen and fclose should wrap the second curl call, not the first
//JSON parsing — the lines after parsing aren't doing anything useful yet

//Defining colors
#define RESET   "\033[0m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define BLUE    "\033[34m"

// Call Back for the curl
size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string* output) {
    output->append((char*)contents, size * nmemb);
    return size * nmemb;
}

// Separate file-writing callback for downloading images
size_t WriteFileCallback(void *contents, size_t size, size_t nmemb, FILE* file) {
    return fwrite(contents, size, nmemb, file);
}

int main() {
    //Start program by requesting API key
    std::string api_key;
    std::cout << "API key: ";
    std::getline(std::cin, api_key);
    std::cout << RED << "Debug Key print: " << RESET << api_key << std::endl;

    //Then request which rover
    std::cout << "What Rover do you want (Currently just curiosity supported)" << std::endl;
    std::string rover_name;
    std::cout << "Rover: ";
    std::getline(std::cin, rover_name);
    std::cout << RED << "Debug Rover Name " << RESET << rover_name << std::endl;

    //Then if Mission Sol or earth date type
    std::string date_type;
    std::cout << "What Sol you want: ";
    std::getline(std::cin, date_type);

    //then which cameras
    std::string camera_type;
    bool valid = false;

    while (!valid) {
        std::cout << "The following cameras are available: FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM" << std::endl;
        std::cout << "Please type your camera type: ";
        std::getline(std::cin, camera_type);

        if (camera_type == "FHAZ" ||
            camera_type == "RHAZ" ||
            camera_type == "MAST" ||
            camera_type == "CHEMCAM" ||
            camera_type == "MAHLI" ||
            camera_type == "MARDI" ||
            camera_type == "NAVCAM") {
            valid = true;
        }
        else {
            std::cout << "Invalid Camera type, try again \n\n" << std::endl;
        }
    }

    CURL* curl = curl_easy_init();
    if (curl) {
        std::string url = "https://api.nasa.gov/mars-photos/api/v1/rovers/" + rover_name + "/photos?sol=" + date_type + "&camera=" + camera_type + "&api_key=" + api_key;

        std::string response;

        // Configure first curl call to fetch JSON metadata
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        json data = json::parse(response);

        int photo_index = 0;
        for (auto& photo : data["photos"]) {
            std::string img_url = photo["img_src"];
            std::cout << GREEN << "Downloading: " << RESET << img_url << std::endl;

            std::string filename = "API_Photo/photo_" + std::to_string(photo_index++) + ".jpg";
            FILE* file = fopen(filename.c_str(), "wb");
            if (file) {
                curl_easy_setopt(curl, CURLOPT_URL, img_url.c_str());
                curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteFileCallback);
                curl_easy_setopt(curl, CURLOPT_WRITEDATA, file);
                curl_easy_perform(curl);
                fclose(file);
            } else {
                std::cerr << RED << "Failed to open file: " << filename << RESET << std::endl;
            }
        }

        curl_easy_cleanup(curl);
    }

    return 0;
}