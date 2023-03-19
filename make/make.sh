# clean folders
rm -R build
rm -R dist

# build program
pyinstaller main.saved.spec

# add additional files and directories
mkdir dist/log
mkdir dist/var
cp ../var/commitextractor.ini dist/var
cp ../var/commitextractor.seed dist/var