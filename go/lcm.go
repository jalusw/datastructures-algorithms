package dsa

func LCM(a int, b int) int {
	return ((a * b) / GCD(a, b))
}
