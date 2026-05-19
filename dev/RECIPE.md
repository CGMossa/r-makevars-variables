# Minimal R package + Makevars variable dump

Goal: bootstrap a throwaway R package with a C stub and dump every
variable that `R CMD INSTALL` makes visible to `src/Makevars`.


```sh
# 1. Empty working directory with an ASCII, letter-led, no-underscore name
mkdir rpkgk68 && cd rpkgk68

# 2. (optional) pin an R version
rig default 4.6

# 3. Scaffold the package + license + src/ from inside R
R --no-save <<'EOF'
usethis::create_package(".", check = FALSE)
usethis::use_mit_license("Mossa Merhi Reimert")
usethis::use_c("stub")
EOF
```

> **Naming gotcha.** `usethis::create_package(".")` derives the package
> name from the *directory* name and rejects underscores (CRAN rule:
> ASCII letters, digits, `.`; must start with a letter; min 2 chars; no
> trailing `.`). Either name the directory `rpkgk68` from the start, or
> create it with `check = FALSE` and edit the `Package:` field in
> `DESCRIPTION` afterwards.

Then drop a probe target into `src/Makevars`:

```make
.PHONY: echo_vars

all: echo_vars

echo_vars:
	@echo "$(.VARIABLES)"
```

Build it:

```sh
R CMD INSTALL .
```

The `all:` target runs before R's own SHLIB rules, so the list of every
variable currently defined in `make`'s namespace is printed at the top
of the install log.

---

## Variables emitted by `$(.VARIABLES)`

Categorised below. Every token from the dump is included.

### R configuration

`R_CMD`, `R_HOME`, `R_VERSION`, `R_PLATFORM`, `R_ARCH`, `R_OSTYPE`,
`R_INCLUDE_DIR`, `R_SHARE_DIR`, `R_DOC_DIR`, `R_LIBRARY_DIR`,
`R_LIBS`, `R_LIBS_USER`, `R_LIBS_SITE`,
`R_PACKAGE_DIR`, `R_PACKAGE_NAME`, `R_INSTALL_PKG`, `R_SESSION_TMPDIR`,
`R_BROWSER`, `R_PDFVIEWER`, `R_PAPERSIZE`, `R_PAPERSIZE_USER`,
`R_PRINTCMD`, `R_DEFAULT_PACKAGES`,
`R_PKGS_BASE`, `R_PKGS_BASE1`, `R_PKGS_BASE2`, `R_PKGS_RECOMMENDED`,
`R_BZIPCMD`, `R_GZIPCMD`, `R_ZIPCMD`, `R_UNZIPCMD`,
`R_TEXI2DVICMD`, `R_RD4PDF`, `R_QPDF`,
`R_XTRA_CPPFLAGS`, `R_XTRA_CFLAGS`, `R_XTRA_CXXFLAGS`, `R_XTRA_FFLAGS`,
`R_STRIP_SHARED_LIB`, `R_STRIP_STATIC_LIB`

### C / C++ compilers and flags

`CC`, `CC17`, `CC23`, `CC90`, `CC99`,
`CXX`, `CXX17`, `CXX20`, `CXX23`, `CXX26`,
`CFLAGS`, `C17FLAGS`, `C23FLAGS`, `C90FLAGS`, `C99FLAGS`,
`CXXFLAGS`, `CXX11FLAGS`, `CXX17FLAGS`, `CXX20FLAGS`, `CXX23FLAGS`, `CXX26FLAGS`,
`CXX17STD`, `CXX20STD`, `CXX23STD`, `CXX26STD`,
`CPICFLAGS`,
`CXXPICFLAGS`, `CXX17PICFLAGS`, `CXX20PICFLAGS`, `CXX23PICFLAGS`, `CXX26PICFLAGS`,
`CPP`, `CPPFLAGS`,
`C_VISIBILITY`, `CXX_VISIBILITY`,
`ALL_CFLAGS`, `ALL_CPPFLAGS`, `ALL_CXXFLAGS`

### Fortran

`FC`, `F77`, `FCFLAGS`, `FFLAGS`, `F77FLAGS`,
`FPICFLAGS`, `FPIEFLAGS`,
`FLIBS`, `FCLIBS_XTRA`,
`P_FCFLAGS`, `SAFE_FFLAGS`, `F_VISIBILITY`,
`ALL_FFLAGS`, `ALL_FCFLAGS`,
`LTO_FC`, `LTO_FC_OPT`

### Objective-C / Objective-C++

`OBJC`, `OBJCXX`, `OBJCFLAGS`, `OBJC_LIBS`,
`ALL_OBJCFLAGS`, `ALL_OBJCXXFLAGS`

### Shared library build (`SHLIB_*`)

`SHLIB`, `SHLIB_EXT`,
`SHLIB_LD`, `SHLIB_LDFLAGS`, `SHLIB_LDFLAGS_R`, `SHLIB_LIBADD`, `SHLIB_LINK`,
`SHLIB_CFLAGS`, `SHLIB_CXXFLAGS`, `SHLIB_CXXLD`, `SHLIB_CXXLDFLAGS`,
`SHLIB_CXX17LD`, `SHLIB_CXX17LDFLAGS`,
`SHLIB_CXX20LD`, `SHLIB_CXX20LDFLAGS`,
`SHLIB_CXX23LD`, `SHLIB_CXX23LDFLAGS`,
`SHLIB_CXX26LD`, `SHLIB_CXX26LDFLAGS`,
`SHLIB_FCLD`, `SHLIB_FCLDFLAGS`, `SHLIB_FFLAGS`,
`SHLIB_OPENMP_CFLAGS`, `SHLIB_OPENMP_CXXFLAGS`, `SHLIB_OPENMP_FFLAGS`

### Dynamic library (macOS `.dylib`)

`DYLIB_LD`, `DYLIB_LDFLAGS`, `DYLIB_LINK`, `DYLIB_EXT`

### Linker, libraries, LTO

`LD`, `LDFLAGS`,
`MAIN_LD`, `MAIN_LDFLAGS`, `MAIN_LINK`,
`LIBS`, `LIBM`, `LIBR`, `LIBR0`, `LIBR1`, `LIBnn`, `LIBINTL`, `LIBTOOL`,
`ALL_LIBS`,
`LTO`, `LTO_OPT`, `LTO_LD`,
`STATIC_LIBR`,
`STRIP_SHARED_LIB`, `STRIP_STATIC_LIB`

### Binutils / archive

`AR`, `ARFLAGS`, `RANLIB`, `NM`, `AS`, `LN_S`

### Numerical / sanitizer libs

`BLAS_LIBS`, `LAPACK_LIBS`, `SAN_LIBS`

### Java

`JAVA`, `JAVA_HOME`, `JAVA_CPPFLAGS`, `JAVA_LIBS`, `JAVA_LD_LIBRARY_PATH`,
`JAVAC`, `JAVAH`, `JAR`

### Tcl/Tk

`TCLTK_CPPFLAGS`, `TCLTK_LIBS`

### macOS frameworks

`FOUNDATION_CPPFLAGS`, `FOUNDATION_LIBS`

### TeX / documentation toolchain

`TEX`, `TEXI2DVI`, `TEXINPUTS`, `BSTINPUTS`, `BIBINPUTS`,
`TANGLE`, `WEAVE`, `CTANGLE`, `CWEAVE`, `MAKEINFO`

### LEX / YACC

`LEX`, `LEX.l`, `LEX.m`, `YACC`, `YACC.y`, `YACC.m`

### Pattern rules (per language)

Compile:
`COMPILE.c`, `COMPILE.cc`, `COMPILE.cpp`, `COMPILE.C`,
`COMPILE.S`, `COMPILE.s`,
`COMPILE.f`, `COMPILE.F`,
`COMPILE.def`, `COMPILE.m`, `COMPILE.mod`, `COMPILE.p`, `COMPILE.r`

Link:
`LINK.c`, `LINK.cc`, `LINK.cpp`, `LINK.C`,
`LINK.f`, `LINK.F`, `LINK.m`, `LINK.o`, `LINK.p`, `LINK.r`,
`LINK.S`, `LINK.s`

Preprocess:
`PREPROCESS.r`, `PREPROCESS.S`, `PREPROCESS.F`

### Misc. tools

`SED`, `TAR`, `RM`, `ECHO`, `ECHO_C`, `ECHO_N`, `ECHO_T`,
`GET`, `CO`, `COFLAGS`, `CHECKOUT,v`,
`MKINSTALLDIRS`, `M2C`,
`LINT`, `LINT.c`,
`PC`, `PAGER`, `EDITOR`, `OUTPUT_OPTION`

### `make` itself (built-in vars)

`MAKE`, `MAKEFLAGS`, `MAKELEVEL`, `MAKEFILES`, `MAKEFILEPATH`,
`MAKEFILE_LIST`, `MAKE_COMMAND`, `MAKE_VERSION`, `MFLAGS`,
`MAKEOVERRIDES`, `GNUMAKE`,
`.FEATURES`, `.LIBPATTERNS`, `.DEFAULT_GOAL`, `.VARIABLES`,
`SUFFIXES`, `CURDIR`, `SHELL`, `OBJECTS`,
`-*-command-variables-*-`

### `make` automatic-variable dir/file suffixes

`@D`, `@F` (target), `%D`, `%F` (archive member),
`*D`, `*F` (stem), `<D`, `<F` (first prereq),
`?D`, `?F` (newer prereqs), `+D`, `+F` (prereqs w/ duplicates),
`^D`, `^F` (prereqs deduped)

### Shell / general OS environment

`PATH`, `HOME`, `USER`, `LOGNAME`, `SHLVL`, `TMPDIR`, `PWD`, `_`,
`TERM`, `TERM_PROGRAM`, `TERM_PROGRAM_VERSION`, `COLORTERM`,
`LANG`, `LC_COLLATE`, `LESS`,
`LSCOLORS`, `LS_COLORS`,
`DISPLAY`, `MANPATH`, `INFOPATH`, `FPATH`,
`ZSH`, `SSH_AUTH_SOCK`, `LIBGL_ALWAYS_SOFTWARE`

### macOS-specific environment

`__CFBundleIdentifier`, `__CF_USER_TEXT_ENCODING`,
`XPC_FLAGS`, `XPC_SERVICE_NAME`, `COMMAND_MODE`,
`SECURITYSESSIONID`, `LaunchInstanceID`, `OSLogRateLimit`

### WezTerm

`WEZTERM_UNIX_SOCKET`, `WEZTERM_CONFIG_DIR`, `WEZTERM_CONFIG_FILE`,
`WEZTERM_EXECUTABLE`, `WEZTERM_EXECUTABLE_DIR`, `WEZTERM_PANE`

### Atuin (shell history)

`ATUIN_SESSION`, `ATUIN_HISTORY_ID`, `ATUIN_SHLVL`, `ATUIN_TMUX_POPUP`

### Starship prompt

`STARSHIP_SESSION_KEY`, `STARSHIP_SHELL`

### Package managers

`HOMEBREW_PREFIX`, `HOMEBREW_CELLAR`, `HOMEBREW_REPOSITORY`,
`BUN_INSTALL`

