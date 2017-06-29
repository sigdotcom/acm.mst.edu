# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python3 -msphinx
SPHINXPROJ    = MST-ACMWebsiteacmmstedu
SOURCEDIR     = .
BUILDDIR      = _build
SPHINX_APIDOC_OPTIONS=members,show-inheritance

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Used as a quick way of using autodoc to create rst files. Works in
# conjuntion with the variable above named "SPHINX_APIDOC_OPTIONS" which allows
# you to change what autodoc variables are added to the rst files that are
# created. Additionally, the force command is used so that even if there isn't
# a change to the python files, it will still create new files in case the
# "SPHINX_APIDOC_OPTIONS" variable was changed.
rst:
	sphinx-apidoc -o apps/events/ ../ACM_General/events/ ../ACM_General/events/migrations/ --force
