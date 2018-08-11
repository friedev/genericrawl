rmdir dist\py /s /q
md dist\py
md dist\py\libtcodpy
md dist\py\src

xcopy libtcodpy dist\py\libtcodpy /s /e
xcopy src dist\py\src /s /e
copy engine.py dist\py
copy *.dll dist\py
copy arial10x10.png dist\py
copy README.md dist\py
copy options.json dist\py

cd dist\py
mv engine.py GeneriCrawl.py

cd ..\..
