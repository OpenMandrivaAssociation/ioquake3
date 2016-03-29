set -x

git clone https://github.com/ioquake/ioq3.git
pushd ioq3
GIT_COMMIT="git rev-parse --short=6 HEAD"
git archive --format=tar --prefix ioquake3-1.36-`${GIT_COMMIT}`/ HEAD | xz -vf > ../ioquake3-1.36-`$GIT_COMMIT`.tar.xz
popd
