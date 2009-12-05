%define realver 1425

Summary:	Helper Tool for online football manager
Name:		hattrick-organizer
Version:	1.425
Release:	%mkrel 1
License:	LGPLv2+
URL:		http://www.hattrickorganizer.net/
Group:		Games/Sports
# as upstream provides no extra src.zip, this is svn r666
Source0:	HO_%{realver}-src.tar.bz2
Patch0:		%{name}-startscript.patch
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	dos2unix
BuildRequires:	fdupes
BuildRequires:	hsqldb
#BuildRequires:	java-1_7_0-icedtea-devel
BuildRequires:	java-rpmbuild
#BuildRequires:	java-1_6_0-sun-devel
BuildRequires:	jlayer
BuildRequires:	jpackage-utils
BuildRequires:	unzip
BuildRequires:	xerces-j2
BuildRequires:	xmlbeans
BuildRequires:	xml-commons-apis
Requires:	hsqldb
Requires:	java >= 1.6
Requires:	jlayer
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Hattrick Organizer is a helper tool for online football
manager (www.hattrick.org),

%prep
%setup -q -n HO1SF
%patch0 -p0

# clean up already packaged jars
pushd Core/src/conf/addToZip
	rm hsqldb.jar
#	ln -s %{_javadir}/hsqldb.jar .
	rm jl*.jar
#	ln -s %{_javadir}/jl.jar jl1.0.jar
popd

# remove Classpath from Manifest
cat > Core/src/conf/MANIFEST.MF << EOF
Manifest-Version: 1.0
Java-Version: 1.6
Created-By: mdv
Main-Class: de.hattrickorganizer.HO
EOF

%build
%ant \
    -f Core/AntBuild.xml \
    -DincludePlugins.Dev=ALL \
    -DincludePlugins.Release=ALL \
    -Dcompile.Classpath="./:./hoplugins:../Core/src/conf/addToZip/jcalendar-1.3.2.jar:`build-classpath hsqldb jl`" \
    ant-compile copy2build

%install
rm -rf %{buildroot}

export NO_BRP_CHECK_BYTECODE_VERSION=true

pushd Core/build
	rm *.bat
	rm hsqldb_lic.txt
	rm README_JL.txt

	dos2unix *.txt
	chmod 644 *.txt

	# jars
	install -dm 755 %{buildroot}%{_javadir}/%{name}
	install -pm 644 ho.jar %{buildroot}%{_javadir}/%{name}/%{name}-%{version}.jar
	pushd %{buildroot}%{_javadir}/%{name}
		for jar in *-%{version}*; do
			ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
		done
		# preserve name ho.jar cause of possible updates from website ...
		ln -s %{name}-%{version}.jar ho.jar
	popd
	install -pm 644 jcalendar*.jar %{buildroot}%{_javadir}/%{name}

	# data
	install -dm 755 %{buildroot}%{_datadir}/%{name}
	install -m 644 version.txt %{buildroot}%{_datadir}/%{name}
	rm version.txt
	install -m 644 *.ico %{buildroot}%{_datadir}/%{name}
	install -dm 755 %{buildroot}%{_datadir}/%{name}/flags
	install -m 644 flags/*.png %{buildroot}%{_datadir}/%{name}/flags
	install -dm 755 %{buildroot}%{_datadir}/%{name}/hoplugins
	cp -a hoplugins/* %{buildroot}%{_datadir}/%{name}/hoplugins
	install -dm 755 %{buildroot}%{_datadir}/%{name}/prediction
	cp -a prediction/* %{buildroot}%{_datadir}/%{name}/prediction
	install -dm 755 %{buildroot}%{_datadir}/%{name}/sprache
	install -m 644 sprache/* %{buildroot}%{_datadir}/%{name}/sprache

	# startscript
	# the original HO.sh was modified to use jpackage features and already packed jars
	install -dm 755 %{buildroot}%{_bindir}
	install -m 755 HO.sh %{buildroot}%{_bindir}/%{name}.sh
popd

# icon and menu-entry
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 Core/build/ho_logo.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Comment=Hattrick Organizer - Helper Tool for online-manager hattrick
Exec=%{name}.sh
Icon=%{name}
Name=Hattrick Organizer
GenericName=Hattrick Organizer
Terminal=false
Type=Application
Categories=Game;SportsGame;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Core/build/*.txt
%dir %{_javadir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/flags
%dir %{_datadir}/%{name}/hoplugins
%dir %{_datadir}/%{name}/prediction
%dir %{_datadir}/%{name}/sprache
%{_bindir}/*.sh
%{_javadir}/%{name}/*
%{_datadir}/%{name}/*.ico
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/flags/*
%{_datadir}/%{name}/hoplugins/*
%{_datadir}/%{name}/prediction/*
%{_datadir}/%{name}/sprache/*
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
