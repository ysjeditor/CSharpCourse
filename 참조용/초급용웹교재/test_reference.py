"""원문 바이트 일치와 본문 절·모든 코드의 웹 표시를 검사합니다."""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import unittest
import build
from reference_renderer import parser, normalize_source

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]

class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_reference = False
        self.capture = None
        self.buffer = []
        self.headings, self.code = [], []
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            self.in_reference = dict(attrs).get('class') == 'reference-content'
        if self.in_reference and (tag == 'pre' or tag in ('h2','h3','h4','h5','h6')):
            self.capture = tag
            self.buffer = []
    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)
    def handle_endtag(self, tag):
        if self.capture == tag:
            (self.code if tag == 'pre' else self.headings).append(''.join(self.buffer))
            self.capture = None
        if tag == 'section':
            self.in_reference = False

class ReferenceTests(unittest.TestCase):
    def test_full_source_and_rendered_content(self):
        config = json.loads((ROOT / 'course.json').read_text(encoding='utf-8'))
        manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(config['chapters']), 8)
        report = []
        md = parser(build.chapter_files)
        for index, row in enumerate(config['chapters']):
            with self.subTest(chapter=index+1):
                original = WORKSPACE / row['source']
                local = ROOT / row['file']
                self.assertEqual(local.read_bytes(), original.read_bytes())
                self.assertEqual(hashlib.sha256(local.read_bytes()).hexdigest(), row['sha256'])
                source = local.read_text(encoding='utf-8')
                body = normalize_source(source, local.name).split('\n', 1)[1]
                tokens = md.parse(body)
                expected_code = [t.content.rstrip('\n') for t in tokens if t.type in ('fence', 'code_block')]
                expected_headings = []
                for i, token in enumerate(tokens):
                    if token.type == 'heading_open':
                        expected_headings.append(''.join(c.content for c in tokens[i+1].children
                            if c.type in ('text','code_inline')))
                parsed = Extract(); parsed.feed(build.chapters[index]['body'])
                self.assertEqual(parsed.code, expected_code)
                self.assertEqual(parsed.headings, expected_headings)
                # 형식 보정이 문장·코드·연습문제의 내용을 삭제하지 않는지 검사합니다.
                raw_lines = [line for line in source.splitlines() if line.strip() and not line.strip().startswith('```')]
                fixed_lines = [line for line in normalize_source(source, local.name).splitlines()
                    if line.strip() and not line.strip().startswith('```')]
                self.assertEqual([x.replace('\\|', '|') for x in raw_lines],
                    [x.replace('\\|', '|') for x in fixed_lines])
                if index == 1:
                    self.assertIn('<code>true || false</code>', build.chapters[index]['body'])
                report.append(dict(chapter=index+1, source_bytes=len(local.read_bytes()),
                    sha256=row['sha256'], headings=len(parsed.headings), code_blocks=len(parsed.code), status='passed'))
        overview = manifest['overview']
        self.assertEqual((ROOT / overview['file']).read_bytes(), (WORKSPACE / overview['source']).read_bytes())
        (ROOT / 'reference-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    unittest.main(verbosity=2)
