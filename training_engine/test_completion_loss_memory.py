"""Optional training-environment numerical checks; not a core dependency."""
import unittest
import torch
from completion_loss import token_cross_entropy,completion_loss

class MemoryBoundedLossTests(unittest.TestCase):
 def test_value_and_gradient_match_full_loss(self):
  for dtype in (torch.float32,torch.float16):
   torch.manual_seed(42);a=torch.randn(1,137,41,dtype=dtype,requires_grad=True);b=a.detach().clone().requires_grad_(True);labels=torch.randint(0,41,(1,137))
   expected=torch.nn.functional.cross_entropy(a.float().reshape(-1,41),labels.reshape(-1));actual=token_cross_entropy(b,labels,chunk_tokens=32)
   expected.backward();actual.backward()
   self.assertTrue(torch.allclose(actual,expected,atol=1e-6,rtol=1e-6));self.assertTrue(torch.allclose(a.grad,b.grad,atol=2e-6,rtol=1e-4))
 def test_prompt_masking_and_target_shift(self):
  class Model(torch.nn.Module):
   def __init__(self):super().__init__();self.logits=torch.nn.Parameter(torch.randn(1,6,11));self.positions=None
   def forward(self,**kwargs):
    self.positions=kwargs['logits_to_keep'];return type('Output',(),dict(logits=self.logits[:,self.positions]))()
  model=Model();labels=torch.tensor([[-100,-100,-100,3,4,5]])
  loss,_=completion_loss(model,dict(input_ids=torch.ones((1,6),dtype=torch.long),labels=labels));self.assertEqual(model.positions.tolist(),[2,3,4]);loss.backward();self.assertEqual(float(model.logits.grad[0,:2].abs().sum()),0)
 def test_invalid_chunk_and_empty_target_refused(self):
  with self.assertRaises(ValueError):token_cross_entropy(torch.zeros(1,2,3),torch.zeros(1,2,dtype=torch.long),0)
  with self.assertRaises(ValueError):token_cross_entropy(torch.zeros(1,0,3),torch.zeros(1,0,dtype=torch.long))


class CpuLogitTransferTests(unittest.TestCase):
 @unittest.skipUnless(torch.cuda.is_available(),'CUDA transfer check requires training hardware')
 def test_cpu_logits_return_gpu_loss_and_differentiable_cpu_gradient(self):
  class Model(torch.nn.Module):
   def __init__(self):super().__init__();self.logits=torch.nn.Parameter(torch.randn(1,6,11))
   def forward(self,**kwargs):return type('Output',(),dict(logits=self.logits[:,kwargs['logits_to_keep'].to(self.logits.device)]))()
  model=Model();labels=torch.tensor([[-100,-100,-100,3,4,5]],device='cuda')
  loss,out=completion_loss(model,dict(input_ids=torch.ones((1,6),dtype=torch.long,device='cuda'),labels=labels))
  self.assertEqual(loss.device.type,'cuda');self.assertEqual(out.logits.device.type,'cpu');loss.backward();self.assertTrue(torch.isfinite(model.logits.grad).all())

if __name__=='__main__':unittest.main()
