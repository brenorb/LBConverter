# -*- coding: utf-8 -*-

import os
import runpy
import subprocess
import sys
import types
import unittest


class PdfExtractionTest(unittest.TestCase):
    def extract(self, result):
        posted = []
        modules = {}
        for name, member, function in (
            ("unotext", "unoconv", lambda *args: self.fail("unexpected UNO call")),
            ("geturl", "download", lambda url: "/fixture/input.pdf"),
            ("escreve", "escrevetxt", lambda url, text: posted.append((url, text))),
        ):
            module = types.ModuleType(name)
            setattr(module, member, function)
            modules[name] = sys.modules.get(name)
            sys.modules[name] = module
        try:
            source = os.path.join(
                os.path.dirname(__file__), "..", "lbconverter", "scripts", "fextractor.py"
            )
            extract = runpy.run_path(source)["extrator"]
        finally:
            for name, module in modules.items():
                if module is None:
                    del sys.modules[name]
                else:
                    sys.modules[name] = module

        class Poppler:
            CalledProcessError = subprocess.CalledProcessError

            def call(self, args):
                return result.returncode if isinstance(result, subprocess.CalledProcessError) else 0

            def check_output(self, args):
                if isinstance(result, Exception):
                    raise result
                return result

        namespace = getattr(extract, "__globals__", None)
        if namespace is None:
            namespace = extract.func_globals
        namespace["subprocess"] = Poppler()
        namespace["sleep"] = lambda seconds: None
        extract("https://fixture.invalid/api/doc/test/42/download", "/tmp/", "fixture.pdf")
        return posted

    def test_posts_extracted_pdf_text(self):
        self.assertEqual(
            self.extract(b"fixture text\n"),
            [("https://fixture.invalid/api/doc/test/42", b"fixture text\n")],
        )

    def test_nonzero_pdf_conversion_preserves_fallback(self):
        self.assertEqual(
            self.extract(subprocess.CalledProcessError(1, "pdftotext")),
            [("https://fixture.invalid/api/doc/test/42", "nulo")],
        )
