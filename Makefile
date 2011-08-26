VERSION		= $(shell echo `awk '{ print $$1 }' version`)
RELEASE		= $(shell echo `awk '{ print $$2 }' version`)
NEWRELEASE	= $(shell echo $$(($(RELEASE) + 1)))

MESSAGESPOT=po/messages.pot


TOPDIR = $(shell pwd)
DATE="date +%Y%m%d"
PROGRAMNAME=kermit-webui
RELEASE=0.0.1
TMPDIR=/tmp
BUILDDIR=build

all: rpms


manpage:

messages:

bumprelease:	

#setversion: 

build: clean
	echo $(TOPDIR)
	echo "- Create new $(TMPDIR)/$(BUILDDIR)"
	mkdir -p $(TMPDIR)/$(BUILDDIR)
	mkdir -p $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME)
	echo "- Copy existing Kermit sources"
	rsync -raC --exclude .git . $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME)
	echo "- Remove useless files"
	rm -Rf $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME)/src/sqlite.db
#	echo "- Rename $(PROGRAMNAME) in $(PROGRAMNAME)-$(RELEASE)"
#	mv $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME) $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME)-$(RELEASE)
	echo "- Compressing $(PROGRAMNAME) directory"
	tar -czf $(PROGRAMNAME)-$(RELEASE).tar.gz -C $(TMPDIR)/$(BUILDDIR) $(PROGRAMNAME)/
	echo "- Moving source package in dist dir"
	mkdir -p ./dist
	mv $(PROGRAMNAME)-$(RELEASE).tar.gz ./dist

clean:
	-rm -rf dist/ 
	-rm -rf rpm-build/
	-rm -rf $(TMPDIR)/$(BUILDDIR)

clean_hard:

clean_harder:

clean_hardest: clean_rpms


install: build manpage

install_hard: clean_hard install

install_harder: clean_harder install

install_hardest: clean_harder clean_rpms rpms install_rpm restart

install_rpm:

restart:

recombuild: install_harder restart

clean_rpms:
	-rpm -e kermit-webui

sdist: messages

new-rpms: bumprelease rpms

pychecker:

pyflakes:

money: clean

async: install
	/sbin/service httpd restart

testit: clean

unittest:

rpms: build manpage sdist
	mkdir -p rpm-build
	cp dist/*.gz rpm-build/
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir  %{_topdir}" \
	--define "vendor Think" \
	-ba misc/specs/kermit-webui.spec

