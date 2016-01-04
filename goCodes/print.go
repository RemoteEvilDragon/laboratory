package main

import "fmt"

var (
    version  = "0.8"
    build    = "Custom"
    codename = "Post Apocalypse"
    whythis = "code style"
    whythat = "portable git test"
    intro    = "A stable and unbreakable connection for everyone."
)

func main() {
    fmt.Printf("hello, world:%v\n",version)
}
