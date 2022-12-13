package main

import (
	"encoding/json"
	"fmt"
)

type Foo struct {
	Bar string `json:"bar"`
}

func main() {
	foo := Foo{Bar: "baz"}
	fooStr, _ := json.Marshal(foo)
	fmt.Println(string(fooStr))

	json.Unmarshal(fooStr, &foo)
	fmt.Println(foo)
}
