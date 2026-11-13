import copy,tempfile,unittest
from unittest.mock import patch
from notella import Notella
from notella.teachers import LocalTeacher,teaching_candidate
from notella.teacher_reviews import record_teacher_review

class TeacherReviewTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.api=Notella(self.temp.name+'/store');provider=LocalTeacher('fixture')
  with patch.object(provider,'generate',return_value=dict(output='synthetic draft')):
   self.candidate=teaching_candidate(provider,'ontology',['concept'],[dict(role='user',content='draft')],self.temp.name+'/candidate')
  self.reviewer=dict(name='Agent reviewer',kind='agent',independent=False)
  self.criteria=[dict(id='policy',requirement='Follows supplied policy')]
 def review(self,status):return record_teacher_review(self.api,self.candidate,self.reviewer,self.criteria,[dict(criterion='policy',status=status,rationale='Recorded reviewer assertion')])['artifact']
 def test_pass_does_not_grant_training_permission(self):
  result=self.review('pass');self.assertEqual(result['disposition'],'review_passed');self.assertFalse(result['trainingPermissionGranted']);self.assertFalse(self.candidate['admittedForTraining'])
 def test_failure_and_uncertainty_have_distinct_dispositions(self):
  self.assertEqual(self.review('fail')['disposition'],'rejected');self.assertEqual(self.review('uncertain')['disposition'],'needs_review')
 def test_tampering_and_missing_judgment_are_refused(self):
  original=copy.deepcopy(self.candidate);self.candidate['output']='changed'
  with self.assertRaises(ValueError):self.review('pass')
  with self.assertRaises(ValueError):record_teacher_review(self.api,original,self.reviewer,self.criteria,[])
if __name__=='__main__':unittest.main()
