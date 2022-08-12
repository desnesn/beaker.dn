# Beaker

Beaker is open-source software for managing and automating labs of test 
computers.

See the [Beaker homepage](http://beaker-project.org/) for further 
documentation and information about the Beaker project.
The [Developer guide](https://beaker-project.org/dev/guide/) in particular 
might be useful if you are working on Beaker.

## = BEAKER DN SETUP =

The Beaker dn branch is a fork on top of upstream Beaker that add these main features:

~~~
* Enables SLES support
* Enables Ubuntu support
* Provides a few tweaks on Fedora repos
* Provides a very ugly hack to enable CentosStream8/9 from a remote repository (temporary).
~~~

Even though beaker.dn works fairly really well, as has been **extremely** helpful to our daily development by providing automatic installations and reservations, **there isn't no guarantees whatsoever of this tweaked usage**; since it didn't go through as much testing as the real upstream Beaker -> Enjoy and use it at your own risk!

Furthermore, we have mostly used only for ppc64le guests on this; hence, feel free to contribute back to this fork with patches changing the autoyasts (SLES) and (autoinstall) Ubuntu to support other arches, as well as new harness packages to support newer versions of these distros.

Fedora COPR repository with beaker.dn binaries:
* https://copr.fedorainfracloud.org/coprs/desnesn/beaker.dn/

Quick enable:
~~~
dnf copr enable desnesn/beaker.dn
~~~

Usage and Installation instructions (README.md), as well as SRPMs code repo:
* https://github.com/desnesn/beaker.dn.rpms
