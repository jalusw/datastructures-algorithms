package tests

import (
	"testing"

	dsa "github.com/jalusw/collections/go"
)

func TestLCM(t *testing.T) {

	a := 10
	b := 5

	if dsa.LCM(a, b) != 10 {
		t.Errorf("Wrong LCM answer for 10 and 5")
	}

}
