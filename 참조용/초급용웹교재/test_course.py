"""단원 순서·참조 대응과 본문의 모든 완성 예제의 실제 출력 검사."""
import json
from pathlib import Path
import re
import unittest
import server

ROOT = Path(__file__).resolve().parent

class CourseTests(unittest.TestCase):
    def test_basic_structure_examples(self):
        server.FRAMEWORK = server.framework()
        config = json.loads((ROOT / 'course.json').read_text(encoding='utf-8'))
        units = [(ROOT / row['supplement']).read_text(encoding='utf-8').removeprefix('# ') for row in config['chapters']]
        control_outputs = ['합격', '통과', '도움말', '통과',
            '0\n1\n2\n70\n80\n90', '3\n2\n1\n0', '1\n3\nTrue']
        results = []
        for number, unit in enumerate(units, 1):
            concept = unit.split('### 따라 하기', 1)[0]
            blocks = re.findall(r'```csharp\n(.*?)\n```', concept, re.S)
            self.assertTrue(blocks, f'{number}단원 기본 구조 코드 누락')
            for index, code in enumerate(blocks):
                with self.subTest(lesson=number, block=index+1):
                    self.assertIn('//', code)
                    result = server.execute(code, number-1, mode='run', stdin='42\n')
                    self.assertEqual(result['status'], 'ok', result)
                    if number == 3:
                        self.assertEqual(result['results'][0]['actual'], control_outputs[index])
                    results.append(dict(lesson=number, block=index+1, status=result['status']))
        (ROOT / 'structure-checks.json').write_text(json.dumps(results,
            ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    def test_mapping_and_sections(self):
        config = json.loads((ROOT / 'course.json').read_text(encoding='utf-8'))
        units = [(ROOT / row['supplement']).read_text(encoding='utf-8').removeprefix('# ') for row in config['chapters']]
        manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(units), 8)
        self.assertEqual([r['number'] for r in manifest['chapters']], list(range(1, 9)))
        for number, unit in enumerate(units, 1):
            self.assertTrue(unit.startswith(f'{number}장. '))
            self.assertEqual(unit.splitlines()[0], manifest['chapters'][number-1]['title'])
            for heading in ['학습 목표', '개념 읽기', '따라 하기', '결과 확인', '자주 하는 실수', '직접 해보기', '힌트와 해설']:
                self.assertIn('### ' + heading, unit)

    def test_all_complete_examples(self):
        server.FRAMEWORK = server.framework()
        config = json.loads((ROOT / 'course.json').read_text(encoding='utf-8'))
        units = [(ROOT / row['supplement']).read_text(encoding='utf-8').removeprefix('# ') for row in config['chapters']]
        results = []
        for number, unit in enumerate(units, 1):
            with self.subTest(lesson=number):
                code = re.search(r'### 따라 하기\s+```csharp\n(.*?)\n```', unit, re.S).group(1)
                expected = re.search(r'### 결과 확인\s+```text\n(.*?)\n```', unit, re.S).group(1)
                result = server.execute(code, number-1, mode='run')
                self.assertEqual(result['status'], 'ok', result)
                self.assertEqual(result['results'][0]['actual'], expected)
                self.assertEqual(result['diagnostics'], [], result['diagnostics'])
                results.append(dict(lesson=number, status=result['status'], output=expected))
        (ROOT / 'example-checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    unittest.main(verbosity=2)
