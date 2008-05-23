%define realver 1400

Summary:	Helper Tool for online football manager
Name:		hattrick-organizer
Version:	1.400
Release:	%mkrel 4
License:	LGPLv2+
URL:		http://www.hattrickorganizer.net/
Group:		Games/Sports
# https://ho1.svn.sourceforge.net/svnroot/ho1 HO_%realver-src
Source0:	HO_%{realver}-src.tar.bz2
Source1:	http://downloads.sourceforge.net/ho1/HO_%{realver}.zip
Source2:	build.xml
Source3:	%{name}.sh
Source4:	%{name}.png
BuildRequires:	ant
BuildRequires:	dos2unix
BuildRequires:	hsqldb
BuildRequires:	java-rpmbuild
BuildRequires:	jlayer >= 1.0-2
BuildRequires:	jpackage-utils
BuildRequires:	unzip
BuildRequires:	update-alternatives
BuildRequires:	xml-commons-apis
Requires:	hsqldb
Requires:	java >= 1.5
Requires:	jpackage-utils
Requires:	jlayer
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Hattrick Organizer is a helper tool for online football 
manager hattrick (www.hattrick.org).

%package javadoc
Summary:	Javadoc for Hattrick Organizer
Group:		Development/Java
Requires(pre):	coreutils

%description javadoc
Javadoc for Hattrick Organizer.

%prep
%setup -q -n HO_%{realver}-src

# needed for all kinds of resources, helper jars ...
unzip -q -o %{SOURCE1}

# own build.xml
install -m 644 %{SOURCE2} .

# clean up
rm *.bat
rm ho.jar
rm hsqldb.jar
rm jl*.jar
rm HOLauncher.class
rm hsqldb_lic.txt
rm README_JL.txt

dos2unix *.txt
chmod 644 *.txt

find hoplugins -type f -exec chmod 644 {} \;

%build
%ant jar javadocs

%install

# jars
install -dm 755 %{buildroot}%{_javadir}
install -pm 644 %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
	for jar in *-%{version}*; do
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
	done
	# preserve ho.jar cause of possible updates from website ...
	ln -s %{name}-%{version}.jar ho.jar
popd

# data
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -m 644 *.dat %{buildroot}%{_datadir}/%{name}
install -m 644 defaults.xml %{buildroot}%{_datadir}/%{name}
install -m 644 version.txt %{buildroot}%{_datadir}/%{name}
install -dm 755 %{buildroot}%{_datadir}/%{name}/flags
install -m 644 flags/*.png %{buildroot}%{_datadir}/%{name}/flags
install -dm 755 %{buildroot}%{_datadir}/%{name}/hoplugins
cp -a hoplugins/* %{buildroot}%{_datadir}/%{name}/hoplugins
install -dm 755 %{buildroot}%{_datadir}/%{name}/sprache
install -m 644 sprache/*.properties %{buildroot}%{_datadir}/%{name}/sprache
install -dm 755 %{buildroot}%{_datadir}/%{name}/prediction
cp -r  conf/prediction/* %{buildroot}%{_datadir}/%{name}/prediction

# startscript
# the original HO.sh was modified to use jpackage features and already packed jars
install -dm 755 %{buildroot}%{_bindir}
install -m 755 %{SOURCE3} %{buildroot}%{_bindir}

# icon and menu-entry
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Comment=Hattrick Organizer - Helper Tool for online-manager hattrick
Exec=%{name}.sh
Icon=%{name}
Name=Hattrick Organizer
Terminal=false
Type=Application
Categories=Game;SportsGame;
EOF

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr javadocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc *.txt
%{_bindir}/*.sh
%{_javadir}/*.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.dat
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/*.xml
%dir %{_datadir}/%{name}/flags
%{_datadir}/%{name}/flags/*
%dir %{_datadir}/%{name}/hoplugins
%{_datadir}/%{name}/hoplugins/*
%dir %{_datadir}/%{name}/sprache
%{_datadir}/%{name}/sprache/*
%dir %{_datadir}/%{name}/prediction
%{_datadir}/%{name}/prediction/*
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}
