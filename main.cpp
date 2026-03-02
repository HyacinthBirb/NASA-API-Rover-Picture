#include <iostream>
#include <string>

//Defining colors
#define RESET   "\033[0m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define BLUE    "\033[34m"

int main() {
    //Start program by requesting API key
    std::string api_key;
    std::cout << "API key: ";
    std::getline(std::cin,api_key);
    std::cout << RED << "Debug Key print: " << RESET << api_key << std::endl;

    //Then request wich rover
    std::cout << "What Rover do you want (Currently just curiosity supported)" << std::endl;
    std::string rover_name;
    std::cout << "Rover: ";
    std::getline(std::cin,rover_name);
    std::cout << RED << "Debug Rover Name "<< RESET << rover_name << std::endl;

    //Then if Mission Sol or earth date type
    std::string date_type;
    std::cout << "What Sol you want: ";
    std::getline (std::cin,date_type);

    //then wich cameras
    std::string camera_type;
    bool valid = false;

    while (!valid) {
        std::cout << "The following cameras are available: FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM" << std::endl;
        std::cout << "Please type your camera type: ";
        std::getline(std::cin,camera_type);

        if (camera_type == "FHAZ" ||
            camera_type != "RHAZ" ||
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
    // Do the function
    //Left here at 14:47
}