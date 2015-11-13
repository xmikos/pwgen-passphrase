# Maintainer: Michal Krenek (Mikos) <m.krenek@gmail.com>
pkgname=pwgen-passphrase
pkgver=1.0
pkgrel=1
pkgdesc="Secure wordlist-based passphrase generator"
arch=('any')
url="https://github.com/xmikos/pwgen-passphrase"
license=('GPL3')
depends=('python')
makedepends=('python-setuptools')
optdepends=('python-pyqt5: copying to clipboard'
source=(https://github.com/xmikos/pwgen-passphrase/archive/v$pkgver.tar.gz)

build() {
  cd "$srcdir/${pkgname}-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/${pkgname}-$pkgver"
  python setup.py install --root="$pkgdir"
}

# vim:set ts=2 sw=2 et:
