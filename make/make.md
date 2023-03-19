# making an executable

In order to be able to run the program without having to install all kinds of dependencies a script is used to make an executable.
This executable can only be run on the platform where it was build. So if you build this on windows it can be used on a windows system. If you build this on a *nix machine it should run on any *nix machine.

### How to build an executable
On the machine where you build the executable a python distribution has to be installed. ( 3.11 or higher)
Also the python package pyinstaller has to be installed. (see documentation on https://pyinstaller.org/en/stable/)
Open a bash command window and navigate therin to de make directory.
Run the make.sh script. ( On *nix you may have to alter the atrributes of the file.)
Within de make directory 2 new directories will be created. A 'build' directory, which is of no use. And a 'dist' directory, which contains the executable.
You can copy the dist directory to a location of your choosing. 

### requirements to run the executable
Since the program uses git, git has to be in the path of the user who runs the program.  

### How to run the executable
After copying the 'dist' directory with all its contents you will have to configure the application.
See ../var/ini.md how this must be done.
Now run a command prompt (windows) or shell prompt (*nix) and navigate therin to the directory 'dist/main'.
Start the program 'main.exe' without any parameters.
Logging will appear in the directory 'dist/log'.







