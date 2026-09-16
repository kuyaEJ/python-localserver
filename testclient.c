#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    struct sockaddr_in server_addr;
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket");
        exit(1);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sock);
        return 1;
    }
    
    // Send HTTP GET request
    char request[] = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n";
    send(sock, request, strlen(request), 0);

    // Read and print response
    char buffer[1024];
    while (recv(sock, buffer, sizeof(buffer), 0) > 0) {
        printf("%zd", recv(sock, buffer, sizeof(buffer), 0));
        buffer[recv(sock, buffer, sizeof(buffer), 0)] = '\0';
        printf("%s", buffer);
    }

    close(sock);
    return 0;
}