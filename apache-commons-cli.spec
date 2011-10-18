%global base_name       cli
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.2
Release:          4
Summary:          Command Line Interface Library for Java
Group:            Development/Java
License:          ASL 2.0
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    apache-commons-parent

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils

Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

# This should go away with F-17
Provides:         jakarta-%{short_name} = 0:%{version}-%{release}
Obsoletes:        jakarta-%{short_name} < 0:1.1-6

%description
The CLI library provides a simple and easy to use API for working with the 
command line arguments and options.

%package javadoc
Summary:          Javadoc for %{name}
Group:            Development/Java
Requires:         jpackage-utils
# This should go away with F-17
Obsoletes:        jakarta-%{short_name}-javadoc < 0:1.1-6

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# following line is only for backwards compatibility. New packages
# should use proper groupid org.apache.commons and also artifactid
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.txt RELEASE-NOTES.txt
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


