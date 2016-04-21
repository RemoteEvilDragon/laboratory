package main

import (
	"fmt"
	"net"
	"os"
	"time"
	"bufio"
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
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error readingggg", err.Error())
		return
	}

	now := time.Now()
	logFile := fmt.Sprintf("%d_%d_%d.log", now.Year(), now.Month(), now.Day())

	fo, err := os.Create(logFile)
	if err != nil {
		fmt.Println(logFile, err)
		return
	}

	w := bufio.NewWriter(fo)
	w.Write(buf[:n])
	w.Flush()
}
