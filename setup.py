
# versions
import os
__version__ = os.environ.get('VERSION_NEW', '0.5.4')
libjpeg_versions = ['6b','8d']

# requirements
try:
  with open('requirements.txt') as f:
    reqs = f.read().splitlines()
except:
  reqs = []

import codecs
import setuptools
with codecs.open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

# import unittest
# def test_suite():
#     test_loader = unittest.TestLoader()
#     test_suite = test_loader.discover('tests', pattern='test_*.py')
#     return test_suite

# create version dependent extensions
import sys
import re
cfiles = {}
hfiles = {}
cjpeglib = {}
for v in libjpeg_versions:
  clib = f'jpeglib/cjpeglib/{v}'
  #files = []
  files = [f'{clib}/{f}' for f in os.listdir(clib) if re.fullmatch(f'.*\.(c|h)', f)]
  for excluded_module in ['jmemdos','jmemmac','jmemansi','ansi2knr','ckconfig','jmemname', # platform dependents
                          'djpeg','cjpeg','rdjpgcom','wrjpgcom','cdjpeg','jpegtran', # executables
                          'rdbmp','wrbmp','rdcolmap','rdppm','wrppm','rdtarga','wrtarga','rdrle','wrrle','rdgif','wrgif','rdswitch', # others
                          'example']: # example
    lim = -2 - len(excluded_module)
    files = [f for f in files if f[lim:-2] != excluded_module]
  #
  cfiles[v] = [f for f in files if f[-2:] == '.c']
  hfiles[v] = [f for f in files if f[-2:] == '.h']

  sources = ['jpeglib/cjpeglib/cjpeglib.c',*cfiles[v]]
  if sys.argv[1] == 'sdist':
    sources = [*sources, *hfiles[v]]
  cjpeglib[v] = setuptools.Extension(
    name = f"jpeglib/cjpeglib/cjpeglib_{v}",
    sources = sources,
    headers = hfiles[v],
    define_macros = [("BITS_IN_JSAMPLE", 8)],
    extra_compile_args=["-fPIC"],
    library_dirs=[f'./{clib}'],
    include_dirs=[f'./{clib}'],
  )

setuptools.setup(
  name = 'jpeglib',
  version = __version__,
  author = u'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Python envelope for the popular C library libjpeg for handling JPEG files.',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='MPL',
  #test_suite = 'setup.test_suite',
  #url = 'https://github.com/martinbenes1996/jpeglib',
  #download_url = 'https://github.com/martinbenes1996/jpeglib/archive/0.1.0.tar.gz',
  keywords = ['libjpeg','jpeglib','jpeg','jpg','dct-coefficients','dct'],
  install_requires=reqs,
  package_dir={'': '.'},
  package_data={'': ['data/*']},
  include_package_data=True,
  ext_modules=[cjpeglib[v] for v in libjpeg_versions],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Topic :: Education',
    'Topic :: Multimedia',
    'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Image Processing',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Security',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ],
)