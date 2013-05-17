#!/bin/sh
set -e
# http://git.opensvc.com/gitweb.cgi?p=multipath-tools/.git
branch=master
tag=tags/0.4.9
url=http://git.opensvc.com/multipath-tools/.git
pkg=multipath-tools
out=$pkg-git.patch

d=$-
filter() {
	set -$d

	# do some filtering. none yet
	cat
}

if [ ! -d $pkg ]; then
	git clone $url $pkg
fi

cd $pkg
	git pull
	git diff $tag..$branch | filter > ../$out.tmp
cd ..

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}
