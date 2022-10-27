
#include <string>
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;

const char* src = "E:\\amadeo\\SwordKing\\";
const char* dst = "C:\\Users\\amade\\Documents\\Unreal Projects\\SwordKing503\\";
#include <stdlib.h>
#include <iostream>
#include <ctime>
#include <sys/types.h>
#include <sys/stat.h>
#include <cerrno>
#include <cstring>
#include <sys/stat.h>
#include <string>
#include <fstream>


inline bool exists_test0 (const std::string& name) {
    std::ifstream f(name.c_str());
    return f.good();
}

int main()
{
    std::vector<std::string> srclist;
    std::vector<std::string> destlist;

    std::string path = "/path/to/directory";
    struct stat SrcfileInfo;
    struct stat DestfileInfo;


    for (const auto & entry : std::filesystem::recursive_directory_iterator (dst))
        destlist.push_back(entry.path().string());//std::cout << entry.path() << std::endl;


//  if (stat(destlist[0].c_str(), &fileInfo) != 0) {  // Use stat() to get the info
//       std::cerr << "Error: " << strerror(errno) << '\n';
//       return(EXIT_FAILURE);
//    }
//    std::cout << "Type:         : ";
//    if ((fileInfo.st_mode & S_IFMT) == S_IFDIR) { // From sys/types.h
//       std::cout << "Directory\n";
//    } else {
//       std::cout << "File\n";
//    }
//   // Printing all the details related to the file
//    std::cout << "Size          : " <<
//       fileInfo.st_size << '\n';               // Size in bytes
//    std::cout << "Device        : " <<
//       (char)(fileInfo.st_dev + 'A') << '\n';  // Device number
//    std::cout << "Created       : " <<
//       std::ctime(&fileInfo.st_ctime);         // Creation time
//    std::cout << "Modified      : " <<
//       std::ctime(&fileInfo.st_mtime); 


    std::cout << "end";

        for (const auto & entry : std::filesystem::recursive_directory_iterator (src))
        srclist.push_back(entry.path().string());//std::cout << entry.path() << std::endl;

    
    std::cout << "end";
    int n = 0;
    bool srcExists = false, DestExists = false; 
    for (auto& srcfile : srclist )
    {
        std::string* destFile = &destlist[n];

        //srcExists = exists_test0(srcfile);
        DestExists = exists_test0(*destFile);
        if (!DestExists)
        {
            std::filesystem::copy_file(srcfile.c_str(), (*destFile).c_str(), std::filesystem::copy_options::overwrite_existing);
            continue;
        }
        
    stat(srcfile.c_str(), &SrcfileInfo);
    stat((*destFile).c_str(), &DestfileInfo);

    if (&SrcfileInfo.st_mtime != &DestfileInfo.st_mtime)
        {
            std::filesystem::copy_file(srcfile.c_str(), (*destFile).c_str(), std::filesystem::copy_options::overwrite_existing);

        }
    
    }

}