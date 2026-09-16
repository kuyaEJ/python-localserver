#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    int sock, new_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    char buffer[1024];
    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(1);
    }

    // bind socket to address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(80); // HTTP port
    if (bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind");
        close(sock);
        exit(1);
    }

    // Listen for connections
    if (listen(sock, 10) == -1) {
        perror("listen");
        close(sock);
        exit(1);
    }
    
    printf("Server listening on port 80\n\r");

    while (1) {
        new_fd = accept(sock, (struct sockaddr*)&client_addr, &addr_len);
        if (new_fd == -1) {
            perror("accept");
            continue;
        }

        printf("Client connect from %s:%d\n",
            inet_ntoa(client_addr.sin_addr),
            ntohs(client_addr.sin_port));
        
        while (1) {
            ssize_t bytes = read(new_fd, buffer, sizeof(buffer) - 1);
            if (bytes == 0) break; // Client closed
            buffer[bytes] = '\0';
            printf("Received: %s\n", buffer);
            write(new_fd, buffer, strlen(buffer));
        }

        close(new_fd);
    }
    
    // Connect to server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        // perror("bind");
        close(sock);
        return 1;
    }

    char message[] = "Hello Server!";
    ssize_t bytes_sent = send(sock, message, strlen(message), 0);
    if (bytes_sent < 0) {
        perror("send");
        return 1;
    }
    printf("Sent %zd bytes\n", bytes_sent);


    close(sock);
    return 0;
}


// netstat -an -p tcp | grep LISTEN

// gcc test.c -o test
// saves test.c compilation executable into the file 'test'
// ./test runs the compiled executable
// gcc -Wall -o test test.c
// Adds warnings
// gcc -Wall -save-temps test.c -o test
// lets you see intermediate files with extensions: test.bc, test.i, test.i, test.s