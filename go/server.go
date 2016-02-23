package main

import (
	"fmt"
	"io"
	"net"
	"os"
	"time"
)

func main() {
	fmt.Println("Starting the server ...")
	listener, err := net.Listen("tcp4", "0.0.0.0:50000")

	if err != nil {
		fmt.Println("Error listening", err.Error())
		return
	}

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting", err.Error())
			return
		}
		doServerStuff(conn)
	}
}

func doServerStuff(conn net.Conn) {
	buf := make([]byte, 512)
	_, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error readingggg", err.Error())
		return
	}

	now := time.Now()
	logFile := fmt.Sprintf("%d_%d_%d.log", now.Year(), now.Month(), now.Day())

	fout, err := os.Create(logFile)
	if err != nil {
		fmt.Println(logFile, err)
		return
	}

	//msg := fmt.Sprintf("%v\n", string(buf))
	// fmt.Println(msg)

	io.WriteString(fout, string(buf))

	defer fout.Close()
}
