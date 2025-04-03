package tests

import (
	"testing"

	dsa "github.com/jalusw/datastructures-algorithms/go"
)

func TestGCD(t *testing.T){
	a := 10
	b := 5
	gcd := dsa.GCD(a,b)

	if gcd != 5 {
		t.Errorf("Wrong Answer for case 10 and 5")
	}
}
