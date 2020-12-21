from distutils.core import setup, Extension

module = Extension('graphModule',
                   sources=['cpyConverter.cpp', 'cycle/cycles.cpp', 'new_position/new_positions.cpp',
                            'fragm_alwdFaces/func.cpp', 'alpha_path/alpha_path.cpp', 'get_optimal_path/dijkstra_algo.cpp'],
                   include_dirs=['cycle', 'fragm_alwdFaces', 'alpha_path',
                                 'new_position', 'get_optimal_path'],
                   language='c++',
                   extra_compile_args=["-std:c++17"])

setup(name='PackageName',
      version='1.0',
      description='This is a package for graphModule',
      ext_modules=[module])
