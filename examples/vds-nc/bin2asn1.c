#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

int main(int argc, char ** argv) {
	char preamble[] = { 0x30 , 0x46 };
	char sha[] = { 0x02, 0x21, 0 };

	char buff[32];
	write(STDOUT_FILENO, preamble, 2);

	write(STDOUT_FILENO, sha, 3);
	read(STDIN_FILENO,buff,32);
	write(STDOUT_FILENO,buff,32);

	write(STDOUT_FILENO, sha, 3);
	read(STDIN_FILENO,buff,32);
	write(STDOUT_FILENO,buff,32);
};
