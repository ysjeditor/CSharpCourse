"""실제 .NET 통합 검증: python test_runner.py"""
import json
from pathlib import Path
import re
import subprocess
import unittest
import threading
import urllib.request
import urllib.error
import server

class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.FRAMEWORK = server.framework()

    def test_all_exercise_solutions(self):
        for i, exercise in enumerate(server.EXERCISES):
            with self.subTest(lesson=i+1):
                result = server.execute(exercise['solution'], i)
                self.assertEqual(result['status'], 'passed', result)
                self.assertEqual(len(result['results']), len(exercise['cases']))

    def test_wrong_answer(self):
        result = server.execute('System.Console.WriteLine(0);', 0)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['results'][0]['actual'], '0')

    def test_compile_error(self):
        result = server.execute('System.Console.WriteLine(missing);', 0)
        self.assertEqual(result['status'], 'compile_error')
        self.assertEqual(result['diagnostics'][0]['line'], 1)
        self.assertEqual(result['diagnostics'][0]['code'], 'CS0103')

    def test_runtime_error(self):
        result = server.execute('int[] a={1};System.Console.WriteLine(a[2]);', 0, mode='run')
        self.assertEqual(result['status'], 'runtime_error')
        self.assertIn('IndexOutOfRangeException', result['results'][0]['actual'])

    def test_time_limit(self):
        result = server.execute('while(true) {}', 0, mode='run')
        self.assertEqual(result['status'], 'timeout')

    def test_output_limit(self):
        result = server.execute('while(true) System.Console.WriteLine(new string(\'x\',1000));', 0, mode='run')
        self.assertEqual(result['status'], 'output_limit')
        self.assertLessEqual(len(result['results'][0]['actual'].encode('utf-8')), server.LIMIT)

    def test_custom_input(self):
        result = server.execute('System.Console.WriteLine(System.Console.ReadLine());', 0, mode='run', stdin='안녕하세요\n')
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['results'][0]['actual'], '안녕하세요')

    def test_generated_javascript(self):
        page = (Path(__file__).parent / 'index.html').read_text(encoding='utf-8')
        js = re.search(r'<script>(.*?)</script>', page, re.S).group(1)
        result = subprocess.run(['node','--check'], input=js, encoding='utf-8', capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(re.search(r'const exercises=(.*?);\n', js).group(1))
        self.assertEqual(len(data), 8)
        self.assertTrue(all('solution' not in exercise for exercise in data))

    def test_http_execution_and_access_checks(self):
        http = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{http.server_port}'
        try:
            with urllib.request.urlopen(base) as response:
                page = response.read().decode('utf-8')
                self.assertIn(f'content="{server.TOKEN}"', page)
                self.assertIn('const exercises=', page)
            data = json.dumps(dict(source=server.EXERCISES[0]['solution'], lesson=0)).encode()
            request = urllib.request.Request(base+'/api/run', data=data,
                headers={'Content-Type':'application/json','Origin':base,'X-Runner-Token':server.TOKEN})
            with urllib.request.urlopen(request) as response:
                self.assertEqual(json.load(response)['status'], 'passed')
            for headers in ({}, {'Origin':'https://example.com','X-Runner-Token':server.TOKEN}):
                with self.assertRaises(urllib.error.HTTPError) as context:
                    urllib.request.urlopen(urllib.request.Request(base+'/api/run', data=data, headers=headers))
                self.assertEqual(context.exception.code, 403)
            with self.assertRaises(urllib.error.HTTPError) as context:
                urllib.request.urlopen(urllib.request.Request(base, headers={'Host':'example.com'}))
            self.assertEqual(context.exception.code, 403)
        finally:
            http.shutdown()
            http.server_close()
            thread.join()

if __name__ == '__main__':
    unittest.main(verbosity=2)
