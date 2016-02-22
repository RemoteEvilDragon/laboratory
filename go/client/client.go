package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	conn, err := net.Dial("tcp", "27.126.181.90:50000")
	if err != nil {
		//No connection could be made because the target machine actively refused it.
		fmt.Println("Error dialing", err.Error())
		return
	}
	inputReader := bufio.NewReader(os.Stdin)
	fmt.Println("First,what is your name?")
	clientname, _ := inputReader.ReadString('\n')
	trimmedClient := strings.Trim(clientname, "\r\n")
	//send info to server until Quit:
	for {
		fmt.Println("what to send to the server?Type Q to quit.")
		input, _ := inputReader.ReadString('\n')
		trimmedInput := strings.Trim(input, "\r\n")
		if trimmedInput == "Q" {
			return
		}
		_, err = conn.Write([]byte(trimmedClient + "says:" + trimmedInput))
	}
}
