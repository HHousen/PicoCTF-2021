# speeds and feeds

## Problem

> There is something on my shop network running at mercury.picoctf.net:16524, but I can't tell what it is. Can you?

## Solution

1. We can use `nc` to connect to the challenge and output the commands to a file: `nc mercury.picoctf.net 16524 > cnc_command.txt`

2. Searching for `What language does a CNC machine use?` finds that the answer is `g-code` Searching for `simulate g-code` finds [NCViewer](https://ncviewer.com/) ([WebGCode](https://nraynaud.github.io/webgcode/) is another option).

3. We can paste in the contents of [cnc_command.txt](./cnc_command.txt) into the "GCode File" panel and then click "Plot" to view the flag.

### Flag

`picoCTF{num3r1cal_c0ntr0l_1395ffad}`
