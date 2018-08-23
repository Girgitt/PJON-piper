#include "stdafx.h"
#include <stdio.h> 
#include <iostream>
#include <iomanip>
#include <string> 
#include <sstream>

#include <inttypes.h>  
#include <stdlib.h>
#include <chrono>
#include <thread>
#include <mutex>

//#define TS_RESPONSE_TIME_OUT 25000
//#define TS_COLLISION_DELAY 3
#define PJON_INCLUDE_TS true // Include only ThroughSerial
#include "PJON/src/PJON.h"
#include "PJON/src/PJONDefines.h"

#include "version.h"

std::mutex bus_mutex;

std::string read_std_in(){
  std::string inStr;
  DWORD fdwMode, fdwOldMode;
  HANDLE hStdIn = GetStdHandle(STD_INPUT_HANDLE);
  GetConsoleMode(hStdIn, &fdwOldMode);
  // disable mouse and window input
  fdwMode = fdwOldMode ^ ENABLE_MOUSE_INPUT ^ ENABLE_WINDOW_INPUT;
  SetConsoleMode(hStdIn, fdwMode);

  if (WaitForSingleObject(hStdIn, 20) == WAIT_OBJECT_0){
    std::getline(std::cin, inStr);
    if (inStr.length() > 1) {
      return inStr;
    }
  }
  return "NO_INPUT";
}

uint64_t rcvd_cnt = 0; // std::time(nullptr);

static void receiver_function(
	uint8_t *payload,
	uint16_t length,
	const PJON_Packet_Info &packet_info){
  
  rcvd_cnt += 1;
  
  std::cout << "#RCV snd_id=" << std::to_string(packet_info.sender_id)
            << " snd_net=";
                          for (uint32_t i = 0; i < sizeof(packet_info.sender_bus_id); i++) {
                            std::cout << std::to_string(packet_info.sender_bus_id[i]);
                            if (i < sizeof(packet_info.sender_bus_id) - 1)
                              std::cout << ".";
                          }
  std::cout << " rcv_id=" << std::to_string(packet_info.receiver_id)
            << " rcv_net=";
                          for (uint32_t i = 0; i < sizeof(packet_info.receiver_bus_id); i++) {
                            std::cout << std::to_string(packet_info.receiver_bus_id[i]);
                            if (i < sizeof(packet_info.receiver_bus_id) - 1)
                              std::cout << ".";
                          }
 std::cout << " id=" << std::to_string(packet_info.id)
           << " hdr=" << std::to_string(packet_info.header)
           << " pckt_cnt=" << std::to_string(rcvd_cnt)
           << " len=" << length
           << " data=";
	                    for (uint32_t i = 0; i != length; i++){
		                    std::cout << payload[i];
	                    }
  std::cout << std::endl;
}

static void error_handler_function(uint8_t code, uint16_t data, void *custom_pointer) {
  std::cout << "#ERR code=" << std::to_string(code);
  std::cout << " data=" << std::to_string(data);
  std::cout << std::endl;
};

std::string get_token_at_pos_for_delim(
  std::string const& str, 
  std::string const& delim, 
  int index){

  std::string s = str;
  std::string delimiter = delim;
  size_t last = 0;
  size_t next = 0;
  int current_token = 0;

  while ((next = s.find(delimiter, last)) != std::string::npos){
    //std::cout << s.substr(last, next - last) << std::endl;
    if (current_token == index) 
      return s.substr(last, next - last);
    last = next + delimiter.length();
    current_token += 1;
  }
  
  if (current_token == index)
    return s.substr(last);
  return "";
}


bool is_enough_args(int argc, char **argv) {
  if (argc < 4) 
    return false;
  return true;
}


bool is_first_arg_com_port(int argc, char **argv) {
  //std::cout << "argv[1]: " << std::string(argv[1]) << "\n";
  if (std::string(argv[1]).find("COM") != std::string::npos)
    return true;
  return false;
}


bool is_second_arg_bitrate(int argc, char **argv) {
  //std::cout << "CHECKING BITRATE: " << std::stoi(std::string(argv[2])) << "\n";
  if (0 < std::stoi(std::string(argv[2])))
    if(std::stoi(std::string(argv[2]))  <= 153600)
      return true;
  return false;
  }


bool is_third_arg_bus_id(int argc, char **argv) {
  if (0 <= std::stoi(std::string(argv[3])))
    if (std::stoi(std::string(argv[3])) <= 255)
      return true;
  return false;
}

bool is_fourth_arg_console_switch(int argc, char **argv) {
  if (argc < 5)
    return false;
  std::cout << argc;

  if (std::string(argv[4]).find("console") != std::string::npos)
    return true;
  return false;
}

void print_usage_help() {
  std::cout
    << "PJON-piper - a lightweight command line client to PJON bus\n"
    << "VERSION: " << PJON_PIPER_VERSION << "\n"
    << "\n"
    << "usage:   pjon_piper.exe COM PORT BITRATE NODE ID <console>\n"
    << "                          \\        \\     \\           | \n"
    << "                           \\        \\     0-255      |  \n"
    << "                            COMXX    1200 - 153600   |    \n"
    << "                      freezes on typing send/set commands    \n"
    << std::endl
    << "example: pjon_piper.exe COM3 57600 254" << std::endl
    << std::endl
    << "other options:" << std::endl
    << "   help - print this help" << std::endl
    << "   coms - displays available COM ports"  << std::endl
    << "version - displays program version" << std::endl
    << "--------------------------------------" << std::endl
    ;

}


void print_send_help(){
  std::cout
    << "send <NODE ID> data=<CHAR PAYLOAD>\n"
    << " \\     \\              \\\n"
    << "  \\     0-255          SOME DATA\n"
    << "   send         - use configured ACK\n"
    << "   send_noack   - force no ACK\n"
    << "   send_syn     - force sync. ACK\n"
    << "   send_asyn    - force async. ACK\n"
    << "   send_synasyn - force syn. asyn. ACK\n"
    << "--------------------------------------\n"
    << "example: send 33 data=B123\n";
}


void print_ack_help() {
  std::cout
    << "set ack <none|synasyn|syn|asyn>       \n"
    << "         /______/______/__/           \n"
    << "      none - no ACK \n"
    << "       syn - synchronous ACK \n"
    << "      asyn - asynchronous ACK \n"
    << "   synasyn - synchr. ACKed async. ACK \n"
    << "--------------------------------------\n"
    << "example: set ack none\n";
}


void print_commands_help() {
  std::cout << "available commands:\n"
            << "======================================\n";
  print_send_help();
  std::cout << "======================================\n";
  print_ack_help();
  std::cout << "======================================\n";
}


void print_available_com_ports(){
  HANDLE hCom = NULL;

  std::cout << "available COM ports:" << std::endl
            << "--------------------------------------" << std::endl;

  for (int i = 1; i <= 99; ++i) {
    std::string com_str = std::string("\\\\.\\COM") + std::to_string(i);

    hCom =
      CreateFile(
        std::wstring(com_str.begin(), com_str.end()).c_str(),
        GENERIC_READ | GENERIC_WRITE,
        0,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
      );

    if (hCom != INVALID_HANDLE_VALUE){
      std::cout << "COM" << std::to_string(i) << std::endl;
      CloseHandle(hCom);
    }
  }

  std::cout << "--------------------------------------" << std::endl
    ;
}

void listen_on_bus(PJON<ThroughSerial> bus, bool is_console_mode) {
  if(!is_console_mode)
    while(true) {
      bus_mutex.lock();
      bus.update();
      bus.receive(1000);
      bus_mutex.unlock();
      delayMicroseconds(1 * 1000);
    }
}

int main(int argc, char **argv) {
  bool is_console_mode = false;

  if (argc == 2) {
    if (std::string(argv[1]) == "help") {
      print_usage_help();
      print_commands_help();
      return 0;
    }
    else if (std::string(argv[1]) == "coms") {
      print_available_com_ports();
      return 0;
    }
    else if (std::string(argv[1]) == "version") {
      std::cout << "VERSION: " << PJON_PIPER_VERSION << "\n";
      return 0;
    }
    print_usage_help();
    std::cerr << "ERROR: option not supported\n";
    return 1;
  }

  if (!is_enough_args(argc, argv)) {
    print_usage_help();
    std::cerr << "ERROR: not enough args\n";
    return 1;
  }
  if (!is_first_arg_com_port(argc, argv)) {
    print_usage_help();
    std::cerr << "ERROR: first arg <COM PORT> should be COMXX\n";
    return 1;
  }
  if (!is_second_arg_bitrate(argc, argv)) {
    print_usage_help();
    std::cerr << "ERROR: second arg <BITRATE> should specify bitrate 1 - 153600 like 2400, 19200, 38400, 57600, 115200, 153600\n";
    return 1;
  }
  if (!is_third_arg_bus_id(argc, argv)) {
    print_usage_help();
    std::cerr << "ERROR: third arg <NODE ID> should specify bus address 0 - 255\n";
    return 1;
  }
  
  if (argc > 4) {
    if (!is_fourth_arg_console_switch(argc, argv)) {
      print_usage_help();
      std::cerr << "ERROR: fourth optional arg <console> should be console or empty\n";
      return 1;
    }
    else {
      is_console_mode = true;
    }
  }
  else {
    is_console_mode = false;
  }
  

  HANDLE hStdIn = GetStdHandle(STD_INPUT_HANDLE);

  FlushConsoleInputBuffer(hStdIn);


  bool resetComOnStratup = false;
  bool testComOnStartup = false;

  std::string com_str = std::string("\\\\.\\") + std::string(argv[1]);
  int bitRate = std::stoi(std::string(argv[2]));

  printf("PJON instantiation... \n");
  uint8_t bus_id[] = { 0, 0, 0, 1 };

  PJON<ThroughSerial> bus(std::stoi(std::string(argv[3])));
  bus.set_router(false);
  try {
    printf("Opening serial... \n");
    Serial serial_handle(com_str, bitRate, testComOnStartup, resetComOnStratup);

    if (resetComOnStratup)
      delayMicroseconds(2 * 1000 * 1000);

    printf("Setting serial... \n");
    bus.strategy.set_serial(&serial_handle);

    printf("Opening bus... \n");
    bus.begin();
    bus.set_receiver(receiver_function);
    bus.set_error(error_handler_function);
    bus.set_synchronous_acknowledge(true);
    
    std::thread bus_receive_thd(listen_on_bus, bus, is_console_mode);


    while (true) {
      //std::string stdIn = "NO_INPUT";//read_std_in();
      std::string stdIn = read_std_in();

      if (stdIn != "NO_INPUT") {

        auto command = get_token_at_pos_for_delim(stdIn, " ", 0);

        if (command == "send" ||
          command == "send_noack" ||
          command == "send_syn" ||
          command == "send_asyn" ||
          command == "send_synasyn") {
          // send <node_address> data=<payload>
          try {
            uint16_t original_config = bus.config;
            std::string node_addr_str = get_token_at_pos_for_delim(stdIn, " ", 1);
            std::string data_str = get_token_at_pos_for_delim(stdIn, "data=", 1);

            if (command == "send_syn") {
              bus.set_synchronous_acknowledge(true);
              bus.set_asynchronous_acknowledge(false);
            }
            else if (command == "send_noack") {
              bus.set_synchronous_acknowledge(false);
              bus.set_asynchronous_acknowledge(false);
            }
            else if (command == "send_asyn") {
              bus.set_synchronous_acknowledge(false);
              bus.set_asynchronous_acknowledge(true);
            }
            else if (command == "send_synasyn") {
              bus.set_synchronous_acknowledge(true);
              bus.set_asynchronous_acknowledge(true);
            }

            std::cout << "snd"
                      << " rcv_id=" << node_addr_str
                      << " data=" << data_str
                      << std::endl;

            int node_adr = std::stoi(node_addr_str);

            bus_mutex.lock();
              bus.send(
                node_adr,
                data_str.c_str(),
                data_str.length()
              );

              for (int i = 0; i < 10; i++) {
                bus.update();
                //delayMicroseconds(10);
              }
            bus_mutex.unlock();

            bus.config = original_config;
          }
          catch (const std::exception&) {
            std::cerr << "ERROR: SEND failure\n";
          }
        }
        else if (command == "set") {

          std::string parameter = get_token_at_pos_for_delim(stdIn, " ", 1);
          std::string parameter_value = get_token_at_pos_for_delim(stdIn, " ", 2);

          if (parameter == "ack") {

            if (parameter_value == "syn") {
              std::cout << "   ack set to: " << "syn";
              bus.set_synchronous_acknowledge(true);
              bus.set_asynchronous_acknowledge(false);
            }
            else if (parameter_value == "asyn") {
              std::cout << "   ack set to: " << "asyn";
              bus.set_asynchronous_acknowledge(true);
              bus.set_synchronous_acknowledge(false);
            }
            else if (parameter_value == "synasyn") {
              std::cout << "   ack set to: " << "synasyn";
              bus.set_asynchronous_acknowledge(true);
              bus.set_synchronous_acknowledge(true);
            }
            else if (parameter_value == "none") {
              std::cout << "   ack set to: " << "none";
              bus.set_asynchronous_acknowledge(false);
              bus.set_synchronous_acknowledge(false);
            }
            else {
              print_ack_help();
              std::cout << "ERROR: ack mode not supported";
            }
            std::cout << std::endl;
          }

        }
        else {
          print_commands_help();
          std::cout << "ERROR: command not supported\n";
        }
      }

      bus_mutex.lock();
        bus.update();
      
        if(is_console_mode){
          bus.receive(1000);
        }
     bus_mutex.unlock();

      delayMicroseconds(1 * 1000);
    }

    //printf("Attempting to receive from bus on exit... \n");
    //bus.receive(100);
    //printf("Success! \n");
    return 0;
  }
  catch (const char* msg) {
    std::cout << "exc: "
              << msg
              << std::endl;
    print_available_com_ports();
    return 1;
  }
};