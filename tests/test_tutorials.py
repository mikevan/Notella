import contextlib,io,os,tempfile,threading,unittest
from unittest.mock import patch
from examples.tutorial import teaching_material,main as tutorial_main
from examples.http_tutorial import main as http_main
from notella import Notella
from notella.http import server

class TutorialTests(unittest.TestCase):
 def test_first_tutorial_runs_as_documented(self):
  with tempfile.TemporaryDirectory() as tmp,patch('sys.argv',['tutorial','--store',tmp]),contextlib.redirect_stdout(io.StringIO()) as output:
   tutorial_main();self.assertIn('"trainingStarted": false',output.getvalue());self.assertIn('"train": 3',output.getvalue())
 def test_http_tutorial_runs_as_documented(self):
  with tempfile.TemporaryDirectory() as tmp:
   token='documentation-example-test-token'
   http=server(Notella(tmp),token,port=0);threading.Thread(target=http.serve_forever,daemon=True).start()
   try:
    with patch.dict(os.environ,{'NOTELLA_API_TOKEN':token}),patch('sys.argv',['http_tutorial','--url','http://127.0.0.1:'+str(http.server_address[1])]),contextlib.redirect_stdout(io.StringIO()) as output:
     http_main();self.assertIn('"exactTargetMatches": 1',output.getvalue());self.assertIn('"trainingStarted": false',output.getvalue())
   finally:http.shutdown();http.server_close()
