from setuptools import setup, Extension
# XXX: No idea where this would go in a config file so I am putting it here...
setup(
    ext_modules=[
        Extension(
            "propcache._propcache_c",
            ["src/propcache/_propcache_c.c"],
            include_dirs=["src/propcache"],
        )
    ]
)
