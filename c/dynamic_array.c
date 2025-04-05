
int main(){ 
    int *arr;
    int size = 5;

    // Allocate memory for the array
    arr = (int *)malloc(size * sizeof(int));

    // Check if memory allocation was successful
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    // Initialize the array
    for (int i = 0; i < size; i++) {
        *(arr + i) = i + 1;
    }

    // Traverse the array using pointer arithmetic
    printf("Array elements using pointer:\n");
    for (int i = 0; i < size; i++) {
        printf("%d ", *(arr + i));
    }
    printf("\n");

    // Free the allocated memory
    free(arr);

    return 0;
}