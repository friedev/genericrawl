pyinstaller engine.py -y

copy *.dll dist\engine
copy arial10x10.png dist\engine
copy README.md dist\engine
copy options.json dist\engine

cd dist\engine
mv engine.exe GeneriCrawl.exe
mv engine.exe.manifest GeneriCrawl.exe.manifest

cd ..\..
