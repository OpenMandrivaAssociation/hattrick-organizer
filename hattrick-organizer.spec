%define oname HO
%define realver 1400

Summary:	Helper Tool for online-manager www.hattrick.org
Name:		hattrick-organizer
Version:	1.400
Release:	%mkrel 1
License:	LGPLv2+
Group:		Games/Sports
Url:		http://www.hattrickorganizer.net/
Source0:	http://downloads.sourceforge.net/ho1/%{oname}_%{realver}.zip
BuildRequires:	java-rpmbuild
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Hattrick Organizer is a helper tool for online football
manager www.hattrick.org .

%prep
%setup -q -c
dos2unix *.txt

%build

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}



%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc
%attr(755,root,root)
