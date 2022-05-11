#include <iostream>
using namespace std;

#include "mscl/mscl.h"

#include "getCurrentConfig.h"
#include "parseData.h"
#include "setCurrentConfig.h"
#include "setToIdle.h"
#include "startSampling.h"

void PrintInfo(mscl::InertialNode& node) {
   cout << "Node Information: " << endl;
   cout << "Node address: " << &node << endl;
   cout << "Node ping response: " << node.ping() << endl;
   cout << "Model Name: " << node.modelName() << endl;
   cout << "Model Number: " << node.modelNumber() << endl;
   cout << "Serial: " << node.serialNumber() << endl;
   cout << "Firmware: " << node.firmwareVersion().str() << endl << endl;
}
int main(int argc, char** argv) {
   // Most use will depend on available hardware
   // Trying some possibilities
   const string COM_PORT = "COM4";
   const string ip = "10.0.0.7";
   const int port = 7002;
   try {
      mscl::Connection connection = mscl::Connection::Serial(COM_PORT);
      mscl::InertialNode node(connection);
      PrintInfo(node);
      // getCurrentConfig(node);
      // setCurrentConfig(node);       //Warning: this example changes settings
      // on your Node! startSampling(node); setToIdle(node); parseData(node);
   } catch (mscl::Error& e) {
      cout << "Could not access node on " << COM_PORT << " Error: " << e.what()
           << endl;
   } catch (...) {
      cout << "Could not access node on " << COM_PORT << endl;
   }
   try {
      mscl::Connection connection = mscl::Connection::TcpIp(ip, port);
      mscl::InertialNode node(connection);
      node.timeout(10000);
      PrintInfo(node);
   } catch (mscl::Error& e) {
      cout << "Could not access node on " << ip << " - " << std::to_string(port)
           << " Error: " << e.what() << endl;
   } catch (...) {
      cout << "Could not access node on " << ip << " - "
           << std::to_string(port);
   }
   return 0;
}
