package main

import (
	"fmt"
	"net"
	"os"
)

const remoteAddr string = "27.126.181.90:6124"
// const remoteAddr string = "localhost:50000"

func main() {
	conn, err := net.Dial("tcp", remoteAddr)
	if err != nil {
		fmt.Println("Error dialing", err.Error())
		return
	}

	_, err = conn.Write([]byte(os.Args[1]))

	fmt.Println("Successfully sending ", os.Args[1])
}
