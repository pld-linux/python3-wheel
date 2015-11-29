#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	wheel
Summary:	A built-package format for Python
Name:		python-%{module}
Version:	0.24.0
Release:	0.1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/w/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	3b0d66f0d127ea8befaa5d11453107fd
URL:		https://bitbucket.org/pypa/wheel
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-argparse
BuildRequires:	python-devel
BuildRequires:	python-jsonschema
BuildRequires:	python-keyring
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-jsonschema
BuildRequires:	python3-keyring
BuildRequires:	python3-pytest
BuildRequires:	python3-setuptools
%endif
Requires:	python-argparse
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename
and the .whl extension. It is designed to contain all the files for a
PEP 376 compatible install in a way that is very close to the on-disk
format.

%package -n python3-%{module}
Summary:	A built-package format for Python
Group:		Libraries/Python

%description -n python3-%{module}
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename
and the .whl extension. It is designed to contain all the files for a
PEP 376 compatible install in a way that is very close to the on-disk
format.

This is package contains Python 3 version of the package.

%prep
%setup -q -n %{module}-%{version}

# remove unneeded shebangs
sed -ie '1d' %{module}/{egg2wheel,wininst2wheel}.py

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with test}
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
rm setup.cfg
PYTHONPATH=build-2/lib py.test --ignore build -k 'not test_keygen'

# no test for Python 3, no python3-jsonschema yet
%if %{with python3} && 0
PYTHONPATH=build-3/lib py.test-%{py3_ver} --ignore build
%endif

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
cd py3
%py3_install
cd $RPM_BUILD_ROOT%{_bindir}
	for f in $(ls); do mv $f python3-$f; done
cd -

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/test
%endif

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/test

%py_postclean
%endif

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt CHANGES.txt README.txt
%attr(755,root,root) %{_bindir}/wheel
%{py_sitescriptdir}/wheel
%{py_sitescriptdir}/wheel-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE.txt CHANGES.txt README.txt
%attr(755,root,root) %{__python}3-wheel
%{py3_sitescriptdir}/%{module}*
%endif
