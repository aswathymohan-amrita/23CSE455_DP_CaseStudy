# C++ verification instructions

The current host has no `g++`, Clang, MSVC `cl`, `c++`, or Zig compiler on PATH. No compiler was installed. Therefore no C++ source was compiled or run, and no stdout, stderr, exit code, or timing is claimed for C++.

On Windows with a C++17-capable `g++` already installed, open PowerShell in `submission/B1/Part3` and run:

```powershell
g++ --version
$out = Join-Path $env:TEMP 'b1-cpp-verification'
New-Item -ItemType Directory -Force $out | Out-Null
$sources = Get-ChildItem -Path . -Recurse -Filter '*.cpp' | Sort-Object FullName
foreach ($src in $sources) {
  $name = [IO.Path]::GetFileNameWithoutExtension($src.Name)
  $exe = Join-Path $out ($name + '.exe')
  $stem = Join-Path $out $name
  & g++ -std=c++17 $src.FullName -o $exe 2> ($stem + '_compile_stderr.txt')
  $compileCode = $LASTEXITCODE
  if ($compileCode -ne 0) {
    "compile_exit_code=$compileCode" | Set-Content ($stem + '_result.txt')
    continue
  }
  & $exe 1> ($stem + '_stdout.txt') 2> ($stem + '_stderr.txt')
  $runCode = $LASTEXITCODE
  "compile_exit_code=0`nrun_exit_code=$runCode`nsource=$($src.FullName)`ncommand=g++ -std=c++17 `"$($src.FullName)`" -o `"$exe`"`nrun_command=`"$exe`"" | Set-Content ($stem + '_result.txt')
}
```

Review and preserve the generated stdout, stderr, compile stderr, and result files alongside `reproduced_2026-10-11/`; then update the C++ rows in the canonical dataset from actual outcomes. This script compiles each source to a temporary executable and does not modify the source files.
