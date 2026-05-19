#!/usr/bin/env python3
"""Build README.md: probe explanation + cross-platform availability table
keyed off the category structure in dev/RECIPE.md."""
import re
from pathlib import Path

LOGS = {
    "L": Path("vars/install-ubuntu-latest.log"),
    "M": Path("vars/install-macos-latest.log"),
    "W": Path("vars/install-windows-latest.log"),
}

NOISE_PREFIXES = (
    "GITHUB_", "RUNNER_", "ACTIONS_", "JAVA_HOME_", "GOROOT_",
    "ANDROID_", "XCODE_", "PIPX_", "AZURE_", "GRADLE_", "POWERSHELL_",
    "DOTNET_", "HOMEBREW_", "GHCUP_", "BOOTSTRAP_HASKELL", "RTOOLS45",
    "PG", "AZ_DEVOPS_", "NUNIT",
)
NOISE_EXACT = {
    "ImageOS", "ImageVersion", "CI", "CONDA", "RSPM", "NOT_CRAN",
    "ACCEPT_EULA", "PKGCACHE_HTTP_VERSION", "DEBIAN_FRONTEND",
    "AGENT_TOOLSDIRECTORY", "SWIFT_PATH", "NVM_DIR", "SGX_AESM_ADDR",
    "VCPKG_INSTALLATION_ROOT", "RENV_CONFIG_REPOS_OVERRIDE",
    "ENABLE_RUNNER_TRACING", "USE_BAZEL_FALLBACK_VERSION",
    "_R_CHECK_SYSTEM_CLOCK_", "_R_INSTALL_TIME_PATCHES_",
    "CHROMEWEBDRIVER", "GECKOWEBDRIVER", "EDGEWEBDRIVER",
    "ChromeWebDriver", "GeckoWebDriver", "EdgeWebDriver", "IEWebDriver",
    "SELENIUM_JAR_PATH", "CHROME_BIN", "ANT_HOME", "M2_REPO", "M2",
    "PHPROOT", "MAVEN_OPTS", "SBT_HOME", "COBERTURA_HOME",
    "JOURNAL_STREAM", "INVOCATION_ID", "SYSTEMD_EXEC_PID",
    "MEMORY_PRESSURE_WATCH", "MEMORY_PRESSURE_WRITE", "TZ",
    "XDG_CONFIG_HOME", "XDG_RUNTIME_DIR", "LD_LIBRARY_PATH",
    "RCT_NO_LAUNCH_PACKAGER", "VM_ASSETS", "ChocolateyInstall", "WIX",
    "DriverData", "npm_config_prefix", "CABAL_DIR", "CURL_CA_BUNDLE",
    "DYLD_FALLBACK_LIBRARY_PATH",
}

def extract_vars(text):
    for line in text.splitlines():
        toks = line.split()
        if ".VARIABLES" in toks and len(toks) > 50:
            return set(toks)
    raise RuntimeError("dump line not found")

def is_noise(v):
    return v in NOISE_EXACT or any(v.startswith(p) for p in NOISE_PREFIXES)

per_os = {k: extract_vars(p.read_text()) for k, p in LOGS.items()}

# Category structure: ordered list of (heading, [vars]).
# Pulled from dev/RECIPE.md but pruned of personal-env categories that
# only ever surface on a local macOS workstation.
CATS = [
    ("R configuration", [
        "R_CMD","R_HOME","R_VERSION","R_PLATFORM","R_ARCH","R_OSTYPE",
        "R_INCLUDE_DIR","R_SHARE_DIR","R_DOC_DIR","R_LIBRARY_DIR",
        "R_LIBS","R_LIBS_USER","R_LIBS_SITE",
        "R_PACKAGE_DIR","R_PACKAGE_NAME","R_INSTALL_PKG","R_SESSION_TMPDIR",
        "R_BROWSER","R_PDFVIEWER","R_PAPERSIZE","R_PAPERSIZE_USER",
        "R_PRINTCMD","R_DEFAULT_PACKAGES",
        "R_PKGS_BASE","R_PKGS_BASE1","R_PKGS_BASE2","R_PKGS_RECOMMENDED",
        "R_BZIPCMD","R_GZIPCMD","R_ZIPCMD","R_UNZIPCMD",
        "R_TEXI2DVICMD","R_RD4PDF","R_QPDF",
        "R_XTRA_CPPFLAGS","R_XTRA_CFLAGS","R_XTRA_CXXFLAGS","R_XTRA_FFLAGS",
        "R_STRIP_SHARED_LIB","R_STRIP_STATIC_LIB",
    ]),
    ("C / C++ compilers and flags", [
        "CC","CC17","CC23","CC90","CC99",
        "CXX","CXX17","CXX20","CXX23","CXX26",
        "CFLAGS","C17FLAGS","C23FLAGS","C90FLAGS","C99FLAGS",
        "CXXFLAGS","CXX11FLAGS","CXX17FLAGS","CXX20FLAGS","CXX23FLAGS","CXX26FLAGS",
        "CXX17STD","CXX20STD","CXX23STD","CXX26STD",
        "CPICFLAGS",
        "CXXPICFLAGS","CXX17PICFLAGS","CXX20PICFLAGS","CXX23PICFLAGS","CXX26PICFLAGS",
        "CPP","CPPFLAGS",
        "C_VISIBILITY","CXX_VISIBILITY",
        "ALL_CFLAGS","ALL_CPPFLAGS","ALL_CXXFLAGS",
    ]),
    ("Fortran", [
        "FC","F77","FCFLAGS","FFLAGS","F77FLAGS",
        "FPICFLAGS","FPIEFLAGS","FLIBS","FCLIBS_XTRA",
        "P_FCFLAGS","SAFE_FFLAGS","F_VISIBILITY",
        "ALL_FFLAGS","ALL_FCFLAGS",
        "LTO_FC","LTO_FC_OPT",
    ]),
    ("Objective-C / Objective-C++", [
        "OBJC","OBJCXX","OBJCFLAGS","OBJC_LIBS",
        "ALL_OBJCFLAGS","ALL_OBJCXXFLAGS",
    ]),
    ("Shared library build (`SHLIB_*`)", [
        "SHLIB","SHLIB_EXT",
        "SHLIB_LD","SHLIB_LDFLAGS","SHLIB_LDFLAGS_R","SHLIB_LIBADD","SHLIB_LINK",
        "SHLIB_CFLAGS","SHLIB_CXXFLAGS","SHLIB_CXXLD","SHLIB_CXXLDFLAGS",
        "SHLIB_CXX17LD","SHLIB_CXX17LDFLAGS",
        "SHLIB_CXX20LD","SHLIB_CXX20LDFLAGS",
        "SHLIB_CXX23LD","SHLIB_CXX23LDFLAGS",
        "SHLIB_CXX26LD","SHLIB_CXX26LDFLAGS",
        "SHLIB_FCLD","SHLIB_FCLDFLAGS","SHLIB_FFLAGS",
        "SHLIB_OPENMP_CFLAGS","SHLIB_OPENMP_CXXFLAGS","SHLIB_OPENMP_FFLAGS",
        "SHLIB_OPENMP_FCFLAGS","SHLIB_PTHREAD_FLAGS",
    ]),
    ("Dynamic library (macOS `.dylib`)", [
        "DYLIB_LD","DYLIB_LDFLAGS","DYLIB_LINK","DYLIB_EXT",
    ]),
    ("Linker, libraries, LTO", [
        "LD","LDFLAGS",
        "MAIN_LD","MAIN_LDFLAGS","MAIN_LINK",
        "LIBS","LIBM","LIBR","LIBR0","LIBR1","LIBnn","LIBINTL","LIBTOOL",
        "ALL_LIBS",
        "LTO","LTO_OPT","LTO_LD",
        "STATIC_LIBR",
        "STRIP_SHARED_LIB","STRIP_STATIC_LIB",
    ]),
    ("Binutils / archive", [
        "AR","ARFLAGS","RANLIB","NM","AS","LN_S",
    ]),
    ("Numerical / sanitizer libs", [
        "BLAS_LIBS","LAPACK_LIBS","SAN_LIBS","ZLIB_LIBS",
    ]),
    ("Java", [
        "JAVA","JAVA_HOME","JAVA_CPPFLAGS","JAVA_LIBS","JAVA_LD_LIBRARY_PATH",
        "JAVAC","JAVAH","JAR",
    ]),
    ("Tcl/Tk", [
        "TCLTK_CPPFLAGS","TCLTK_LIBS",
    ]),
    ("macOS frameworks", [
        "FOUNDATION_CPPFLAGS","FOUNDATION_LIBS",
    ]),
    ("TeX / documentation toolchain", [
        "TEX","TEXI2DVI","TEXINPUTS","BSTINPUTS","BIBINPUTS",
        "TANGLE","WEAVE","CTANGLE","CWEAVE","MAKEINFO",
    ]),
    ("LEX / YACC", [
        "LEX","LEX.l","LEX.m","YACC","YACC.y","YACC.m",
    ]),
    ("Compile / link / preprocess pattern rules", [
        "COMPILE.c","COMPILE.cc","COMPILE.cpp","COMPILE.C",
        "COMPILE.S","COMPILE.s","COMPILE.f","COMPILE.F",
        "COMPILE.def","COMPILE.m","COMPILE.mod","COMPILE.p","COMPILE.r",
        "LINK.c","LINK.cc","LINK.cpp","LINK.C",
        "LINK.f","LINK.F","LINK.m","LINK.o","LINK.p","LINK.r",
        "LINK.S","LINK.s",
        "PREPROCESS.r","PREPROCESS.S","PREPROCESS.F",
    ]),
    ("Misc. build tools", [
        "SED","TAR","RM","ECHO","ECHO_C","ECHO_N","ECHO_T",
        "GET","CO","COFLAGS","CHECKOUT,v",
        "MKINSTALLDIRS","M2C",
        "LINT","LINT.c",
        "PC","PAGER","EDITOR","OUTPUT_OPTION",
    ]),
    ("`make` built-in variables", [
        "MAKE","MAKEFLAGS","MAKELEVEL","MAKEFILES","MAKEFILEPATH",
        "MAKEFILE_LIST","MAKE_COMMAND","MAKE_VERSION","MFLAGS",
        "MAKEOVERRIDES","GNUMAKE","GNUMAKEFLAGS","MAKE_HOST",
        ".FEATURES",".LIBPATTERNS",".DEFAULT_GOAL",".VARIABLES",
        ".RECIPEPREFIX",".SHELLFLAGS",".LOADED",".INCLUDE_DIRS",
        "SUFFIXES","CURDIR","SHELL","OBJECTS",
        "-*-command-variables-*-",
    ]),
    ("`make` automatic-variable dir/file suffixes", [
        "@D","@F","%D","%F","*D","*F","<D","<F","?D","?F","+D","+F","^D","^F",
    ]),
    ("Common POSIX environment", [
        "PATH","HOME","USER","LOGNAME","SHLVL","TMPDIR","PWD","_",
        "LANG","LC_COLLATE",
    ]),
]

CATEGORIZED = {v for _, vs in CATS for v in vs}

def mark(v, plat):
    return "✓" if v in per_os[plat] else " "

def row(v):
    return f"| `{v}` | {mark(v,'L')} | {mark(v,'M')} | {mark(v,'W')} |"

def render_category(name, vars_):
    # Only render rows that are present on at least one platform.
    present = [v for v in vars_ if any(v in per_os[p] for p in "LMW")]
    if not present:
        return ""
    out = [f"### {name}", "",
           "| Variable | L | M | W |",
           "| --- | :-: | :-: | :-: |"]
    out += [row(v) for v in present]
    return "\n".join(out) + "\n"

def wrap(items, width=78):
    out, line = [], ""
    for v in items:
        if len(line) + len(v) + 2 > width:
            out.append(line.rstrip())
            line = ""
        line += v + ", "
    if line:
        out.append(line.rstrip().rstrip(","))
    return "\n".join(out)

# ---- write README ----
lines = []
P = lines.append

P("# r-makevars-variables")
P("")
P("A throwaway R package whose `src/Makevars` prints every `make` variable")
P("visible during `R CMD INSTALL`. CI runs the probe on `ubuntu-latest`,")
P("`macos-latest`, and `windows-latest` with `r-version: 'release'` and")
P("commits the raw logs to [`vars/`](vars/). The cross-platform diff is")
P("below.")
P("")
P("## The probe")
P("")
P("```make")
P(".PHONY: echo_vars")
P("all: echo_vars")
P("echo_vars:")
P("\t@echo \"$(.VARIABLES)\"")
P("```")
P("")
P("R's build of an installed package merges its own `Makeconf` with the")
P("user's `src/Makevars`. Because `all:` is the first target in the merged")
P("file, it runs before the SHLIB rules and `$(.VARIABLES)` prints every")
P("variable currently defined — R config, compiler/linker flags, make")
P("built-ins, and inherited environment.")
P("")
P("Full scaffolding recipe (rig, usethis, the package-name gotcha): see")
P("[`dev/RECIPE.md`](dev/RECIPE.md).")
P("")
P("## Re-running")
P("")
P("- **CI**: push to `main`, or `gh workflow run dump-makevars.yml`. The")
P("  workflow runs `R CMD INSTALL .` on each runner and commits the per-OS")
P("  install log back to `vars/`.")
P("- **Locally**: `R CMD INSTALL .` on whatever platform you have. The")
P("  variable dump appears in the install output before the compile lines.")
P("- **Check action pins** against the latest releases: `just check-action-versions`.")
P("")
totals = {p: sum(1 for v in per_os[p] if not is_noise(v)) for p in "LMW"}
P("## Cross-platform availability")
P("")
P("Tables show whether each variable is set on Linux (**L**), macOS (**M**),")
P("and Windows (**W**) during `R CMD INSTALL`. Vars that don't surface on")
P("*any* of the three runners are omitted from a category.")
P("")
P(f"After filtering CI-runner noise (`GITHUB_*`, `RUNNER_*`, `JAVA_HOME_*`,")
P(f"`GOROOT_*`, `ANDROID_*`, browser-driver paths, …): "
  f"linux **{totals['L']}** · macos **{totals['M']}** · windows **{totals['W']}**.")
P("")
for name, vs in CATS:
    chunk = render_category(name, vs)
    if chunk:
        P(chunk)

# Extras: vars in CI logs (any platform) that no category claimed.
extras_all = sorted({v for s in per_os.values() for v in s
                     if v not in CATEGORIZED and not is_noise(v)})
def avail_key(v):
    return tuple(p for p in "LMW" if v in per_os[p])

groups = {}
for v in extras_all:
    groups.setdefault(avail_key(v), []).append(v)

P("### Platform extras")
P("")
P("Variables present in CI logs that don't fit the categories above —")
P("mostly Rtools/mingw-only tooling on Windows and a handful of macOS")
P("framework paths.")
P("")
LABEL = {
    ("L","M","W"): "All three",
    ("L","M"):    "Linux + macOS",
    ("L","W"):    "Linux + Windows",
    ("M","W"):    "macOS + Windows",
    ("L",):       "Linux only",
    ("M",):       "macOS only",
    ("W",):       "Windows only",
}
for key in [("L","M","W"),("L","M"),("M","W"),("L","W"),("W",),("M",),("L",)]:
    items = groups.get(key, [])
    if not items:
        continue
    P(f"**{LABEL[key]}** ({len(items)})")
    P("")
    P("```")
    P(wrap(items))
    P("```")
    P("")

P("## Layout")
P("")
P("- [`src/Makevars`](src/Makevars) — the probe (4 lines).")
P("- [`vars/`](vars/) — raw `R CMD INSTALL` logs per OS, refreshed by CI.")
P("- [`.github/workflows/dump-makevars.yml`](.github/workflows/dump-makevars.yml) — the dump+commit workflow.")
P("- [`justfile`](justfile) — `gh-latest` and `check-action-versions` recipes.")
P("- [`dev/RECIPE.md`](dev/RECIPE.md) — original scaffolding lab notes.")

Path("README.md").write_text("\n".join(lines) + "\n")
print(f"wrote README.md: {len(lines)} lines, "
      f"L={totals['L']} M={totals['M']} W={totals['W']}")
