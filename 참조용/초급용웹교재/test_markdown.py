"""문서 서식 변환 검증. python -m unittest test_markdown -v"""
import unittest
import build

class MarkdownTests(unittest.TestCase):
    def test_emphasis_and_code(self):
        self.assertEqual(build.inline('**선언**과 `int health;`'), '<strong>선언</strong>과 <code>int health;</code>')
        self.assertIn('<code>int</code>', build.inline('**`int` 자료형**'))
        self.assertEqual(build.inline('`**문자열** <tag>`'), '<code>**문자열** &lt;tag&gt;</code>')

    def test_headings_lists_quote_and_table(self):
        value = build.render('#### 작은 제목\n\n- 첫째\n- 둘째\n\n1. 시작\n2. 끝\n\n> **주의**\n\n| 자료형 | 예 |\n| --- | --- |\n| `bool` | `a || b` |')
        for tag in ('<h3>작은 제목</h3>', '<ul>', '<ol>', '<blockquote>', '<strong>주의</strong>', '<table>', '<code>a || b</code>'):
            self.assertIn(tag, value)
        self.assertEqual(value.count('<td>'), 2)

    def test_code_block_and_html_are_not_executed(self):
        value = build.render('```csharp\nif (x < 5) {}\n```\n\n<script>alert(1)</script>')
        self.assertIn('x &lt; 5', value)
        self.assertNotIn('<script>', value)
        self.assertIn('&lt;script&gt;', value)

    def test_hint_ends_at_next_section(self):
        value = build.render('### 힌트와 해설\n힌트\n### 다음 항목\n본문')
        self.assertIn('</details><h2>다음 항목</h2>', value)

    def test_all_chapters_and_variable_depth(self):
        self.assertEqual(len(build.chapters), 8)
        variable = build.chapters[1]['body']
        for tag in ('<strong>', '<code>', '<h3>', '<table>'):
            self.assertIn(tag, variable)
        for chapter in build.chapters:
            self.assertGreaterEqual(chapter['body'].count('<h3>'), 2)
            self.assertEqual(chapter['body'].count('<details>'), chapter['body'].count('</details>'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
