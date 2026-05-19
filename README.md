# r-makevars-variables

A throwaway R package whose `src/Makevars` prints every `make` variable
visible during `R CMD INSTALL`. CI runs the probe on `ubuntu-latest`,
`macos-latest`, and `windows-latest` with `r-version: 'release'` and
commits the raw logs to [`vars/`](vars/). The cross-platform diff is
below.

## The probe

```make
.PHONY: echo_vars
all: echo_vars
echo_vars:
	@echo "$(.VARIABLES)"
```

R's build of an installed package merges its own `Makeconf` with the
user's `src/Makevars`. Because `all:` is the first target in the merged
file, it runs before the SHLIB rules and `$(.VARIABLES)` prints every
variable currently defined — R config, compiler/linker flags, make
built-ins, and inherited environment.

Full scaffolding recipe (rig, usethis, the package-name gotcha): see
[`dev/RECIPE.md`](dev/RECIPE.md).

## Re-running

- **CI**: push to `main`, or `gh workflow run dump-makevars.yml`. The
  workflow runs `R CMD INSTALL .` on each runner and commits the per-OS
  install log back to `vars/`.
- **Locally**: `R CMD INSTALL .` on whatever platform you have. The
  variable dump appears in the install output before the compile lines.
- **Check action pins** against the latest releases: `just check-action-versions`.

## Cross-platform availability

Tables show whether each variable is set on Linux (**L**), macOS (**M**),
and Windows (**W**) during `R CMD INSTALL`. Vars that don't surface on
*any* of the three runners are omitted from a category.

After filtering CI-runner noise (`GITHUB_*`, `RUNNER_*`, `JAVA_HOME_*`,
`GOROOT_*`, `ANDROID_*`, browser-driver paths, …): linux **278** · macos **284** · windows **334**.

### R configuration

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `R_CMD` | ✓ | ✓ | ✓ |
| `R_HOME` | ✓ | ✓ | ✓ |
| `R_VERSION` | ✓ | ✓ | ✓ |
| `R_PLATFORM` | ✓ | ✓ |   |
| `R_ARCH` | ✓ | ✓ | ✓ |
| `R_OSTYPE` | ✓ | ✓ | ✓ |
| `R_INCLUDE_DIR` | ✓ | ✓ | ✓ |
| `R_SHARE_DIR` | ✓ | ✓ | ✓ |
| `R_DOC_DIR` | ✓ | ✓ | ✓ |
| `R_LIBRARY_DIR` | ✓ | ✓ | ✓ |
| `R_LIBS` | ✓ | ✓ | ✓ |
| `R_LIBS_USER` | ✓ | ✓ | ✓ |
| `R_LIBS_SITE` | ✓ | ✓ | ✓ |
| `R_PACKAGE_DIR` | ✓ | ✓ | ✓ |
| `R_PACKAGE_NAME` | ✓ | ✓ | ✓ |
| `R_INSTALL_PKG` | ✓ | ✓ | ✓ |
| `R_SESSION_TMPDIR` | ✓ | ✓ |   |
| `R_BROWSER` | ✓ | ✓ |   |
| `R_PDFVIEWER` | ✓ | ✓ |   |
| `R_PAPERSIZE` | ✓ | ✓ | ✓ |
| `R_PAPERSIZE_USER` | ✓ | ✓ |   |
| `R_PRINTCMD` | ✓ | ✓ |   |
| `R_DEFAULT_PACKAGES` | ✓ | ✓ |   |
| `R_PKGS_BASE` | ✓ | ✓ |   |
| `R_PKGS_BASE1` | ✓ | ✓ |   |
| `R_PKGS_BASE2` | ✓ | ✓ |   |
| `R_PKGS_RECOMMENDED` | ✓ | ✓ |   |
| `R_BZIPCMD` | ✓ | ✓ | ✓ |
| `R_GZIPCMD` | ✓ | ✓ | ✓ |
| `R_ZIPCMD` | ✓ | ✓ | ✓ |
| `R_UNZIPCMD` | ✓ | ✓ | ✓ |
| `R_TEXI2DVICMD` | ✓ | ✓ |   |
| `R_RD4PDF` | ✓ | ✓ | ✓ |
| `R_QPDF` |   | ✓ |   |
| `R_XTRA_CPPFLAGS` | ✓ | ✓ | ✓ |
| `R_XTRA_CFLAGS` | ✓ | ✓ | ✓ |
| `R_XTRA_CXXFLAGS` | ✓ | ✓ | ✓ |
| `R_XTRA_FFLAGS` | ✓ | ✓ | ✓ |
| `R_STRIP_SHARED_LIB` | ✓ | ✓ |   |
| `R_STRIP_STATIC_LIB` | ✓ | ✓ |   |

### C / C++ compilers and flags

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `CC` | ✓ | ✓ | ✓ |
| `CC17` | ✓ | ✓ | ✓ |
| `CC23` | ✓ | ✓ | ✓ |
| `CC90` | ✓ | ✓ | ✓ |
| `CC99` | ✓ | ✓ | ✓ |
| `CXX` | ✓ | ✓ | ✓ |
| `CXX17` | ✓ | ✓ | ✓ |
| `CXX20` | ✓ | ✓ | ✓ |
| `CXX23` | ✓ | ✓ | ✓ |
| `CXX26` | ✓ | ✓ | ✓ |
| `CFLAGS` | ✓ | ✓ | ✓ |
| `C17FLAGS` | ✓ | ✓ | ✓ |
| `C23FLAGS` | ✓ | ✓ | ✓ |
| `C90FLAGS` | ✓ | ✓ | ✓ |
| `C99FLAGS` | ✓ | ✓ | ✓ |
| `CXXFLAGS` | ✓ | ✓ | ✓ |
| `CXX17FLAGS` | ✓ | ✓ | ✓ |
| `CXX20FLAGS` | ✓ | ✓ | ✓ |
| `CXX23FLAGS` | ✓ | ✓ | ✓ |
| `CXX26FLAGS` | ✓ | ✓ | ✓ |
| `CXX17STD` | ✓ | ✓ | ✓ |
| `CXX20STD` | ✓ | ✓ | ✓ |
| `CXX23STD` | ✓ | ✓ | ✓ |
| `CXX26STD` | ✓ | ✓ | ✓ |
| `CPICFLAGS` | ✓ | ✓ | ✓ |
| `CXXPICFLAGS` | ✓ | ✓ | ✓ |
| `CXX17PICFLAGS` | ✓ | ✓ | ✓ |
| `CXX20PICFLAGS` | ✓ | ✓ | ✓ |
| `CXX23PICFLAGS` | ✓ | ✓ | ✓ |
| `CXX26PICFLAGS` | ✓ | ✓ | ✓ |
| `CPP` | ✓ | ✓ | ✓ |
| `CPPFLAGS` | ✓ | ✓ | ✓ |
| `C_VISIBILITY` | ✓ | ✓ | ✓ |
| `CXX_VISIBILITY` | ✓ | ✓ |   |
| `ALL_CFLAGS` | ✓ | ✓ | ✓ |
| `ALL_CPPFLAGS` | ✓ | ✓ | ✓ |
| `ALL_CXXFLAGS` | ✓ | ✓ | ✓ |

### Fortran

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `FC` | ✓ | ✓ | ✓ |
| `F77` | ✓ | ✓ | ✓ |
| `FCFLAGS` | ✓ | ✓ | ✓ |
| `FFLAGS` | ✓ | ✓ | ✓ |
| `F77FLAGS` | ✓ | ✓ | ✓ |
| `FPICFLAGS` | ✓ | ✓ | ✓ |
| `FPIEFLAGS` | ✓ | ✓ |   |
| `FLIBS` | ✓ | ✓ | ✓ |
| `FCLIBS_XTRA` | ✓ | ✓ | ✓ |
| `P_FCFLAGS` | ✓ | ✓ | ✓ |
| `SAFE_FFLAGS` | ✓ | ✓ | ✓ |
| `F_VISIBILITY` | ✓ | ✓ | ✓ |
| `ALL_FFLAGS` | ✓ | ✓ | ✓ |
| `ALL_FCFLAGS` | ✓ | ✓ | ✓ |
| `LTO_FC` | ✓ | ✓ |   |
| `LTO_FC_OPT` | ✓ | ✓ |   |

### Objective-C / Objective-C++

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `OBJC` | ✓ | ✓ | ✓ |
| `OBJCXX` | ✓ | ✓ | ✓ |
| `OBJCFLAGS` | ✓ | ✓ | ✓ |
| `OBJC_LIBS` | ✓ | ✓ | ✓ |
| `ALL_OBJCFLAGS` | ✓ | ✓ | ✓ |
| `ALL_OBJCXXFLAGS` | ✓ | ✓ | ✓ |

### Shared library build (`SHLIB_*`)

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `SHLIB` | ✓ | ✓ | ✓ |
| `SHLIB_EXT` | ✓ | ✓ | ✓ |
| `SHLIB_LD` | ✓ | ✓ | ✓ |
| `SHLIB_LDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_LDFLAGS_R` | ✓ | ✓ |   |
| `SHLIB_LIBADD` | ✓ | ✓ | ✓ |
| `SHLIB_LINK` | ✓ | ✓ | ✓ |
| `SHLIB_CFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_CXXFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_CXXLD` | ✓ | ✓ | ✓ |
| `SHLIB_CXXLDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_CXX17LD` | ✓ | ✓ | ✓ |
| `SHLIB_CXX17LDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_CXX20LD` | ✓ | ✓ | ✓ |
| `SHLIB_CXX20LDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_CXX23LD` | ✓ | ✓ | ✓ |
| `SHLIB_CXX23LDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_CXX26LD` | ✓ | ✓ | ✓ |
| `SHLIB_CXX26LDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_FCLD` | ✓ | ✓ | ✓ |
| `SHLIB_FCLDFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_FFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_OPENMP_CFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_OPENMP_CXXFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_OPENMP_FFLAGS` | ✓ | ✓ | ✓ |
| `SHLIB_OPENMP_FCFLAGS` |   |   | ✓ |
| `SHLIB_PTHREAD_FLAGS` |   |   | ✓ |

### Dynamic library (macOS `.dylib`)

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `DYLIB_LD` | ✓ | ✓ | ✓ |
| `DYLIB_LDFLAGS` | ✓ | ✓ | ✓ |
| `DYLIB_LINK` | ✓ | ✓ | ✓ |
| `DYLIB_EXT` | ✓ | ✓ | ✓ |

### Linker, libraries, LTO

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `LD` | ✓ | ✓ | ✓ |
| `LDFLAGS` | ✓ | ✓ | ✓ |
| `MAIN_LD` | ✓ | ✓ |   |
| `MAIN_LDFLAGS` | ✓ | ✓ |   |
| `MAIN_LINK` | ✓ | ✓ |   |
| `LIBS` | ✓ | ✓ | ✓ |
| `LIBM` | ✓ | ✓ | ✓ |
| `LIBR` | ✓ | ✓ | ✓ |
| `LIBR0` | ✓ | ✓ |   |
| `LIBR1` | ✓ | ✓ |   |
| `LIBnn` | ✓ | ✓ | ✓ |
| `LIBINTL` | ✓ | ✓ | ✓ |
| `LIBTOOL` | ✓ | ✓ | ✓ |
| `ALL_LIBS` | ✓ | ✓ | ✓ |
| `LTO` | ✓ | ✓ | ✓ |
| `LTO_OPT` | ✓ | ✓ | ✓ |
| `LTO_LD` | ✓ | ✓ |   |
| `STATIC_LIBR` | ✓ | ✓ | ✓ |
| `STRIP_SHARED_LIB` | ✓ | ✓ | ✓ |
| `STRIP_STATIC_LIB` | ✓ | ✓ | ✓ |

### Binutils / archive

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `AR` | ✓ | ✓ | ✓ |
| `ARFLAGS` | ✓ | ✓ | ✓ |
| `RANLIB` | ✓ | ✓ | ✓ |
| `NM` | ✓ | ✓ | ✓ |
| `AS` | ✓ | ✓ | ✓ |
| `LN_S` | ✓ | ✓ |   |

### Numerical / sanitizer libs

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `BLAS_LIBS` | ✓ | ✓ | ✓ |
| `LAPACK_LIBS` | ✓ | ✓ | ✓ |
| `SAN_LIBS` | ✓ | ✓ |   |
| `ZLIB_LIBS` |   |   | ✓ |

### Java

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `JAVA` | ✓ | ✓ | ✓ |
| `JAVA_HOME` | ✓ | ✓ | ✓ |
| `JAVA_CPPFLAGS` | ✓ | ✓ | ✓ |
| `JAVA_LIBS` | ✓ | ✓ | ✓ |
| `JAVA_LD_LIBRARY_PATH` | ✓ | ✓ |   |
| `JAVAC` | ✓ | ✓ | ✓ |
| `JAVAH` | ✓ | ✓ | ✓ |
| `JAR` | ✓ | ✓ | ✓ |

### Tcl/Tk

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `TCLTK_CPPFLAGS` | ✓ | ✓ | ✓ |
| `TCLTK_LIBS` | ✓ | ✓ | ✓ |

### macOS frameworks

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `FOUNDATION_CPPFLAGS` | ✓ | ✓ | ✓ |
| `FOUNDATION_LIBS` | ✓ | ✓ | ✓ |

### TeX / documentation toolchain

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `TEX` | ✓ | ✓ | ✓ |
| `TEXI2DVI` | ✓ | ✓ | ✓ |
| `TEXINPUTS` | ✓ | ✓ | ✓ |
| `BSTINPUTS` | ✓ | ✓ | ✓ |
| `BIBINPUTS` | ✓ | ✓ | ✓ |
| `TANGLE` | ✓ | ✓ | ✓ |
| `WEAVE` | ✓ | ✓ | ✓ |
| `CTANGLE` | ✓ | ✓ | ✓ |
| `CWEAVE` | ✓ | ✓ | ✓ |
| `MAKEINFO` | ✓ | ✓ | ✓ |

### LEX / YACC

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `LEX` | ✓ | ✓ | ✓ |
| `LEX.l` | ✓ | ✓ | ✓ |
| `LEX.m` | ✓ | ✓ | ✓ |
| `YACC` | ✓ | ✓ | ✓ |
| `YACC.y` | ✓ | ✓ | ✓ |
| `YACC.m` | ✓ | ✓ | ✓ |

### Compile / link / preprocess pattern rules

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `COMPILE.c` | ✓ | ✓ | ✓ |
| `COMPILE.cc` | ✓ | ✓ | ✓ |
| `COMPILE.cpp` | ✓ | ✓ | ✓ |
| `COMPILE.C` | ✓ | ✓ | ✓ |
| `COMPILE.S` | ✓ | ✓ | ✓ |
| `COMPILE.s` | ✓ | ✓ | ✓ |
| `COMPILE.f` | ✓ | ✓ | ✓ |
| `COMPILE.F` | ✓ | ✓ | ✓ |
| `COMPILE.def` | ✓ | ✓ | ✓ |
| `COMPILE.m` | ✓ | ✓ | ✓ |
| `COMPILE.mod` | ✓ | ✓ | ✓ |
| `COMPILE.p` | ✓ | ✓ | ✓ |
| `COMPILE.r` | ✓ | ✓ | ✓ |
| `LINK.c` | ✓ | ✓ | ✓ |
| `LINK.cc` | ✓ | ✓ | ✓ |
| `LINK.cpp` | ✓ | ✓ | ✓ |
| `LINK.C` | ✓ | ✓ | ✓ |
| `LINK.f` | ✓ | ✓ | ✓ |
| `LINK.F` | ✓ | ✓ | ✓ |
| `LINK.m` | ✓ | ✓ | ✓ |
| `LINK.o` | ✓ | ✓ | ✓ |
| `LINK.p` | ✓ | ✓ | ✓ |
| `LINK.r` | ✓ | ✓ | ✓ |
| `LINK.S` | ✓ | ✓ | ✓ |
| `LINK.s` | ✓ | ✓ | ✓ |
| `PREPROCESS.r` | ✓ | ✓ | ✓ |
| `PREPROCESS.S` | ✓ | ✓ | ✓ |
| `PREPROCESS.F` | ✓ | ✓ | ✓ |

### Misc. build tools

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `SED` | ✓ | ✓ | ✓ |
| `TAR` | ✓ | ✓ | ✓ |
| `RM` | ✓ | ✓ | ✓ |
| `ECHO` | ✓ | ✓ | ✓ |
| `ECHO_C` | ✓ | ✓ | ✓ |
| `ECHO_N` | ✓ | ✓ | ✓ |
| `ECHO_T` | ✓ | ✓ | ✓ |
| `GET` | ✓ | ✓ | ✓ |
| `CO` | ✓ | ✓ | ✓ |
| `COFLAGS` | ✓ | ✓ | ✓ |
| `CHECKOUT,v` | ✓ | ✓ | ✓ |
| `MKINSTALLDIRS` | ✓ | ✓ | ✓ |
| `M2C` | ✓ | ✓ | ✓ |
| `LINT` | ✓ | ✓ | ✓ |
| `LINT.c` | ✓ | ✓ | ✓ |
| `PC` | ✓ | ✓ | ✓ |
| `PAGER` | ✓ | ✓ |   |
| `EDITOR` | ✓ | ✓ |   |
| `OUTPUT_OPTION` | ✓ | ✓ | ✓ |

### `make` built-in variables

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `MAKE` | ✓ | ✓ | ✓ |
| `MAKEFLAGS` | ✓ | ✓ | ✓ |
| `MAKELEVEL` | ✓ | ✓ | ✓ |
| `MAKEFILES` | ✓ | ✓ | ✓ |
| `MAKEFILEPATH` |   | ✓ |   |
| `MAKEFILE_LIST` | ✓ | ✓ | ✓ |
| `MAKE_COMMAND` | ✓ | ✓ | ✓ |
| `MAKE_VERSION` | ✓ | ✓ | ✓ |
| `MFLAGS` | ✓ | ✓ | ✓ |
| `MAKEOVERRIDES` | ✓ | ✓ | ✓ |
| `GNUMAKE` |   | ✓ |   |
| `GNUMAKEFLAGS` | ✓ |   | ✓ |
| `MAKE_HOST` | ✓ |   | ✓ |
| `.FEATURES` | ✓ | ✓ | ✓ |
| `.LIBPATTERNS` | ✓ | ✓ | ✓ |
| `.DEFAULT_GOAL` | ✓ | ✓ | ✓ |
| `.VARIABLES` | ✓ | ✓ | ✓ |
| `.RECIPEPREFIX` | ✓ |   | ✓ |
| `.SHELLFLAGS` | ✓ |   | ✓ |
| `.LOADED` | ✓ |   | ✓ |
| `.INCLUDE_DIRS` | ✓ |   | ✓ |
| `SUFFIXES` | ✓ | ✓ | ✓ |
| `CURDIR` | ✓ | ✓ | ✓ |
| `SHELL` | ✓ | ✓ | ✓ |
| `OBJECTS` | ✓ | ✓ | ✓ |
| `-*-command-variables-*-` | ✓ | ✓ | ✓ |

### `make` automatic-variable dir/file suffixes

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `@D` | ✓ | ✓ | ✓ |
| `@F` | ✓ | ✓ | ✓ |
| `%D` | ✓ | ✓ | ✓ |
| `%F` | ✓ | ✓ | ✓ |
| `*D` | ✓ | ✓ | ✓ |
| `*F` | ✓ | ✓ | ✓ |
| `<D` | ✓ | ✓ | ✓ |
| `<F` | ✓ | ✓ | ✓ |
| `?D` | ✓ | ✓ | ✓ |
| `?F` | ✓ | ✓ | ✓ |
| `+D` | ✓ | ✓ | ✓ |
| `+F` | ✓ | ✓ | ✓ |
| `^D` | ✓ | ✓ | ✓ |
| `^F` | ✓ | ✓ | ✓ |

### Common POSIX environment

| Variable | L | M | W |
| --- | :-: | :-: | :-: |
| `PATH` | ✓ | ✓ | ✓ |
| `HOME` | ✓ | ✓ | ✓ |
| `USER` | ✓ | ✓ |   |
| `LOGNAME` | ✓ | ✓ |   |
| `SHLVL` | ✓ | ✓ | ✓ |
| `TMPDIR` |   | ✓ | ✓ |
| `PWD` | ✓ | ✓ | ✓ |
| `_` |   | ✓ | ✓ |
| `LANG` | ✓ | ✓ |   |
| `LC_COLLATE` | ✓ | ✓ | ✓ |

### Platform extras

Variables present in CI logs that don't fit the categories above —
mostly Rtools/mingw-only tooling on Windows and a handful of macOS
framework paths.

**Linux + Windows** (1)

```
PSModulePath
```

**Windows only** (84)

```
!D:, ADDQU, ALLUSERSPROFILE, APPDATA, BASE, BINDIR, BINPREF, CAT, CCBASE,
COMMONPROGRAMFILES, COMPILED_BY, COMPUTERNAME, COMSPEC, CP, CXXCPP,
CommonProgramFiles(x86), CommonProgramW6432, DEBUGFLAG, DLL, DLLFLAGS,
DLLTOOL, DLLTOOLFLAGS, DT_ARCH, FDEBUGFLAG, GCM_INTERACTIVE, GRAPHAPP_LIB,
HOMEDRIVE, HOMEPATH, IMPDIR, LINKER, LINKFLAGS, LLVMPREF, LOCALAPPDATA,
LOCAL_CPPFLAGS, LOCAL_LIBS, LOCAL_SOFT, LOGONSERVER, MINGW_PREFIX, MKDIR,
MSYS2_ENV_CONV_EXCL, M_ARCH, NM_FILTER, NUMBER_OF_PROCESSORS, OBJDUMP, OS,
PATHEXT, PKG_CONFIG, PROCESSOR_ARCHITECTURE, PROCESSOR_IDENTIFIER,
PROCESSOR_LEVEL, PROCESSOR_REVISION, PROGRAMFILES, PROMPT,
PSModuleAnalysisCachePath, PUBLIC, ProgramData, ProgramFiles(x86),
ProgramW6432, RC_ARCH, RESCOMP, R_ARCH_BIN, R_COMPILED_BY, R_INSTALLER_BUILD,
R_RTOOLS45_PATH, R_TOOLS_SOFT, R_USER, SORT, SYMPAT, SYSTEMDRIVE, SYSTEMROOT,
TAR_OPTIONS, TCLBIN, TCL_HOME, TCL_VERSION, TEMP, TERM, TMP, USERDOMAIN,
USERDOMAIN_ROAMINGPROFILE, USERNAME, USERPROFILE, USE_LLVM, WIN, WINDIR
```

**macOS only** (8)

```
INFOPATH, LC_ALL, LC_CTYPE, MANPATH, SSH_AUTH_SOCK, XPC_FLAGS,
XPC_SERVICE_NAME, __CF_USER_TEXT_ENCODING
```

## Layout

- [`src/Makevars`](src/Makevars) — the probe (4 lines).
- [`vars/`](vars/) — raw `R CMD INSTALL` logs per OS, refreshed by CI.
- [`.github/workflows/dump-makevars.yml`](.github/workflows/dump-makevars.yml) — the dump+commit workflow.
- [`justfile`](justfile) — `gh-latest` and `check-action-versions` recipes.
- [`dev/RECIPE.md`](dev/RECIPE.md) — original scaffolding lab notes.
