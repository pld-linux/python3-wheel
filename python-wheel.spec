#
# Conditional build:
%bcond_with	tests	# unit tests [broken with "--build-base"]
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	wheel
Summary:	A built-package format for Python
Summary(pl.UTF-8):	Format zbudowanych pakietów dla Pythona
Name:		python-%{module}
Version:	0.29.0
Release:	4
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/wheel/
Source0:	https://pypi.python.org/packages/source/w/wheel/%{module}-%{version}.tar.gz
# Source0-md5:	555a67e4507cedee23a0deb9651e452f
URL:		https://bitbucket.org/pypa/wheel
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
%if "%{py_ver}" < "2.7"
BuildRequires:	python-argparse
BuildRequires:	python-importlib
%endif
BuildRequires:	python-coverage
BuildRequires:	python-jsonschema
BuildRequires:	python-keyring
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-pyxdg
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage
BuildRequires:	python3-jsonschema
BuildRequires:	python3-keyring
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pyxdg
%endif
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

%prep
%setup -q -n %{module}-%{version}

# not installed as standalone scripts, so remove unneeded shebangs
%{__sed} -ie '1d' %{module}/{egg2wheel,wininst2wheel}.py

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=build-2/lib %{__python} -m pytest --ignore build -k 'not test_keygen'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=build-3/lib %{__python3} -m pytest --ignore build
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/wheel{,-3}

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/test
%endif

%if %{with python2}
%py_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/wheel{,-2}
ln -sf wheel-2 $RPM_BUILD_ROOT%{_bindir}/wheel

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/test

%py_postclean
%endif

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt
%attr(755,root,root) %{_bindir}/wheel
%attr(755,root,root) %{_bindir}/wheel-2
%{py_sitescriptdir}/wheel
%{py_sitescriptdir}/wheel-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt
%attr(755,root,root) %{_bindir}/wheel-3
%{py3_sitescriptdir}/wheel
%{py3_sitescriptdir}/wheel-%{version}-py*.egg-info
%endif
