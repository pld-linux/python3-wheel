#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	wheel
Summary:	A built-package format for Python
Summary(pl.UTF-8):	Format zbudowanych pakietów dla Pythona
Name:		python-%{module}
Version:	0.37.1
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/wheel/
Source0:	https://pypi.python.org/packages/source/w/wheel/%{module}-%{version}.tar.gz
# Source0-md5:	f490f1399e5903706cb1d4fbed9ecb28
URL:		https://bitbucket.org/pypa/wheel
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools >= 1:40.9.0
%if %{with tests}
BuildRequires:	python-keyring
BuildRequires:	python-pytest >= 3.0.0
BuildRequires:	python-pytest-cov
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 1:40.9.0
%if %{with tests}
BuildRequires:	python3-keyring
BuildRequires:	python3-pytest >= 3.0.0
BuildRequires:	python3-pytest-cov
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename
and the .whl extension. It is designed to contain all the files for a
PEP 376 compatible install in a way that is very close to the on-disk
format.

%description -l pl.UTF-8
Format zbudowanych pakietów dla Pythona.

"wheel" to archiwum w formacie ZIP ze specjalnie sformatowaną nazwą
pliku oraz rozszerzeniem ".whl". Jest zaprojektowane, aby zawierało
wszystkie pliki instalacji zgodnej z PEP 376 w sposób bardzo zbliżony
do formatu na dysku.

%package -n python3-%{module}
Summary:	A built-package format for Python
Summary(pl.UTF-8):	Format zbudowanych pakietów dla Pythona
Group:		Libraries/Python
# /usr/bin/wheel migration
Conflicts:	python-wheel < 0.37.1

%description -n python3-%{module}
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename
and the .whl extension. It is designed to contain all the files for a
PEP 376 compatible install in a way that is very close to the on-disk
format.

%description -n python3-%{module} -l pl.UTF-8
Format zbudowanych pakietów dla Pythona.

"wheel" to archiwum w formacie ZIP ze specjalnie sformatowaną nazwą
pliku oraz rozszerzeniem ".whl". Jest zaprojektowane, aby zawierało
wszystkie pliki instalacji zgodnej z PEP 376 w sposób bardzo zbliżony
do formatu na dysku.

%package apidocs
Summary:	API documentation for Python wheel module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona wheel
Group:		Documentation

%description apidocs
API documentation for Python wheel module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona wheel.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests -k 'not test_macosx_libfile'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_macosx_libfile'
%endif
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/wheel{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/wheel{,-3}
ln -sf wheel-3 $RPM_BUILD_ROOT%{_bindir}/wheel
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/wheel-2
%{py_sitescriptdir}/wheel
%{py_sitescriptdir}/wheel-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/wheel
%attr(755,root,root) %{_bindir}/wheel-3
%{py3_sitescriptdir}/wheel
%{py3_sitescriptdir}/wheel-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,reference,*.html,*.js}
%endif
