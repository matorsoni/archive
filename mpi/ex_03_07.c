#include <stdio.h>
#include <string.h>

#include "mpi.h"

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int this_rank = -1, num_procs = -1;
    MPI_Comm_rank(MPI_COMM_WORLD, &this_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    char message[100];
    sprintf(message, "Hello from proc %d!\n", this_rank);
    int count = strlen(message) + 1;
    MPI_Send(message, count, MPI_CHAR, (this_rank + 1)%num_procs, 0, MPI_COMM_WORLD);

    MPI_Status status;
    MPI_Recv(message, 100, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    MPI_Get_count(&status, MPI_CHAR, &count);    
    printf("Proc %d received message:\n", this_rank);
    printf("    Source: %d, Tag: %d, Error: %d, Count: %d\n", status.MPI_SOURCE, status.MPI_TAG, status.MPI_ERROR, count);

    MPI_Finalize();
    return 0;
}
