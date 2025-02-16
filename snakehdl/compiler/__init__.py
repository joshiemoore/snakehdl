from .compiler import Compiler, Compiled  # noqa: F401
from .compiler_python import PythonCompiler

_COMPILERS = {
  'python': PythonCompiler,
}
