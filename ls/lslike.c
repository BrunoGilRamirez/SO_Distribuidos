//Bruno Gil Ramirez
// Christian Gamez
#include <stdio.h> // para usar la funcion fprintf()
#include <stdlib.h> // para usar la funcion exit()
#include <dirent.h> // para usar la funcion opendir()
#include <sys/stat.h> // para usar la funcion stat()
#include <string.h> // para usar la funcion strlen()
#include <pwd.h> // para usar la funcion getpwuid()
#include <grp.h> // para usar la funcion getgrgid()
#include <time.h> // para usar la funcion localtime()
 
//  este programa usa la funcion stat() devuelve la informacion del archivo, incluyendo el numero de inodo.
// y este numero es el que se usa para identificar el archivo
// y el directorio es un archivo que contiene una lista de archivos y sus inodos.


int main(int argc, char *argv[]) {
    char *dirname; // se define un puntero a un arreglo de caracteres que contendrá el nombre del directorio
    DIR *dir; // se define un puntero a un directorio
    struct dirent *entry; // se define un puntero a una estructura dirent
    struct stat info; // se define un puntero a una estructura stat
    char cwd[1024]; // se define un arreglo de caracteres que contendrá el directorio actual
    if (argc < 2) { // si no se proporciona un argumento, se obtiene el directorio actual
        if (getcwd(cwd, sizeof(cwd)) == NULL) // getcwd() obtiene el directorio actual
            perror("getcwd() error"); // perror() imprime un mensaje de error
        else // si se puede obtener el directorio actual, se imprime un mensaje
            printf("Direccion actual: %s\n\n", cwd); // printf() imprime un mensaje en la pantalla
            dirname = cwd; // se asigna el directorio actual a dirname
    } else { // si se proporciona un argumento, se asigna a dirname
        dirname = argv[1];  // se asigna el argumento a dirname
    }

    if (argc > 2) { // si se proporcionan más de dos argumentos, se imprime un mensaje de error
        fprintf(stderr, "Uso: %s <directorio>, Solo requiere de un parametro.", argv[0]); // fprintf() imprime un mensaje en la pantalla
        exit(EXIT_FAILURE); // exit() termina el programa
    }


    if ((dir = opendir(dirname)) == NULL) { // opendir() abre un directorio
        fprintf(stderr, "Error opening directory %s\n", dirname); // si no se puede abrir el directorio, se imprime un mensaje de error
        exit(EXIT_FAILURE); // exit() termina el programa
    }
    
    // dirent es una estructura que contiene información sobre un archivo en un directorio (nombre, tipo, etc.)
    // dirent contiene los siguientes campos:
    // d_ino: es un entero que contiene el número de inodo del archivo
    // d_off: es un entero que contiene la posición del archivo en el directorio
    // d_reclen: es un entero que contiene el tamaño del archivo en bytes
    // d_type: es un entero que contiene el tipo de archivo
    // d_name: es un arreglo de caracteres que contiene el nombre del archivo
    while ((entry = readdir(dir)) != NULL) { // readdir() lee el directorio y devuelve un puntero a la estructura dirent
        char filepath[1024]; // se define un arreglo de caracteres que contendrá la ruta del archivo
        sprintf(filepath, "%s/%s", dirname, entry->d_name); // se crea la ruta del archivo

        if (stat(filepath, &info) == -1) { // stat() obtiene información sobre un archivo
            fprintf(stderr, "Error getting info for %s\n", filepath); // si no se puede obtener la información del archivo, se imprime un mensaje de error
            continue; // se continua con el siguiente archivo
        }

        // determina el tipo de archivo
        char filetype; // se define un caracter que determina el tipo de archivo
        switch (info.st_mode & S_IFMT) { // info.st_mode y S_IFMT son constantes de stat() que indican el tipo de archivo
            case S_IFBLK:  filetype = 'b'; break; // S_IFBLK: es una constante de stat() que indica que el archivo es un dispositivo de bloques (disco duro, unidad de CD, etc.)
            case S_IFCHR:  filetype = 'c'; break; // S_IFCHR: es una constante de stat() que indica que el archivo es un dispositivo de caracteres (teclado, ratón, etc.)
            case S_IFDIR:  filetype = 'd'; break; // S_IFDIR: es una constante de stat() que indica que el archivo es un directorio
            case S_IFIFO:  filetype = 'p'; break; // S_IFIFO: es una constante de stat() que indica que el archivo es un pipe o FIFO
            case S_IFLNK:  filetype = 'l'; break; // S_IFLNK: es una constante de stat() que indica que el archivo es un enlace simbólico
            case S_IFREG:  filetype = '-'; break; // S_IFREG: es una constante de stat() que indica que el archivo es un archivo regular
            case S_IFSOCK: filetype = 's'; break; // S_IFSOCK: es una constante de stat() que indica que el archivo es un socket
            default:       filetype = '?'; break; // ? es un caracter que no se puede imprimir
        }

        // se definen los permisos de lectura, escritura y ejecución del archivo.
        // info.st_mode: es una constante de stat() que indica los permisos del archivo
        // S_IRUSR: es una constante de stat() que indica que el usuario tiene permiso de lectura
        // S_IWUSR: es una constante de stat() que indica que el usuario tiene permiso de escritura
        // S_IXUSR: es una constante de stat() que indica que el usuario tiene permiso de ejecución
        // S_IRGRP: es una constante de stat() que indica que el grupo tiene permiso de lectura
        // S_IWGRP: es una constante de stat() que indica que el grupo tiene permiso de escritura
        // S_IXGRP: es una constante de stat() que indica que el grupo tiene permiso de ejecución
        // S_IROTH: es una constante de stat() que indica que otros tienen permiso de lectura
        // S_IWOTH: es una constante de stat() que indica que otros tienen permiso de escritura
        // S_IXOTH: es una constante de stat() que indica que otros tienen permiso de ejecución
        char perm[10] = "---------";
        if (info.st_mode & S_IRUSR) perm[0] = 'r'; // determina si el usuario tiene permiso de lectura
        if (info.st_mode & S_IWUSR) perm[1] = 'w'; // determina si el usuario tiene permiso de escritura
        if (info.st_mode & S_IXUSR) perm[2] = 'x'; // determina si el usuario tiene permiso de ejecución
        if (info.st_mode & S_IRGRP) perm[3] = 'r'; // determina si el grupo tiene permiso de lectura
        if (info.st_mode & S_IWGRP) perm[4] = 'w';  // determina si el grupo tiene permiso de escritura
        if (info.st_mode & S_IXGRP) perm[5] = 'x'; // determina si el grupo tiene permiso de ejecución
        if (info.st_mode & S_IROTH) perm[6] = 'r'; // determina si otros tienen permiso de lectura
        if (info.st_mode & S_IWOTH) perm[7] = 'w'; // determina si otros tienen permiso de escritura
        if (info.st_mode & S_IXOTH) perm[8] = 'x'; // determina si otros tienen permiso de ejecución

        struct passwd *owner = getpwuid(info.st_uid); // getpwuid() obtiene información sobre el usuario propietario del archivo
        struct group *group = getgrgid(info.st_gid); // getgrgid() obtiene información sobre el grupo propietario del archivo
        char timestr[80]; // se define un arreglo de caracteres que contendrá la fecha y hora
        strftime(timestr, 80, "%Y-%m-%d %H:%M:%S", localtime(&info.st_mtime)); // strftime() formatea la fecha y hora
        
        if ((entry->d_type == DT_DIR)&& (strcmp(entry->d_name,".")!=0) && (strcmp(entry->d_name,"..")!=0)){ // DT_DIR: es una constante de dirent() que indica que el archivo es un directorio
            printf("TIPO: %c PERMISOS: %s #ENLACES: %ld PROPIETARIOS: %s GRUPO: %s  TAMAÑO: %ld FECHA: %s NOMBRE: %s\n", filetype, perm, info.st_nlink,owner->pw_name, group->gr_name, info.st_size, timestr, entry->d_name); // info.st_nlink: es una constante de stat() que indica el número de enlaces al archivo, info.st_size: indica el tamaño del archivo en bytes

        }
        if ((entry->d_type == DT_REG)&&(strcmp(entry->d_name,".")!=0) && (strcmp(entry->d_name,"..")!=0) ){ // DT_REG: es una constante de dirent() que indica que el archivo es un archivo regular
            printf("TIPO: %c PERMISOS: %s #ENLACES: %ld PROPIETARIOS: %s GRUPO: %s  TAMAÑO: %ld FECHA: %s NOMBRE: %s\n", filetype, perm, info.st_nlink,owner->pw_name, group->gr_name, info.st_size, timestr, entry->d_name); // info.st_nlink: es una constante de stat() que indica el número de enlaces al archivo, info.st_size: indica el tamaño del archivo en bytes

        }
        //printf("Tipo: %c permisos: %s #enlaces: %ld propietario: %s grupo: %s  Tamaño: %ld fecha: %s Nombre: %s\n", filetype, perm, info.st_nlink,owner->pw_name, group->gr_name, info.st_size, timestr, entry->d_name); // info.st_nlink: es una constante de stat() que indica el número de enlaces al archivo, info.st_size: indica el tamaño del archivo en bytes
    }
    closedir(dir); // closedir() cierra el directorio
    return 0; // retorna 0
}