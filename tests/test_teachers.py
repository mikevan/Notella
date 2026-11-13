import json
import tempfile
import unittest
from unittest.mock import patch
from notella.teachers import LocalTeacher, teaching_candidate

class TeacherTests(unittest.TestCase):
    def test_external_addresses_refused(self):
        for url in ['https://example.com/v1','http://127.0.0.1@example.com/v1','http://localhost/v1?x=1']:
            with self.assertRaises(ValueError):LocalTeacher('test',url)
    def test_resume_never_repeats_completed_generation(self):
        provider=LocalTeacher('test')
        with tempfile.TemporaryDirectory() as d, patch.object(provider,'generate',return_value=dict(output='candidate',admittedForTraining=False)) as generate:
            first=teaching_candidate(provider,'ontology',['concept'],[dict(role='user',content='draft')],d)
            second=teaching_candidate(provider,'ontology',['concept'],[dict(role='user',content='draft')],d)
            self.assertEqual(first,second);generate.assert_called_once()
            self.assertFalse(second['admittedForTraining'])
            with self.assertRaises(ValueError):teaching_candidate(provider,'changed',['concept'],[],d)
    def test_uncertain_failure_requires_explicit_retry(self):
        provider=LocalTeacher('test')
        with tempfile.TemporaryDirectory() as d, patch.object(provider,'generate',side_effect=TimeoutError('timed out')) as generate:
            with self.assertRaises(TimeoutError):teaching_candidate(provider,'o',['c'],[dict(role='user',content='draft')],d)
            with self.assertRaises(ValueError):teaching_candidate(provider,'o',['c'],[dict(role='user',content='draft')],d)
            generate.assert_called_once()
            self.assertFalse(json.loads(__import__('pathlib').Path(d,'error.json').read_text())['admittedForTraining'])


class TeacherHTTPTests(unittest.TestCase):
    def test_wire_request_and_raw_response(self):
        from http.server import BaseHTTPRequestHandler,HTTPServer
        import threading
        captured=[]
        raw=b'{"model":"fixture-teacher","choices":[{"message":{"content":"candidate"},"finish_reason":"stop"}]}'
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                captured.append((self.path,json.loads(self.rfile.read(int(self.headers['Content-Length'])))))
                self.send_response(200);self.end_headers();self.wfile.write(raw)
            def log_message(self,*args):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            provider=LocalTeacher('fixture-teacher',f'http://127.0.0.1:{server.server_port}/v1')
            with tempfile.TemporaryDirectory() as d:
                result=teaching_candidate(provider,'o',['c'],[dict(role='user',content='draft')],d)
                self.assertEqual(result['responseBody'],raw.decode())
                self.assertEqual(result['output'],'candidate')
                self.assertEqual(captured[0][0],'/v1/chat/completions')
                self.assertEqual(set(captured[0][1]),{'model','messages','temperature','max_tokens','stream'})
                self.assertFalse(result['admittedForTraining'])
        finally:server.shutdown();server.server_close();thread.join()

class TeacherIntegrityTests(unittest.TestCase):
    def test_saved_result_modification_is_refused(self):
        from pathlib import Path
        provider=LocalTeacher('fixture')
        with tempfile.TemporaryDirectory() as d, patch.object(provider,'generate',return_value=dict(output='draft')):
            teaching_candidate(provider,'ontology',['concept'],[dict(role='user',content='draft')],d)
            path=Path(d)/'result.json';value=json.loads(path.read_text());value['output']='changed';path.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError,'integrity'):
                teaching_candidate(provider,'ontology',['concept'],[dict(role='user',content='draft')],d)



class TeacherFailureReceiptTests(unittest.TestCase):
    def test_malformed_and_http_error_bodies_are_preserved(self):
        from http.server import BaseHTTPRequestHandler,HTTPServer
        from pathlib import Path
        import threading
        class Handler(BaseHTTPRequestHandler):
            status=200
            def do_POST(self):
                self.rfile.read(int(self.headers['Content-Length']))
                self.send_response(self.status);self.end_headers();self.wfile.write(b'invalid teacher response')
            def log_message(self,*args):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            provider=LocalTeacher('fixture',f'http://127.0.0.1:{server.server_port}/v1')
            for status in (200,500):
                Handler.status=status
                with self.subTest(status=status),tempfile.TemporaryDirectory() as d:
                    with self.assertRaises(Exception):teaching_candidate(provider,'o',['c'],[dict(role='user',content='draft')],d)
                    error=json.loads(Path(d,'error.json').read_text())
                    self.assertEqual(error['responseBody'],'invalid teacher response')
                    self.assertFalse(Path(d,'result.json').exists())
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
