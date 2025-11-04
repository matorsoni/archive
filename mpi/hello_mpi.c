#include <stdio.h>
#include <string.h>

#include <unistd.h>

#include "mpi.h"

int main(int argc, char** argv) {
    int my_rank;
    int p;
    int source;
    int dest;
    int tag = 0;
    char message[100];
    MPI_Status status;

    // start up mpi
    MPI_Init(&argc, &argv);
    
    // find out process rank
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    // find out number of processes
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    if (my_rank != 0) {
        sleep(1);
        // create message
        sprintf(message, "Greetings from process %d!", my_rank);
        dest = 0;
        MPI_Send(message, strlen(message)+1, MPI_CHAR, dest, tag, MPI_COMM_WORLD);
    } else {
        for (source = 1; source < p; ++source) {
            MPI_Recv(message, 100, MPI_CHAR, source, tag, MPI_COMM_WORLD, &status);
            printf("%s\n", message);
        }
    }

    // shut down mpi
    MPI_Finalize();

    
    return 0;
}

