#
# Conditional build:
%bcond_with	tests	# do not perform "make test"

%define 	module	django-assets
Summary:	Asset management for Django, to compress and merge CSS and Javascript files
Name:		python-%{module}
Version:	0.8
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/d/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	2c7f3876420f825aa39f9bbfe5f7f95d
URL:		http://github.com/miracle2k/django-assets
BuildRequires:	python-devel
BuildRequires:	python-django
BuildRequires:	python-nose
BuildRequires:	python-sphinx
BuildRequires:	python-webassets >= 0.8
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-django
Requires:	python-webassets >= 0.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Integrates the webassets library with Django, adding support for
merging, minifying and compiling CSS and Javascript files.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%if %{with tests}
# Unittests can't be run yet: https://github.com/miracle2k/django-assets/issues/10
%{__python} setup.py test
%endif

# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
rm -r html/.{doctrees,buildinfo}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/tests

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc html README.rst LICENSE
%{py_sitescriptdir}/django_assets
%{py_sitescriptdir}/django_assets-%{version}-py*.egg-info
