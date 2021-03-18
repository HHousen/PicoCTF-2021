# Disk, disk, sleuth! II

## Problem

> All we know is the file with the flag is named `down-at-the-bottom.txt`... Disk image: dds2-alpine.flag.img.gz

* [dds2-alpine.flag.img.gz](https://mercury.picoctf.net/static/b369e0ba3b6ffd2be8164cd3c99c294b/dds2-alpine.flag.img.gz)

## Solution

1. Using the [TSK Tool Overview](http://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview) website we can find that the `fls` command can list all files in a directory. We specify the `-r`, which means recursive so it will scan the entire disk image, and `-p`, so it prints the full path, flags. The `-o` flag is the offset of the partition we want to use, which can be dounf by running `mmls dds2-alpine.flag.img`. Finally, we search the output using `grep` for the name of the file given in the challenge description. So, the resulting command looks as follows: `fls -r -p -o 2048 dds2-alpine.flag.img | grep down-at-the-bottom.txt`. The output is: `r/r 18291:  root/down-at-the-bottom.txt`

2. `18291` is the inode number of the file. We can use `icat` to list the contents of that inode like so: `icat -o 2048 dds2-alpine.flag.img 18291`

    The flag is shown in the output (inside of a unique pattern so we couldn't simply search for it):

    ```
      _     _     _     _     _     _     _     _     _     _     _     _     _  
     / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
    ( p ) ( i ) ( c ) ( o ) ( C ) ( T ) ( F ) ( { ) ( f ) ( 0 ) ( r ) ( 3 ) ( n )
     \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 
      _     _     _     _     _     _     _     _     _     _     _     _     _  
     / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
    ( s ) ( 1 ) ( c ) ( 4 ) ( t ) ( 0 ) ( r ) ( _ ) ( n ) ( 0 ) ( v ) ( 1 ) ( c )
     \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 
      _     _     _     _     _     _     _     _     _     _     _  
     / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
    ( 3 ) ( _ ) ( 0 ) ( b ) ( a ) ( 8 ) ( d ) ( 0 ) ( 2 ) ( d ) ( } )
     \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 
    ```

3. Alternatively, `autopsy` can be used to interact with the disk in a GUI, which may be easier. It was easier for me at at first.

### Flag

`picoCTF{f0r3ns1c4t0r_n0v1c3_0ba8d02d}`
