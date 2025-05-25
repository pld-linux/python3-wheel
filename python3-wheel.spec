#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	wheel
Summary:	A built-package format for Python
Summary(pl.UTF-8):	Format zbudowanych pakietów dla Pythona
Name:		python3-%{module}
Version:	0.45.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/wheel/
Source0:	https://files.pythonhosted.org/packages/source/w/wheel/%{module}-%{version}.tar.gz
# Source0-md5:	dddc505d0573d03576c7c6c5a4fe0641
URL:		https://pypi.org/project/wheel/
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools >= 1:65
%if %{with tests}
BuildRequires:	python3-keyring
BuildRequires:	python3-pytest >= 6.0.0
BuildRequires:	python3-pytest-cov
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.8
Conflicts:	python-wheel < 0.37.1
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_macosx_libfile'
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/wheel{,-3}
ln -sf wheel-3 $RPM_BUILD_ROOT%{_bindir}/wheel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/wheel
%attr(755,root,root) %{_bindir}/wheel-3
%{py3_sitescriptdir}/wheel
%{py3_sitescriptdir}/wheel-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,reference,*.html,*.js}
%endif
