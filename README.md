# PDF Merge Tool

## Simple desktop app for merging and splitting pdf files

## How to run
- clone repository
- install requirements
- run main.py

## Main window

![image](https://github.com/badgersky/pdf-merge-tool/assets/111532012/4bd712c7-d52a-4faa-a0d3-5b73b8eed746)

From here you can open window for merging pdfs, for splitting pdfs, or you can quit app.

## Merge tool

![image](https://github.com/badgersky/pdf-merge-tool/assets/111532012/71f0aabb-3894-4e1a-a113-927c17154d79)

Here you can select how many pdf files you want to merge, their names will be visible in "selected files" textbox.
In "new filename" entry you can write filename for merged file, if not provided program will use filename of the first chosen pdf.
By clicking "clear" button you can clear selected files, button "back" closes window. Button "merge" merges selected files and puts them
in directory "merged" which should be created in repository directory.

## Split tool

![image](https://github.com/badgersky/pdf-merge-tool/assets/111532012/d2fdda8b-4e7c-4492-b0ef-bc623e534656)

Here you can select one pdf file you want to split, its name will be visible in "selected files" textbox. In "new filename" entry
you can type filename for split pdfs, if not provide the app will use filename of chosen pdf. The app will save split pdfs as filename-part1.pdf
and filename-part2.pdf. After selecting file you can choose in "chose page number" select box, page after which the app will split file. Buttons "clear"
and "back" work the same as in the merge tool. When you click "split" button the app will split you file and put both parts in directory "split" created in repository directory.


## Licence

"THE BEERWARE LICENSE" (Revision 42):
badgersky wrote this code. As long as you retain this 
notice, you can do whatever you want with this stuff. If we
meet someday, and you think this stuff is worth it, you can
buy me a beer in return.
