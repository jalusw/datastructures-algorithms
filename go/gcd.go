package collections

func GCD(a int, b int) int {
	if a%b == 0 {
		return b
	}

	return GCD(b, b%a)
}
