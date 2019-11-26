package main

import (
	"os"
	"fmt"
	"github.com/urfave/cli"
)

var (
	ParseCommand = cli.Command{
		Name:        "parse",
		Usage:       "Command to generate ethereum accounts",
		Description: `Creation of public key, private key, and account address`,
		Action:      parseCommand,
		Flags:       []cli.Flag{},
	}
)

func parseCommand(ctx *cli.Context) error {
	fp := ""
	fmt.Println(len(os.Args))
	if (len(os.Args) < 3 || len(os.Args) > 3 && len(os.Args) !=3) {
		fmt.Println("Error in Argument for File Path Provided")
                return nil
	} else {
		fp = os.Args[2]
	}
        parse(fp)		
	return nil
}

