# Documentation with Sphinx

## Getting Started
1.) Assuming you've already cloned down the repo, start up vagrant and use the "vagrant ssh" command to then switch to a terminal accessing the virtual machine vagrant has created.

2.) Navigate to the docs folder located at "acm.mst.edu/docs/" where acm.mst.edu is the name given to the main folder you've cloned down (assuming you didn't change the name).

3.) Run the command "make rst". This will create the rst files located in the "app_rst_docs" folder (which you shouldn't have to mess with).

4.) Run the command "make html". This will create the html files based off of the sphinx settings along with the autodoc generated rst files that were created with the previous command.

5.) Open up a file explorer and go to "acm.mst.edu/docs/\_build/html/". Inside this folder is a file named "index.html"; click on this file to open it in a web browser.

6.) From here, you can explore what the documentation currently looks like. The documentation for the apps (events, payments, etc.) can be found by going to the bottom of the main documentation page and clicking on "Module Index".

## Sphinx Documentation Resources
- http://www.sphinx-doc.org/en/stable/contents.html
- http://docutils.sourceforge.net/rst.html
- https://thomas-cokelaer.info/tutorials/sphinx/index.html
