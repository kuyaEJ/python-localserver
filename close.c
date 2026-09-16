#include <sys/socket.h>
#include <unistd.h>
#include <stdlib.h>

int sock = -1;

void cleanup(void) {
    if (sock != -1) {
        close(sock);
        sock = -1;
    }
}

int main() {
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(1);
    }

    // ... do work ...

    cleanup(); // Close socket before exit
    exit(0);
}
