#!/bin/sh
set -e
# http://git.kernel.org/gitweb.cgi?p=linux/storage/multipath-tools/.git
branch=master
tag=tags/0.4.9
#url=http://kernel.org/pub/scm/linux/storage/multipath-tools/.git
url=http://git.opensvc.com/multipath-tools/.git
pkg=multipath-tools
out=$pkg-branch.diff

d=$-
filter() {
	set -$d

	# do some filtering. none yet
	cat
}

if [ ! -d git ]; then
	git clone $url git
fi

cd git
	git pull
	git diff $tag..$branch | filter > ../$out.tmp
cd ..

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}
