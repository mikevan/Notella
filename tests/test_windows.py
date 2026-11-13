import copy,unittest
from notella.windows import RollingInterceptWindow,semantic_delta,LatestWindowWork

class WindowTests(unittest.TestCase):
 def record(self,i,t,available=None):return dict(id=i,observedAtMs=t,availableAtMs=t if available is None else available,payload={'kind':'synthetic'})
 def test_ten_seconds_then_slide_one_second_without_recounting(self):
  w=RollingInterceptWindow()
  for i in range(1,11):w.ingest(self.record('i'+str(i),i*1000))
  first=w.advance(10000);self.assertEqual((len(first['added']),first['activeCount']),(10,10))
  w.ingest(self.record('i11',11000));second=w.advance(11000)
  self.assertEqual([r['id'] for r in second['added']],['i11']);self.assertEqual(second['expiredIds'],['i1']);self.assertEqual(second['retainedCount'],9)
 def test_late_current_record_only_appears_when_available(self):
  w=RollingInterceptWindow();w.advance(10000);w.ingest(self.record('late',5000,11000));frame=w.advance(11000)
  self.assertEqual([r['id'] for r in frame['added']],['late'])
 def test_old_late_record_not_revived(self):
  w=RollingInterceptWindow();w.advance(20000);r=w.ingest(self.record('old',5000,21000));self.assertFalse(r['accepted']);frame=w.advance(21000);self.assertEqual(frame['lateOutsideWindowIds'],['old']);self.assertEqual(frame['activeCount'],0)
 def test_expiry_without_new_intercepts_is_explicit(self):
  w=RollingInterceptWindow();w.ingest(self.record('one',1000));w.advance(10000);frame=w.advance(11000)
  self.assertEqual(frame['expiredIds'],['one']);self.assertEqual(frame['added'],[]);self.assertNotIn('criticality',frame)
 def test_capacity_loss_is_reported_not_silently_sampled(self):
  w=RollingInterceptWindow(max_records=1);w.ingest(self.record('one',1000));r=w.ingest(self.record('two',2000));self.assertEqual(r['reason'],'capacity_exceeded');self.assertEqual(w.advance(10000)['capacityRejects'],1)
 def test_conflicting_ids_and_backdated_receipt_rejected(self):
  w=RollingInterceptWindow();w.ingest(self.record('one',1000))
  with self.assertRaises(ValueError):w.ingest(self.record('one',2000))
  w.advance(10000)
  with self.assertRaises(ValueError):w.ingest(self.record('two',9000))
 def test_future_records_not_visible_and_stride_enforced(self):
  w=RollingInterceptWindow();w.ingest(self.record('future',12000));self.assertEqual(w.advance(10000)['activeCount'],0)
  with self.assertRaises(ValueError):w.advance(12000)
 def test_graph_delta_records_only_changes(self):
  before=dict(nodes=[dict(id='n1',count=2)],edges=[],assessment={'criticality':'high'})
  after=copy.deepcopy(before);after['nodes'][0]['count']=3;after['edges'].append(dict(id='e1',support=1));r=semantic_delta(before,after)
  self.assertEqual(len(r['nodes']['updated']),1);self.assertEqual(len(r['edges']['added']),1);self.assertFalse(r['assessmentChanged']);self.assertEqual(before['nodes'][0]['count'],2)
 def test_slow_inference_coalesces_and_marks_old_results(self):
  q=LatestWindowWork();state=dict(nodes=[],edges=[]);q.offer(dict(revision=1,state=state));self.assertEqual(q.begin()['revision'],1)
  q.offer(dict(revision=2,state=state));q.offer(dict(revision=3,state=state));self.assertIsNone(q.begin());self.assertTrue(q.finish(1)['stale']);self.assertEqual(q.begin()['revision'],3)


class WindowContinuityTests(unittest.TestCase):
 def test_coalescing_keeps_changes_from_skipped_tick(self):
  q=LatestWindowWork()
  def frame(rev):return dict(revision=rev,state=dict(nodes=[dict(id='n'+str(i)) for i in range(1,rev+1)],edges=[]))
  q.offer(frame(1));q.begin();q.offer(frame(2));q.offer(frame(3));self.assertFalse(q.finish(1,accepted=True)['accepted'])
  work=q.begin();self.assertEqual([n['id'] for n in work['delta']['nodes']['added']],['n1','n2','n3'])
  self.assertTrue(q.finish(3,accepted=True)['accepted']);q.offer(frame(4));work=q.begin();self.assertEqual([n['id'] for n in work['delta']['nodes']['added']],['n4'])
 def test_raw_tick_delta_cannot_replace_full_scheduling_state(self):
  with self.assertRaises(ValueError):LatestWindowWork().offer(dict(revision=1,added=['n1']))
 def test_serialized_capacity_is_reported(self):
  w=RollingInterceptWindow(max_bytes=20);r=w.ingest(dict(id='n1',observedAtMs=1,availableAtMs=1));self.assertEqual(r['reason'],'capacity_exceeded');self.assertEqual(w.advance(1000)['capacityRejects'],1)
 def test_identical_report_retry_does_not_recount_after_tick(self):
  w=RollingInterceptWindow();r=dict(id='n1',observedAtMs=1,availableAtMs=1);w.ingest(r);w.advance(1000);self.assertEqual(w.ingest(r)['reason'],'duplicate_id');self.assertEqual(w.advance(2000)['retainedCount'],1)



class WindowResultRevalidationTests(unittest.TestCase):
 def test_explicit_latest_revalidation_allows_result_without_losing_pending_changes(self):
  q=LatestWindowWork()
  def frame(rev):return dict(revision=rev,state=dict(nodes=[dict(id='n'+str(i)) for i in range(1,rev+1)],edges=[]))
  q.offer(frame(1));q.begin();q.offer(frame(2));q.offer(frame(3))
  result=q.finish(1,accepted=True,revalidated_revision=3);self.assertTrue(result['accepted']);self.assertFalse(result['requiresRevalidation'])
  work=q.begin();self.assertEqual(work['baselineRevision'],1);self.assertEqual([n['id'] for n in work['delta']['nodes']['added']],['n2','n3'])
 def test_revalidation_against_an_obsolete_revision_is_refused(self):
  q=LatestWindowWork();q.offer(dict(revision=1,state=dict(nodes=[],edges=[])));q.begin();q.offer(dict(revision=3,state=dict(nodes=[],edges=[])))
  with self.assertRaises(ValueError):q.finish(1,accepted=True,revalidated_revision=2)

if __name__=='__main__':unittest.main()
