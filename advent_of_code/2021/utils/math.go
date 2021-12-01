package utils

func Sum(values []int) int {
	sum := 0
	for _, value := range values {
		sum = sum + value
	}
	return sum
}

func Product(values []int) int {
	product := 1
	for _, value := range values {
		product = product * value
	}
	return product
}
